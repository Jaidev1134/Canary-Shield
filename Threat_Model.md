# Canary Shield: Threat Model & Security Analysis

## 1. Introduction
This document outlines the threat model for the **Canary Shield** system. It details the adversarial capabilities being simulated, the defense mechanisms implemented to counter them, the system's inherent limitations, and potential attack vectors against the defense system itself.

## 2. Adversary Profile: The Ransomware Actor
The system models a destructive, financially motivated threat actor operating post-exploitation.
- **Goal:** Deny availability to user data by encrypting files and extorting the user for decryption keys.
- **Capabilities:**
  - Has already achieved Code Execution (CE) in user-space.
  - Possesses read/write permissions matching the compromised user account.
  - Utilizes strong cryptography (simulated via `cryptography.fernet` AES-128) ensuring data cannot be recovered without the key.
- **Behavioral Footprint (Simulated via `ransomware_sim.py`):**
  - Sequential directory traversal (`os.walk`).
  - Rapid, iterative file modification.
  - Appends distinctive extensions (`.locked`) and drops ransom notes (`README_DECRYPT.txt`).

## 3. Defense Mechanism: The Canary Tripwire
Canary Shield abandons traditional signature-based detection (which fails against zero-day or heavily obfuscated malware) in favor of **Behavioral & Decoy-based Detection**.

### 3.1. The Honey-Tokens (Canary Files)
- **Concept:** The system (`system2_seeder.py`) seeds the environment with dummy files that look identical to high-value user data (e.g., `financial_records.pdf`, `passwords.txt`).
- **Placement:** Canaries are distributed strategically across the directory tree to maximize the statistical probability that a ransomware traversal algorithm will hit them early in the attack chain.

### 3.2. Detection Engine (`canary_monitor.py`)
- **Real-Time Monitoring:** Utilizes OS-level interrupts (via `watchdog`) to monitor the exact inodes/paths of the canary files.
- **Integrity Verification:** If a canary file is touched, the system calculates its SHA-256 hash. If the hash deviates from the known baseline (`canary_registry.json`), an alert is triggered instantly.
- **Process Correlation:** The system attempts to scan open file handles using `psutil` to correlate the malicious file write with a specific Process ID (PID).

### 3.3. Mitigation & Response (`kill_engine.py`)
- **Automated Takedown:** Upon receiving an alert, the engine forcefully terminates the offending PID using a `SIGTERM` followed by an escalating `SIGKILL`.
- **Damage Limitation:** The objective is not prevention (the system acknowledges that the canary and potentially a few other files *will* be encrypted), but rather extreme mitigation, stopping the attack before it can spread to the remaining 99% of the file system.

## 4. System Limitations & Known Bypasses
While highly effective against aggressive, automated encryption loops, the system acknowledges the following limitations:

### 4.1. The "Sacrificial" Constraint
- The system fundamentally requires the ransomware to successfully encrypt at least one canary file to trigger the alarm. Therefore, 100% protection is theoretically impossible; there will always be a small degree of data loss (the "sacrificial" files).

### 4.2. User-Space Latency (Race Conditions)
- Because `canary_monitor.py` runs in user-space rather than as a Kernel-mode driver, there is a microsecond to millisecond delay between the file modification event and the execution of the `kill` command. Extremely fast, multi-threaded ransomware might successfully encrypt several real files during this latency window.

### 4.3. Smart/Evasive Ransomware
- **Canary Evasion:** Advanced ransomware could be programmed to look for specific traits of canary files (e.g., specific file sizes, entropy levels, or hidden attributes) and intentionally skip them.
- **Process Hiding:** If the ransomware utilizes rootkit capabilities to hide its PID or unlinks its file handles quickly, `collect_suspect_processes()` may fail to identify the correct PID to terminate.

## 5. Potential Attacks Against the Defense System
To maintain integrity, the defense system itself must be protected from the adversary:
1. **Denial of Service (Killing the Monitor):** If the ransomware has elevated privileges, it could simply terminate `canary_monitor.py` before beginning its encryption routine.
   - *Mitigation:* In a production environment, the monitor would need to run as `SYSTEM` or be protected by an Anti-Malware Early Launch (ELAM) driver to prevent user-space termination.
2. **Configuration Tampering:** Modifying `canary_registry.json` to blind the monitor.
   - *Mitigation:* The registry and configuration files must have strict read-only permissions enforced at the OS level.
