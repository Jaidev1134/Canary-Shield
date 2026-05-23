from flask import Flask, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import glob
from config import TEST_DIR, PID_FILE, INCIDENT_LOG

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEMO_LOG = os.path.join(BASE_DIR, "demo_run.log")

demo_process = None

@app.route('/')
def index():
    return send_file('dashboard.html')

@app.route('/launch', methods=['POST'])
def launch():
    global demo_process
    
    # Ensure any old log is removed before starting
    if os.path.exists(DEMO_LOG):
        try:
            os.remove(DEMO_LOG)
        except OSError:
            pass
            
    # We use python executable from the current environment
    import sys
    with open(DEMO_LOG, 'w', encoding='utf-8') as f:
        demo_process = subprocess.Popen(
            [sys.executable, "demo.py"],
            cwd=BASE_DIR,
            stdout=f,
            stderr=subprocess.STDOUT
        )
    return jsonify({'status': 'launched'})

@app.route('/reset', methods=['POST'])
def reset_demo():
    import sys
    subprocess.run([sys.executable, 'reset_env.py'])
    subprocess.run([sys.executable, 'system2_seeder.py'])
    return jsonify({'status': 'reset'})

@app.route('/file/<path:filepath>')
def serve_file(filepath):
    print(f"DEBUG serve_file: requested filepath = {filepath}")
    # Handle absolute paths pasted from terminal (Windows paths often have 'C:')
    if os.path.isabs(filepath) or ":" in filepath:
        safe_path = os.path.abspath(filepath)
    else:
        # It's a relative path clicked from the UI tree
        safe_path = os.path.abspath(os.path.join(TEST_DIR, filepath))
        
    test_dir_abs = os.path.abspath(TEST_DIR)
    print(f"DEBUG serve_file: safe_path = {safe_path}")
    print(f"DEBUG serve_file: test_dir_abs = {test_dir_abs}")
    
    # Security check: ensure path traversal doesn't escape the test environment
    if not safe_path.startswith(test_dir_abs):
        print("DEBUG serve_file: Access denied 403")
        return "Access denied", 403
        
    # 1. Try exact path requested
    if os.path.exists(safe_path):
        print("DEBUG serve_file: Exact path found.")
        return send_file(safe_path, mimetype='text/plain')
        
    # 2. Try with .locked appended (clicked in UI after it got encrypted)
    if os.path.exists(safe_path + ".locked"):
        print("DEBUG serve_file: .locked path found.")
        return send_file(safe_path + ".locked", mimetype='text/plain')
        
    # 3. Try with .locked removed (pasted from terminal but system was reset)
    if safe_path.endswith(".locked"):
        unlocked = safe_path[:-7]
        if os.path.exists(unlocked):
            print("DEBUG serve_file: unlocked path found.")
            return send_file(unlocked, mimetype='text/plain')
            
    print("DEBUG serve_file: File not found 404")
    return f"File not found. Tried safe_path: {safe_path} | test_dir_abs: {test_dir_abs}", 404

@app.route('/status')
def status():
    # 1. Determine state
    state = "idle"
    if os.path.exists(INCIDENT_LOG):
        state = "done"
    elif os.path.exists(PID_FILE):
        state = "running"
    elif os.path.exists(DEMO_LOG):
        state = "starting"

    # 2. Get file statuses
    files_state = []
    if os.path.exists(TEST_DIR):
        for root, dirs, files in os.walk(TEST_DIR):
            dirs.sort()  # ensure deterministic sort
            for f in sorted(files):
                # Ignore internal protection/keys just in case, though they shouldn't be here
                if f in ["alert.json", "incident_log.txt", "canary_registry.json", "ransomware.pid", "encryption.key"]:
                    continue
                
                rel_path = os.path.relpath(os.path.join(root, f), TEST_DIR).replace("\\", "/")
                is_locked = f.endswith(".locked")
                display_name = rel_path.replace(".locked", "")
                
                files_state.append({
                    "name": display_name,
                    "status": "encrypted" if is_locked else "safe"
                })

    # Sort files matching the exact directory walk output order
    # (Since we built it sequentially from the sorted os.walk, it's already in perfect order)

    # 3. Read log lines from the live terminal feed
    log_lines = []
    if os.path.exists(DEMO_LOG):
        try:
            with open(DEMO_LOG, 'r', encoding='utf-8') as f:
                log_lines = [line.strip() for line in f.readlines() if line.strip()]
        except Exception:
            pass

    # 4. Read final stats if done
    stats = {
        "latency": 0.0,
        "encrypted": 0,
        "saved": 0,
        "protection_rate": 0.0
    }
    
    if state == "done" and os.path.exists(INCIDENT_LOG):
        try:
            with open(INCIDENT_LOG, 'r', encoding='utf-8') as f:
                content = f.read()
                # Parse the incident log block
                for line in content.split("\n"):
                    if "Latency" in line:
                        val = line.split(":")[1].replace("sec", "").strip()
                        stats["latency"] = float(val)
                    elif "Encrypted Files" in line:
                        stats["encrypted"] = int(line.split(":")[1].strip())
                    elif "Safe Files" in line:
                        stats["saved"] = int(line.split(":")[1].strip())
                    elif "Protection Rate" in line:
                        val = line.split(":")[1].replace("%", "").strip()
                        stats["protection_rate"] = float(val)
        except Exception:
            pass

    return jsonify({
        "state": state,
        "files": files_state,
        "log_lines": log_lines,
        "stats": stats
    })

if __name__ == '__main__':
    app.run(port=5001, debug=False)
