# Canary Shield: Code Architecture & Comments Documentation

## System Architecture Overview

Canary Shield is built on a modular, event-driven architecture designed to simulate and detect ransomware in real-time. The system splits the attacker (ransomware) and the defender (canary monitor & kill engine) into separate processes that run concurrently, while a Flask backend streams the events to a frontend UI for observation.

The system is composed of several core layers:
1. **Frontend / UI Layer:** Vanilla HTML, CSS, JS (`dashboard.html`).
2. **Backend / API Layer:** Python Flask Server (`server.py`).
3. **Simulation Orchestrator:** Environment initialization and demo runner (`demo.py`, `reset_env.py`, `system2_seeder.py`).
4. **Attacker Module:** Ransomware simulation using AES cryptography (`ransomware_sim.py`).
5. **Defender Module:** High-speed real-time file system watchdog and termination engine (`canary_monitor.py`, `kill_engine.py`).

---

## Core Modules & Functionality

### 1. `server.py` (Backend API & Log Streaming)
This module acts as the bridge between the Python simulation and the web dashboard.
- **Framework:** `Flask` with `Flask-CORS`.
- **Key Responsibilities:**
  - **Serving the UI:** Delivers the `dashboard.html` to the user via the `/` route.
  - **Process Management:** Exposes `/launch` to trigger `demo.py` as a background subprocess and `/reset` to execute `reset_env.py`.
  - **File Serving (`/file/<path>`):** Implements a secure path-traversal resistant file server that allows the UI to read the contents of files inside the `test_env/` directory, including both safe and `.locked` files.
  - **State Polling (`/status`):** Continuously reads `demo_run.log` and the directory structure to supply the dashboard with live terminal feeds, file states, and final incident statistics.

### 2. `canary_monitor.py` (The EDR / Watchdog)
This script is the heart of the detection system, acting as a background daemon.
- **Framework:** `watchdog` library for OS-level file events, `psutil` for process scanning.
- **Key Responsibilities:**
  - **Real-Time Observation:** Uses `watchdog.observers.Observer` to monitor directories containing canary files without polling, minimizing CPU overhead.
  - **Hash Validation:** Implements `sha256_of_file()` to immediately calculate the cryptographic hash of a file when it gets touched, comparing it to the expected state.
  - **Process Enrichment:** Features `collect_suspect_processes()` which scans `psutil` open file handles to correlate a file system event with the offending process ID.
  - **Alerting & Escalation:** When a canary file is modified (hash mismatch), it generates a structured JSON alert and immediately imports and executes `trigger_kill()` from the `kill_engine.py` module.

### 3. `kill_engine.py` (The Mitigation & Response Engine)
The EDR response module triggered the moment a threat is identified.
- **Key Responsibilities:**
  - **Rapid Termination:** Reads the suspect PID and uses `psutil.Process.terminate()` (with a fallback to `SIGKILL`) to instantly stop the ransomware.
  - **Damage Assessment:** Executes `scan_environment()` to recursively walk the file system and calculate the exact number of encrypted versus safe files.
  - **Latency Measurement:** Calculates the exact time difference between canary detection (`T1`) and process termination (`T2`) to derive the system's reaction latency (typically sub-second).
  - **Incident Reporting:** Uses `colorama` to generate a beautiful, color-coded terminal incident report and writes a persistent summary to `incident_log.txt`.

### 4. `ransomware_sim.py` (The Threat Actor)
A benign simulation of a severe cryptographic attack.
- **Framework:** `cryptography.fernet` (AES-128 encryption).
- **Key Responsibilities:**
  - **Process Registration:** Records its own PID into `ransomware.pid` so the simulation knows what to track.
  - **File Traversal & Encryption:** Uses `os.walk` to find files and encrypts them using a dynamically generated key. 
  - **Extortion:** Appends a ransom banner to the encrypted data, drops a `README_DECRYPT.txt` note, and changes the file extension to `.locked`.
  - **Delay Mechanism:** Incorporates an artificial delay (default 300ms) between file encryptions to allow the demo to be observable by human eyes.

### 5. Utilities
- **`config.py`**: A central repository for environment constants (paths to `test_env`, `PID_FILE`, `INCIDENT_LOG`, etc.) to prevent hardcoded paths.
- **`system2_seeder.py`**: Dynamically generates the mock file system (the "Bank") with hundreds of files and explicitly places the hidden canary files (the "tripwires") mapped into `canary_registry.json`.
- **`demo.py`**: The main orchestrator that sequentially kicks off the seeder, starts the canary monitor, waits for it to arm, and finally launches the ransomware simulator in parallel.
- **`reset_env.py`**: Clears out the `test_env/` directory to ensure idempotency between runs.

---

## Code Quality & Documentation Comments
The system utilizes strong engineering practices:
- **Typing:** `canary_monitor.py` makes heavy use of Python's `typing` module (e.g., `tuple[Path, ...]`, `dict[str, Any]`) to ensure strict data validation.
- **Platform Agnosticism:** Operations utilize `pathlib.Path` and `os.path` ensuring compatibility across Windows and POSIX systems.
- **Error Handling:** Graceful fallbacks exist for situations where processes terminate unexpectedly or file access is denied (e.g., `psutil.AccessDenied` captures).
- **Security Engineering:** The `/file/` endpoint in `server.py` implements path sanitization to prevent unauthorized Local File Inclusion (LFI) outside the `test_env` directory.
