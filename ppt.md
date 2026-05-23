# Canary Shield: Real-Time Ransomware Defense Engine
**Hackathon Presentation Content**

---

## Slide 1: Introduction
**Title:** The Ransomware Epidemic & The Canary Approach
* **Context:** Ransomware attacks have evolved into highly automated, military-grade encryption campaigns capable of bringing entire corporate networks down in minutes.
* **The Concept:** "Canary files" are strategically placed, heavily monitored decoy files. Like a canary in a coal mine, any unauthorized modification to these files acts as an immediate, undeniable indicator of compromise.
* **Our Solution:** Canary Shield is a lightweight, zero-trust Endpoint Detection and Response (EDR) engine that uses deterministic file-integrity monitoring to instantly detect and neutralize cryptographic threats in real-time.

---

## Slide 2: Problem Statement
**Title:** The Failure of Traditional Defense Mechanisms
* **Signature Lag:** Traditional Antivirus relies on known malware signatures. Zero-day and polymorphic ransomware easily bypass these static defenses.
* **Heuristic False Positives:** Behavioral analysis tools often misidentify legitimate corporate encryption or massive file migrations as malicious, leading to alert fatigue.
* **The Speed of Attack:** Modern ransomware (like LockBit or Ryuk) can encrypt thousands of files per second. By the time traditional alerts reach a human analyst, the data is already irreparably lost.
* **Objective:** We need an automated, deterministic kill-chain that acts faster than human response times without relying on outdated malware signatures.

---

## Slide 3: Research Gaps and Challenges
**Title:** Overcoming the Detection Latency
* **Research Gap:** Many existing solutions poll the filesystem too slowly or rely on expensive kernel hooks that degrade system performance.
* **Challenge 1 (I/O Bottlenecks):** Monitoring thousands of corporate files continuously consumes massive CPU overhead.
* **Challenge 2 (Process Identification):** Accurately tracing a modified file back to the specific malicious PID (Process ID) responsible for the encryption.
* **Challenge 3 (Evasion Tactics):** Advanced ransomware attempts to kill defense monitoring tools before encrypting.
* **Our Approach:** By isolating the monitoring strictly to lightweight SHA-256 hash checks on hidden Canary files, we reduce CPU overhead by 99% while achieving sub-second detection.

---

## Slide 4: Proposed System Architecture
**Title:** Canary Shield Architecture & Flow
* **Environment Orchestrator:** Automatically seeds a massive, recursive corporate file tree with hidden `000_passwords.txt` and `AAA_crypto_keys.txt` canary decoys.
* **Watchdog Daemon:** A lightweight background process continuously polling the SHA-256 integrity of the registry of Canary files.
* **The Kill Engine:** Upon detecting cryptographic alteration (hash mismatch), the system immediately halts the environment, traces the active malicious processes, and executes an escalated `SIGTERM` → `SIGKILL` termination sequence.
* **Live SOC Dashboard:** A real-time, React-style Flask dashboard providing a live terminal feed, threat meter, and interactive file-system tree for instantaneous visibility.

---

## Slide 5: Conclusion and Future Work
**Title:** Results & The Path Forward
* **Conclusion:** Canary Shield successfully demonstrates that deterministic decoy monitoring can drastically reduce the blast radius of a zero-day ransomware attack. Our live simulation proved the Kill Engine can identify and terminate the attacker with >95% of corporate data successfully saved.
* **Future Work 1 (Kernel-Level Drivers):** Migrating the watchdog from a user-space polling daemon to a Windows/Linux Kernel Mini-Filter for absolute zero-latency I/O blocking.
* **Future Work 2 (Network Isolation):** Upgrading the Kill Engine to automatically disable the host's NIC (Network Interface Card) to prevent lateral movement across the corporate network.
* **Future Work 3 (Machine Learning):** Integrating a lightweight ML model to analyze I/O entropy to catch slow-encrypting "stealth" ransomware that attempts to avoid canary files.

---
