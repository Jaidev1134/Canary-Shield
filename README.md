# 🛡️ Canary Shield: Real-Time Ransomware Defense

Welcome to the **Canary Shield** project! 

Whether you are a highly skilled software engineer, a 5-year-old child learning about computers, or a retired grandparent who just bought their first laptop—this document is written for **you**. 

We will explain exactly what this project does, how it works, who built it, and how you can run it on your own computer.

---

## 📖 The Story: What Does This Project Do?

Imagine your computer is a huge **Bank**, and inside this bank are millions of safe deposit boxes containing your most precious items (your photos, your passwords, your work documents). 

A **Ransomware Attack** is like a super-fast thief who breaks into the bank and starts putting unbreakable padlocks on every single box. If you want the key to unlock your boxes, the thief demands a massive amount of money (a ransom). 

Usually, the bank's security guards (traditional Antivirus) try to stop thieves by looking at their faces. But what if the thief is wearing a brand-new mask that the guards don't recognize? The thief gets right past them!

### Our Solution: The Canary Tripwire 🐦
Instead of trying to recognize the thief's face, we built **Canary Shield**. 
We placed secret, invisible "tripwires" (fake safe deposit boxes) all over the bank. The thief doesn't know which boxes are real and which are fake. The absolute millisecond the thief touches *even one* of our tripwires, a silent alarm goes off, and an automated SWAT team drops from the ceiling and instantly stops the thief before they can lock up the rest of the bank.

---

## 👥 Meet the Team & Our Roles

*Note to judges: Please replace the bracketed names with your actual team members!*

### 1. The Architect: `[Team Member 1 - e.g., Jaidev Sharma]`
**What they did:** Built the core nervous system of the project.
**Explain like I'm 5:** Jaidev built the SWAT team and the Bank's security cameras. He wrote the backend server that listens for alarms and created the incredibly beautiful, hacker-style "Dashboard" (the TV screen) where we can watch the thief get caught in real-time.

### 2. The Trap Setter: `[Team Member 2 - Amit]`
**What they did:** Built the dummy file generator and the ransomware simulator.
**Explain like I'm 5:** This person built the fake bank boxes (the 150+ dummy files) and hid the tripwires inside them. They also built the "fake thief" (the ransomware simulator) so we could safely test our security system without actually destroying our own computers.

### 3. The Guard Commander: `[Team Member 3 - Manasa]` (If applicable)
**What they did:** Developed the Watchdog Daemon and Kill Engine logic.
**Explain like I'm 5:** This person wrote the rules for the security guard. They told the guard exactly how to check the tripwires a hundred times a second, and taught the SWAT team how to accurately track down the thief and permanently stop them.

4th. atharv[integration]

---

## 🧩 How We Integrated Everything Together

Making all these pieces talk to each other was like conducting an orchestra. Here is how we connected it:

1. **The Setup:** When you click "Launch" on our dashboard, the system first calls our "Seeder" script. This instantly builds a massive maze of folders and 150+ files (our bank) and hides our tripwires inside them.
2. **The Race:** Next, we release the Thief (Ransomware) and wake up the Guard (Watchdog) at the exact same time. They run in parallel.
3. **The Connection:** The Guard uses a secret map (`canary_registry.json`) to know exactly where the tripwires are. It constantly checks them. 
4. **The Takedown:** When the Thief locks a tripwire, the Guard sees the math change (the file hash changes). It immediately shouts the Thief's ID number to the Kill Engine. The Kill Engine uses computer-level permissions to terminate the Thief.
5. **The Live TV:** While all this happens in the dark background of the computer, our Flask Server reads the action logs and streams them directly to our web browser so you can eat popcorn and watch it happen live!

---

## 🏗️ System Architecture & Tech Stack

For the tech-savvy readers, here is exactly what runs under the hood:

* **Frontend:** Vanilla HTML, CSS, and JavaScript. We used zero heavy frameworks so it runs instantly. It features a live-polling terminal feed and a dynamic DOM tree.
* **Backend:** Python `Flask`. It handles the API routes (`/launch`, `/reset`, `/status`) and safely streams locked file contents directly to the browser.
* **Cryptography:** Python's `cryptography` library (Fernet AES-128) is used to simulate military-grade ransomware encryption.
* **Integrity Monitoring:** We use `hashlib` (SHA-256) to perform high-speed cryptographic hashing of the Canary files to detect bit-level tampering.
* **Process Management:** We use Python's `psutil` and `os` libraries to track down malicious PIDs and send `SIGTERM` / `SIGKILL` escalation commands to terminate processes.

---

## 📝 The Incident Report

When the dust settles and the thief is stopped, our system automatically generates an **Incident Report**. 
This is a summary ticket that tells you exactly how much damage was done. It shows:
* **Latency:** Exactly how many milliseconds it took to catch the thief (usually less than 0.2 seconds!).
* **Files Encrypted:** How many files the thief managed to lock before getting shot down.
* **Files Saved:** How many files survived perfectly intact.
* **Protection Rate:** A percentage score (e.g., 96.5% of data saved).

---

## 🚧 Our Limitations

We are very proud of this system, but we are also honest about what it cannot do (yet):
1. **The Sacrifice:** Our system *requires* the ransomware to lock at least one or two files (the tripwires) before it knows an attack is happening. We cannot save the first file that gets attacked.
2. **User-Space Delays:** Because our watchdog runs as a normal computer program (user-space), there is a tiny millisecond delay. If the thief is unbelievably fast, they might lock 5 or 10 files before the guard catches them. To fix this, we would need to install the guard deep inside the core of the operating system (Kernel space).
3. **Smart Thieves:** A highly advanced thief might realize what a tripwire looks like and choose to skip those specific boxes. 

---

## 🚀 How to Run the Project on Your System

Follow these simple steps to watch the magic happen on your own Windows computer:

### Step 1: Install Python
If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/) and install it. Make sure to check the box that says "Add Python to PATH" during installation.

### Step 2: Open the Folder
Download this project folder and extract it to your Desktop. 

### Step 3: Install the Requirements
Open your computer's **Terminal** (Command Prompt or PowerShell), navigate to the folder, and type this command to install the required tools:
```bash
pip install -r requirements.txt
```

### Step 4: Start the Server
In that same terminal, run the server by typing:
```bash
python server.py
```
You should see a message saying `Running on http://127.0.0.1:5001`.

### Step 5: Watch the Show
1. Open your favorite web browser (Chrome, Edge, etc.).
2. Go to this exact address: `http://127.0.0.1:5001`
3. You will see the gorgeous Canary Shield Dashboard!
4. Click files on the left to see their contents.
5. Hit the glowing **LAUNCH RANSOMWARE SIMULATION** button at the bottom.
6. Watch the terminal turn red, see the files get locked, and watch the system terminate the threat and save your data!
