import os

# anchor everything to the directory config.py lives in
_BASE = os.path.dirname(os.path.abspath(__file__))

TEST_DIR        = os.path.join(_BASE, "test_env", "files")
PID_FILE        = os.path.join(_BASE, "test_env", "ransomware.pid")
KEY_FILE        = os.path.join(_BASE, "test_env", "encryption.key")
CANARY_REGISTRY = os.path.join(_BASE, "test_env", "canary_registry.json")
ALERT_FILE      = os.path.join(_BASE, "test_env", "alert.json")
INCIDENT_LOG    = os.path.join(_BASE, "test_env", "incident_log.txt")
