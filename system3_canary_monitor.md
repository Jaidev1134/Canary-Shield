# System 3: Canary Watchdog Monitor

This part watches canary files in real time and emits critical alerts when any
canary is opened, modified, moved, deleted, or recreated.

## Responsibility

System 3 does detection only:

- Load canary paths from the seeder manifest or CLI.
- Watch parent directories with `watchdog`.
- Detect canary file events quickly.
- Write structured alert JSON into `alerts/`.
- Verify current canary hash against System 2's seeded SHA-256 when possible.
- Add best-effort suspect process details using `psutil`.

System 4 should read the alert JSON and perform process kill, user alerting, and
recovery measurement.

## Install

```powershell
pip install -r requirements.txt
```

## Run

Preferred flow with System 2:

1. Run `system2_seeder.py`.
2. Keep that seeder terminal open so its locked trap file stays locked.
3. Start System 3 from the same repo/root folder:

```powershell
python -m defense.canary_monitor --manifest canary_config.json --stdout-alerts
```

If `--manifest` is omitted, System 3 automatically looks for:

- `canary_config.json`
- `canaries.json`
- `canary_manifest.json`
- `config/canaries.json`
- `configs/canaries.json`

The monitor accepts the upgraded System 2 manifest format:

```json
{
  "target_directory": "C:\\path\\to\\Safe_Target_Folder",
  "canary_files": {
    "Safe_Target_Folder/000_passwords.txt": {
      "path": "C:\\path\\to\\Safe_Target_Folder\\000_passwords.txt",
      "sha256": "..."
    }
  }
}
```

You can also pass files directly:

```powershell
python -m defense.canary_monitor --canary test_directory/.canary_DO_NOT_TOUCH.txt --stdout-alerts
```

## Alert Contract

Each detection creates a JSON file in `alerts/`.

Important fields:

- `alert_type`: always `canary_file_touched`
- `severity`: `critical`
- `event_type`: watchdog event such as `opened`, `modified`, `deleted`, or `moved`
- `canary_path`: absolute path of the canary
- `registry_key`: key from System 2's `canary_files` registry
- `expected_sha256`: seeded hash from System 2
- `current_sha256`: hash at detection time, or `null` if the file is gone
- `hash_matches_manifest`: `true`, `false`, or `null`
- `suspect_processes`: best-effort process list from open files
- `recommended_action`: handoff instruction for System 4

Pure read/open events depend on the operating system backend. Modification,
delete, move, and rename events are detected reliably by `watchdog` on Windows
ReadDirectoryChangesW and Linux inotify.
