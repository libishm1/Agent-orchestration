# /audit_query

Run the audit trail query tool and display the results.

## Steps

1. Run: `python audit_query.py $ARGUMENTS` from the project root.
2. Display the output verbatim.
3. If the output is empty or the file is missing, say so clearly.

## Examples

- `/audit_query` — last 10 events (summary table)
- `/audit_query --event checkpoint` — all checkpoint events
- `/audit_query --event handoff` — all handoff events
- `/audit_query --agent qwen_local` — all events from the local Qwen agent
- `/audit_query --task grasshopper_websocket_pose_pipeline` — every event for that task
- `/audit_query --file wiki/ur10e_ros2_grasshopper/websocket_pose_pipeline.md` — events that read or changed that page
- `/audit_query --since 2026-04-29` — events from a specific date onward
- `/audit_query --severity P0` — P0 health issues only
- `/audit_query --last 5 --json` — last 5 events as full JSON
- `/audit_query --count` — total number of events recorded

## Notes

- `--json` outputs full JSON objects, one per event, for programmatic use.
- `--count` is useful for a quick audit trail size check.
- Combine filters: `--event checkpoint --agent qwen_local --since 2026-04-29`.
