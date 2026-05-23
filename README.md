Ransomware Early-Warning System using Canary Files

Overview

This project demonstrates a ransomware detection and prevention system using canary files and real-time file monitoring.

The system contains two main components:

1. Ransomware Simulator
    * Simulates ransomware behavior
    * Enumerates files in a target directory
    * Encrypts files using AES encryption
2. Canary-Based Defense System
    * Places hidden canary files in monitored directories
    * Detects unauthorized access/modification
    * Immediately kills the malicious encryption process
    * Sends alerts within 2 seconds
    * Preserves remaining unencrypted files

This project is designed for educational and defensive cybersecurity research purposes only.

⸻

MITRE ATT&CK Mapping
Technique

ID

Data Encrypted for Impact

T1486
Features

Ransomware Simulator

* Recursive file enumeration
* AES file encryption
* Simulated ransomware extension renaming
* Multi-threaded encryption
* Logging of encrypted files

Canary Defense Daemon

* Hidden canary file generation
* Real-time file monitoring
* Instant alert generation
* Process identification
* Automatic malicious process termination
* File integrity verification

Additional Features

* Docker-based isolated environment
* Recovery statistics
* Encryption timing metrics
* Detection latency measurement
* Safe test directory execution

⸻

Project Architecture
                    +----------------------+
                    |   Target Directory   |
                    +----------------------+
                               |
             ----------------------------------------
             |                                      |
             v                                      v

+-----------------------+          +-----------------------------+
| Ransomware Simulator  |          | Canary Monitoring Daemon    |
|-----------------------|          |-----------------------------|
| Enumerates files      |          | Watches canary files        |
| AES Encrypts files    |          | Detects modifications       |
| Renames extensions    |          | Sends alerts                |
| Simulates attack      |          | Kills malicious process     |
+-----------------------+          +-----------------------------+
                                                |
                                                v
                                  +-----------------------------+
                                  |  Remaining Files Preserved  |
                                  +-----------------------------+
                      Tech Stack

Programming Language

* Python 3.10+

Libraries

* cryptography
* watchdog
* psutil

Monitoring Tools

* Linux inotify
* Windows ReadDirectoryChangesW
* Wazuh FIM

Environment

* Docker

⸻

Folder Structure
