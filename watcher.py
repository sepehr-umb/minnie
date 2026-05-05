import os
import json
import time
import subprocess
import threading
from datetime import datetime, timezone
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

STATE_FILE  = os.environ.get("TUTOR_STATE_FILE", "/home/{student}/json-backend/brains.json")
PROJECT_DIR = os.environ.get("TUTOR_PROJECT_DIR", "/home/{student}/minnie")

DEBOUNCE_SECONDS = 1.5
POLL_INTERVAL    = 3
TUTOR_START_TIME = time.time()
_last_event_time = 0


def load_state(student):
    with open(STATE_FILE.format(student=student)) as f:
        return json.load(f)


def save_state(state, student):
    state["meta"]["last_saved"] = datetime.now(timezone.utc).isoformat()
    state["session"]["dirty"]   = False
    path = STATE_FILE.format(student=student)
    tmp  = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, path)


def get_current_step(state):
    step_id = state["progress"]["current_step"]
    return next((s for s in state["steps"] if s["id"] == step_id), None)


def advance_step(state, student):
    step_id = state["progress"]["current_step"]
    if step_id > state["progress"]["total_steps"]:
        print("\nTutorial complete!\n")
        return state
    for step in state["steps"]:
        if step["id"] == step_id:
            step["completed"]    = True
            step["completed_at"] = datetime.now(timezone.utc).isoformat()
            state["progress"]["completed_steps"].append(step_id)
            break
    state["progress"]["current_step"] = step_id + 1
    state["session"]["dirty"] = True
    save_state(state, student)
    next_step = get_current_step(state)
    print(f"\n✓ Step {step_id} complete!")
    print(f"\n{next_step['instructions']}\n" if next_step else "\nAll steps complete!\n")
    return state


def validate_step(step, student):
    v     = step.get("validation", {})
    vtype = v.get("type")
    if vtype == "inotifywait":
        target = os.path.join(PROJECT_DIR.format(student=student), v["target_file"])
        if v.get("check") == "exists":
            return os.path.exists(target)
        if v.get("check") == "modified":
            return os.path.exists(target) and os.path.getmtime(target) > TUTOR_START_TIME
    if vtype == "curl_probe":
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "5", v["url"]],
            capture_output=True, text=True,
        )
        try:
            return int(result.stdout.strip()) == v.get("expected_status", 200)
        except ValueError:
            return False
    return False


class TutorHandler(FileSystemEventHandler):
    def __init__(self, student):
        self.student = student

    def on_modified(self, event):
        global _last_event_time
        if event.is_directory:
            return
        now = time.time()
        if now - _last_event_time < DEBOUNCE_SECONDS:
            return
        _last_event_time = now
        state = load_state(self.student)
        step  = get_current_step(state)
        if not step or step["validation"].get("type") != "inotifywait":
            return
        target = os.path.join(PROJECT_DIR.format(student=self.student), step["validation"]["target_file"])
        if event.src_path != target:
            return
        if validate_step(step, self.student):
            advance_step(state, self.student)
        else:
            for hint in step.get("hints", []):
                print(f"  → {hint}")


def polling_loop(student):
    while True:
        time.sleep(POLL_INTERVAL)
        state = load_state(student)
        step  = get_current_step(state)
        if not step or step["validation"].get("type") != "curl_probe":
            continue
        if validate_step(step, student):
            advance_step(state, student)


def main(student):
    state = load_state(student)
    step  = get_current_step(state)
    if step and not step.get("completed"):
        print(f"\n{step['instructions']}\n")
    observer = Observer()
    observer.schedule(TutorHandler(student), path=PROJECT_DIR.format(student=student), recursive=False)
    observer.start()
    threading.Thread(target=polling_loop, args=(student,), daemon=True).start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--student", required=True)
    args = parser.parse_args()
    main(args.student)