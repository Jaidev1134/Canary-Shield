# Canary Shield: Setup & Deployment Documentation

## Overview
This document provides step-by-step instructions to set up, configure, and run the Canary Shield project on a local Windows machine. Canary Shield is a real-time ransomware defense simulator that features a web dashboard, an automated tripwire monitor, and a safe ransomware simulation environment.

## System Requirements
- **Operating System**: Windows 10/11 (The system utilizes `psutil` and `os` specifically configured for cross-platform and Windows process management).
- **Python Version**: Python 3.8 or higher.
- **Web Browser**: Any modern browser (Chrome, Edge, Firefox) for viewing the dashboard.

## Installation Instructions

### 1. Install Python
If Python is not installed on your system:
1. Download the installer from the official [Python website](https://www.python.org/downloads/).
2. Run the installer. 
3. **Important:** Make sure to check the box that says **"Add Python to PATH"** before clicking install.

### 2. Prepare the Project Directory
1. Download or clone the Canary Shield repository.
2. Extract the contents to a designated folder (e.g., your Desktop).
3. Open your computer's Terminal (Command Prompt or PowerShell).
4. Navigate to the project directory using the `cd` command:
   ```bash
   cd path\to\canary-shield
   ```

### 3. Set Up a Virtual Environment (Optional but Recommended)
To prevent dependency conflicts, it is highly recommended to use a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
Once inside the project directory (and with your virtual environment activated), install the required Python packages using `pip`:
```bash
pip install -r requirements.txt
```
The key dependencies include:
- `flask` & `flask_cors`: For the web dashboard backend.
- `cryptography`: For the AES-128 encryption used in the ransomware simulator.
- `watchdog`: For real-time file system monitoring.
- `psutil`: For advanced process tracking and termination.
- `colorama`: For color-coded terminal output during the simulation.

## Running the Application

### 1. Start the Flask Server
The Flask backend serves the dashboard and handles the API requests to launch and reset the simulation. In your terminal, run:
```bash
python server.py
```
You should see output indicating that the server is running on `http://127.0.0.1:5001`.

### 2. Access the Dashboard
1. Open your web browser.
2. Navigate to [http://127.0.0.1:5001](http://127.0.0.1:5001).
3. You will see the Canary Shield Control Panel, featuring the live file tree and the terminal output feed.

### 3. Launch the Simulation
1. At the bottom of the dashboard, click the **"LAUNCH RANSOMWARE SIMULATION"** button.
2. The backend (`server.py`) will execute `demo.py`, which seamlessly orchestrates:
   - Setting up a fresh directory with dummy files (`system2_seeder.py`).
   - Starting the real-time defender (`canary_monitor.py`).
   - Launching the threat actor (`ransomware_sim.py`).
3. Watch the terminal output in the browser as the ransomware encrypts files and the defender catches it and terminates the process via `kill_engine.py`.

### 4. Resetting the Environment
If you wish to run the simulation again or clean up the `test_env` directory:
- Click the **"Reset Environment"** button located at the top right of the dashboard.
- This will clear the locked files, delete any incident logs, and generate a fresh file tree for the next run.

## Troubleshooting

- **"Port 5001 is already in use"**: If you get an error stating the port is bound, change the port in `server.py` at the very bottom: `app.run(port=5001, debug=False)`.
- **Packages not found**: Ensure you ran `pip install -r requirements.txt` and that you are using the correct Python environment.
- **Permission Denied during Kill Engine execution**: The script terminates user-space processes. If it fails, you may need to run your terminal as an Administrator.
