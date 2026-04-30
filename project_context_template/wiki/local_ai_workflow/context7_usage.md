# Context7 Usage

This page is the single source of truth for which external libraries are queried via Context7. `AGENTS.md` and `CLAUDE.md` reference this page; do not duplicate the list there.

## Purpose

Define which libraries the assistant may query through Context7 MCP, the cached library IDs for fast lookup, and the rules for when to use Context7 vs the wiki vs web search.

## Confirmed facts

- Context7 is provided by Upstash via the `@upstash/context7-mcp` package.
- Context7 supplies current external API documentation; it is not project memory.
- Context7 uses identifiers like `/upstash/context7` or `/vercel/next.js`. These IDs must be resolved before use.

## Allowed Context7 libraries

The assistant may query Context7 for any of these libraries. Update this table when adding or removing libraries.

| Library | Domain | Cached ID | Last verified |
|---|---|---|---|
| ROS2 Humble docs | Robotics | /websites/ros_en_humble | 2026-04-30 |
| ros2_control | Robotics | (resolve on first use) | |
| MoveIt2 | Robotics | (resolve on first use) | |
| ur_robot_driver | Robotics | (resolve on first use) | |
| universal_robots_ros2_description | Robotics | /universalrobots/universal_robots_ros2_description | 2026-04-30 |
| ur_rtde | Robotics | (resolve on first use) | |
| FastAPI | Web | (resolve on first use) | |
| Flask | Web | (resolve on first use) | |
| websockets (Python) | Web | /python-websockets/websockets/16.0 | 2026-04-30 |
| aiohttp WebSockets | Web | (resolve on first use) | |
| React | Web | (resolve on first use) | |
| Three.js | 3D web | (resolve on first use) | |
| urdf-loader | 3D web | (resolve on first use) | |
| Open3D | Geometry | (resolve on first use) | |
| DGL | GraphML | (resolve on first use) | |
| PyTorch Geometric (PyG) | GraphML | (resolve on first use) | |
| scikit-learn | ML | (resolve on first use) | |
| vLLM | LLM serving | (resolve on first use) | |
| llama.cpp | LLM runtime | (resolve on first use) | |
| LM Studio | LLM runtime | (resolve on first use) | |
| Ollama | LLM runtime | (resolve on first use) | |
| Claude Code | Tooling | (resolve on first use) | |
| Codex CLI | Tooling | (resolve on first use) | |
| Paper2Code | Research tooling | /going-doer/paper2code | 2026-04-30 |

## Resolution workflow

On first use of a library:

1. Call `resolve-library-id` with the library name.
2. Update the **Cached ID** column above with the returned identifier.
3. Update the **Last verified** column with today's date.
4. Future calls use the cached ID directly.

## Caching strategy

After Context7 returns a useful answer:

1. Save the relevant excerpt into `wiki/local_ai_workflow/<library>_notes.md`.
2. Record the library version and the date.
3. Future reads check the wiki page first.
4. Refresh from Context7 only if:
   - The wiki entry is older than 90 days.
   - The user reports a version bump.
   - The wiki entry contradicts current behavior.

## Fallback strategy

- If Context7 is unavailable, fall back to web search of the library's official documentation URL.
- If both are unavailable, state the uncertainty and proceed with the most recent wiki entry, marked as potentially stale.

## Fallback checks

| Date | Library/source | Reason | Result |
|---|---|---|---|
| 2026-04-29 | `websockets`, `roslibpy`, RhinoCommon, Bengesht, Webots URe | Context7 MCP was not available in the Codex session. | Official docs and source URLs were checked and summarized in `wiki/ur10e_ros2_grasshopper/reference_digest.md`. Cached Context7 IDs were not filled because no `resolve-library-id` call was available. |
| 2026-04-30 | `websockets` | Context7 MCP available. | Resolved to `/python-websockets/websockets`; queried version `16.0`; cached notes updated in `wiki/local_ai_workflow/websockets_notes.md`. |
| 2026-04-30 | ROS2 Humble docs, `universal_robots_ros2_description`, Paper2Code | User provided preferred Context7 URLs. | Cached IDs recorded for future use: `/websites/ros_en_humble`, `/universalrobots/universal_robots_ros2_description`, and `/going-doer/paper2code`. |

## When NOT to use Context7

Context7 is not project memory. Do not use it for:

- Project history.
- Personal decisions.
- Raw experiment notes.
- Local implementation choices.
- Paper-specific claims, unless the claim is about library or API usage.

For these, read the wiki.

## Risks

- Context7 results can lag the latest library release. Always check the version in the response.
- Some libraries (especially community packages like `ur_rtde`) may have sparse Context7 coverage. Fall back to the official docs.
- Caching stale answers in the wiki defeats the purpose. Run `/health_check_wiki` periodically to flag entries older than 90 days.

## Open questions

- Should `wiki/local_ai_workflow/<library>_notes.md` files be templated to a common schema (version, last verified, key API patterns, common errors)?

## Related wiki pages

- [Codex setup](codex_setup.md)
- [Claude Code setup](claude_code_setup.md)
- [Local models](local_models.md)
- [Offline workflow](offline_workflow.md)

## Last updated

2026-04-30
