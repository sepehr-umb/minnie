#!/usr/bin/env bash
# Local test harness for backend.py — no Minnie/Apache/Django needed.
# Simulates both validation types: inotifywait (file check) and curl_probe (HTTP check).

set -e

STUDENT="testuser"
TEST_DIR="$(pwd)/.local_test"
PROJECT_DIR="$TEST_DIR/project"
STATE_FILE="$TEST_DIR/brains.json"

export TUTOR_STATE_FILE="$STATE_FILE"
export TUTOR_PROJECT_DIR="$PROJECT_DIR"

cleanup() {
    echo ""
    echo "--- cleaning up ---"
    kill "$SERVER_PID" 2>/dev/null || true
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

echo "=== Setting up local test environment ==="
mkdir -p "$PROJECT_DIR"

# Reset state to step 1 (file check)
cat > "$STATE_FILE" <<'EOF'
{
  "meta": { "version": "1.0.0", "student": "testuser" },
  "progress": { "current_step": 1, "total_steps": 2, "completed_steps": [], "last_exit_code": 0 },
  "steps": [
    {
      "id": 1,
      "title": "Create your first file",
      "instructions": "Run: touch hello.txt",
      "completed": false,
      "completed_at": null,
      "validation": { "type": "inotifywait", "target_file": "hello.txt", "check": "exists" },
      "hints": ["Try using the 'touch' command followed by a filename.", "Make sure you are in the correct directory."]
    },
    {
      "id": 2,
      "title": "Start a web server",
      "instructions": "Run: python3 -m http.server 8080",
      "completed": false,
      "completed_at": null,
      "validation": { "type": "curl_probe", "url": "http://localhost:8080", "expected_status": 200 },
      "hints": ["Use python3 -m http.server followed by a port number.", "Check that port 8080 is not already in use."]
    }
  ],
  "session": { "ssh_login_count": 1, "command_history": [], "dirty": false }
}
EOF

echo ""
echo "=== TEST 1: inotifywait — validate BEFORE file exists (should show hints) ==="
python3 json-backend/backend.py --student "$STUDENT" --validate 0 --cmd "ls"

echo ""
echo "=== TEST 2: inotifywait — create file, then validate (should advance to step 2) ==="
touch "$PROJECT_DIR/hello.txt"
python3 json-backend/backend.py --student "$STUDENT" --validate 0 --cmd "touch hello.txt"

echo ""
echo "=== TEST 3: curl_probe — validate BEFORE server is running (should show hints) ==="
python3 json-backend/backend.py --student "$STUDENT" --validate 0 --cmd "ls"

echo ""
echo "=== TEST 4: curl_probe — start python http.server, then validate (should advance) ==="
python3 -m http.server 8080 --directory "$PROJECT_DIR" &>/dev/null &
SERVER_PID=$!
sleep 1  # give it a moment to bind
python3 json-backend/backend.py --student "$STUDENT" --validate 0 --cmd "python3 -m http.server 8080"

echo ""
echo "=== TEST 5: --flush ==="
python3 json-backend/backend.py --student "$STUDENT" --flush

echo ""
echo "=== Final state ==="
python3 -c "import json; s=json.load(open('$STATE_FILE')); print(json.dumps(s['progress'], indent=2))"
