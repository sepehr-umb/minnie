import json
import os
import subprocess
from datetime import datetime, timezone


STATE_FILE  = os.environ.get("TUTOR_STATE_FILE", "/home/{student}/json-backend/brains.json")
PROJECT_DIR = os.environ.get("TUTOR_PROJECT_DIR", "/home/{student}/minnie")


def load_state(student: str) -> dict:
    path = STATE_FILE.format(student=student)
    try:
        with open(path, "r") as fp:
            return json.load(fp)
    except FileNotFoundError:
        raise FileNotFoundError(f"No state file found for student '{student}' at {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"State file is corrupt at {path}: {e}")


def save_state(state: dict, student: str) -> None:
    state["meta"]["last_saved"] = datetime.now(timezone.utc).isoformat()
    state["session"]["dirty"] = False
    path = STATE_FILE.format(student=student)
    tmp = path + ".tmp"
    with open(tmp, "w") as fp:
        json.dump(state, fp, indent=2, sort_keys=False)
    os.replace(tmp, path)


def get_current_step(state: dict) -> dict | None:
    step_id = state["progress"]["current_step"]
    return next((s for s in state["steps"] if s["id"] == step_id), None)


def advance_step(state: dict, student: str) -> dict:
    step_id = state["progress"]["current_step"]
    total = state["progress"]["total_steps"]

    if step_id > total:
        print("Tutorial complete!")
        return state

    for step in state["steps"]:
        if step["id"] == step_id:
            step["completed"] = True
            step["completed_at"] = datetime.now(timezone.utc).isoformat()
            state["progress"]["completed_steps"].append(step_id)
            break

    state["progress"]["current_step"] = step_id + 1
    state["session"]["dirty"] = True
    save_state(state, student)
    return state


def get_hints(state: dict) -> list:
    return get_current_step(state)["hints"]


def validate_step(step: dict, student: str) -> bool:
    v     = step.get("validation", {})
    vtype = v.get("type")
    if vtype == "inotifywait":
        target = os.path.join(PROJECT_DIR.format(student=student), v["target_file"])
        if v.get("check") == "exists":
            return os.path.exists(target)
        if v.get("check") == "modified":
            return os.path.exists(target)
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


def record_command(state: dict, cmd: str, exit_code: int, student: str) -> None:
    state["progress"]["last_exit_code"] = exit_code
    state["session"]["command_history"].append(cmd)
    state["session"]["dirty"] = True
    save_state(state, student)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--student", required=True, help="Linux username")
    parser.add_argument("--validate", type=int, metavar="EXIT_CODE",
                        help="Record last command's exit code and run validation")
    parser.add_argument("--flush", action="store_true",
                        help="Flush state to disk on logout (called by trap)")
    parser.add_argument("--cmd", default="", help="The command that was run")
    args = parser.parse_args()

    state = load_state(args.student)

    if args.validate is not None:
        record_command(state, args.cmd, args.validate, args.student)
        step = get_current_step(state)
        if step and not step.get("completed"):
            if validate_step(step, args.student):
                advance_step(state, args.student)
                print(f"✓ Step {step['id']} complete!")
            else:
                for hint in step.get("hints", []):
                    print(f"  → {hint}")

    elif args.flush:
        save_state(state, args.student)
        print("State flushed.")