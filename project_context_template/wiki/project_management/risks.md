# Risks

## Purpose

Project-level risk register. Append-only. One row per risk.

## Risk register

| ID | Risk | Likelihood (L/M/H) | Impact (L/M/H) | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| R-001 | TCP/payload mis-set on UR10e causes protective stop or wrong toolpath. | M | H | Verify TCP at session start. `setPayload()` after every grip change. See `ur10e_ros2_grasshopper/testing_checklist.md`. | Libish | Open |
| R-002 | Grasshopper-to-robot bridge sends mm where m is expected. | M | H | Unit assert at every bridge boundary. See `ur10e_ros2_grasshopper/grasshopper_bridge.md`. | Libish | Open |
| R-003 | Wiki and Context7 drift; assistant trusts stale wiki. | M | M | Run `/health_check_wiki` weekly. Refresh entries older than 90 days. | Libish | Open |
| R-004 | DGL deprecation strands ongoing experiments. | L | M | Maintain PyG pipeline as primary. DGL kept for comparison only. See `graphml_baseline_comparison/overview.md`. | Libish | Open |
| R-005 | Lab loses internet during a deadline; no offline workflow tested. | M | M | Pre-pull a Qwen-coder model. Cache top-10 library notes. See `local_ai_workflow/offline_workflow.md`. | Libish | Open |
| R-006 | Subagent over-delegation inflates total token cost. | L | L | Reserve subagents for naturally separable work. Pin haiku where possible. | Libish | Open |
| R-007 | WebSocket relay is exposed beyond localhost before authentication and ROS safety gates exist. | M | H | Bind to `127.0.0.1` during Level 1. Add authentication and network policy before LAN exposure. | Libish | Open |
| R-008 | A browser/rosbridge publish is mistaken for a motion-safe ROS2 command path. | M | H | Keep Level 1, Level 2, and Level 3 gates explicit. Require simulation and controller checks before motion. | Libish | Open |

## Add new risk

```markdown
| R-NNN | <one-sentence risk> | L/M/H | L/M/H | <mitigation> | <owner> | Open |
```
