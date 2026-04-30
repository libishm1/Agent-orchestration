# UR10e ROS2-Grasshopper Reference Digest

## Purpose

Record what each cited reference contributes to the UR10e with RG6 gripper, Grasshopper, WebSocket, web receiver, and ROS2 bridge plan.

## Confirmed facts

| Reference | Status | Relevant facts | Use in this project |
|---|---|---|---|
| `websockets` PyPI and docs: https://pypi.org/project/websockets/ | Official package source. Rechecked with Context7 2026-04-30. | Current Context7 query used `websockets` 16.0 under `/python-websockets/websockets/16.0`; the package implements the WebSocket protocol for Python servers and clients. | Python relay server. |
| `websockets` asyncio server and upgrade docs: https://websockets.readthedocs.io/en/stable/reference/asyncio/server.html and https://websockets.readthedocs.io/en/stable/howto/upgrade.html | Official docs. Rechecked with Context7 2026-04-30. | Current asyncio API lives under `websockets.asyncio`; server handlers receive one `ServerConnection` argument. The old `handler(websocket, path)` pattern should be replaced with `handler(websocket)` and `websocket.request.path` if needed. | Prototype prefers current docs while retaining compatibility with locally installed `websockets` 11.0.3. |
| Bengesht Food4Rhino: https://www.food4rhino.com/en/app/bengesht | Listed source. Food4Rhino page was reachable but not text-extractable in this session. | Bengesht is the intended Grasshopper plugin source. | Installation/source pointer. |
| Bengesht GrasshopperDocs mirror: https://grasshopperdocs.com/addons/bengesht.html | Community docs mirror. Checked 2026-04-29. | Version 3.3, released 2018-11-03, 17 components. WebSocket components can send and receive data with a WebSocket server. | Grasshopper no-code sender route. |
| `roslibpy` GitHub/PyPI: https://github.com/RobotWebTools/roslibpy and https://pypi.org/project/roslibpy/ | Source repository and PyPI. Checked 2026-04-29. | Connects to rosbridge over WebSockets. ROS 1 is fully supported; ROS 2 support remains in progress. PyPI version 2.0.0 added ROS 2 action client support. | Future web-to-ROS bridge candidate, not final motion execution layer. |
| Universal Robots ROS2 Driver: https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver | Official Universal Robots repository. Checked 2026-04-30. | ROS2 driver for UR CB3, e-Series, and PolyScope X robots. Repository packages include `ur`, `ur_calibration`, `ur_controllers`, `ur_dashboard_msgs`, `ur_moveit_config`, and `ur_robot_driver`. Docs stress calibration extraction for correct TCP poses in ROS. | Authoritative ROS2 arm driver and MoveIt2 starting point. Prefer over third-party URDF mirrors for UR arm integration. |
| ABC-iRobotics OnRobot ROS2 controller: https://github.com/ABC-iRobotics/onrobot-ros2 | Community ROS2 repository. Checked 2026-04-30. | Targets OnRobot RG grippers; README says current package supports the RG series and was tested on RG6. Includes packages for Modbus TCP/IP, description, messages, controller, CLI controller, a width/height/joint calculation service, and a `GripperCommand` action server. | Candidate ROS2 RG6 control path. Evaluate in simulation or bench setup before using with robot motion. |
| Zhengxuez RG6 gripper description: https://github.com/Zhengxuez/rg6_gripper_description | Community URDF description. Checked 2026-04-30. | Provides an OnRobot RG6 URDF/Xacro description based on `fusion2urdf` and OnRobot STEP data, with meshes and RViz display launch. README notes the `g_main` fixed joint `rpy` may need updating if the adapter-to-body angle changes. | Candidate visual/collision model source for RG6. Treat frame/origin values as unverified until checked against the physical adapter and official CAD. |
| Runtime Robotics OnRobot RG2/RG6 ROS2 driver: https://github.com/runtimerobotics/onrobot_rg2_ros2 | Community ROS2 repository. Checked 2026-04-30. | README describes a ROS2 Jazzy driver for OnRobot RG2/RG6, using `pymodbus==2.5.3`, with a launch file and `/send_gripper_cmd` `std_msgs/msg/Int32` topic for values 0 to 1100. | Lightweight candidate gripper command interface for Jazzy experiments. API is simple but sparse; do not assume safety/feedback semantics without testing. |
| RhinoCommon API: https://developer.rhino3d.com/api/rhinocommon/rhino.geometry.plane | Official McNeel API docs. Checked 2026-04-29. | `Rhino.Geometry.Plane` represents an origin plus axes and exposes origin and axis properties. | Grasshopper plane to pose conversion. |
| UR10e URDF dataset: https://github.com/Daniella1/urdf_files_dataset/blob/main/urdf_files/ros-industrial/xacro_generated/universal_robots/ur_description/urdf/ur10e.urdf | Third-party generated URDF mirror. Checked 2026-04-29. | Includes standard UR joint names and `tool0`. | Frame and joint-name reference only. Prefer official UR ROS2 description for implementation. |
| Polito thesis PDF: https://webthesis.biblio.polito.it/38675/1/tesi.pdf | Downloaded to `outputs/2026-04-29/reference_cache/polito_38675_tesi.pdf`. Checked 2026-04-29. | Focuses on deep reinforcement learning for UR10e manipulation, with simulation-to-URSim-to-real deployment and ROS2 integration. | Supports the staged validation ladder: simulation and controller validation before hardware. |
| Webots URe R2022b docs: https://raw.githubusercontent.com/cyberbotics/webots/R2022b/docs/guide/ure.md | Official Cyberbotics source file. Checked 2026-04-29. | Webots includes UR3e/UR5e/UR10e models, ROS compatibility, `toolSlot`, `staticBase`, and sample worlds. | Optional Level 2 simulation reference. |
| `Robotics in UR Robots_March 2019_r1.pdf` | Local PDF provided by user. Extracted 2026-04-29. | Explains UR joint vs linear space, TCP, base/tool coordinates, rotation vectors, pose transformations, singularities, RTDE notes, and UR10e repeatability. | Pose/frame rules and safety notes. Treat as reference material, not official support. |
| `1-s2.0-S2772991525000040-main.pdf` | Local Elsevier PDF provided by user. Extracted 2026-04-29. | Construction robotics paper covering robotic arm positioning inaccuracy, fiducial marker accuracy, frame alignment, and tolerance-aware assembly. | Reinforces need for calibration, pose tolerance, and no hardware execution from unvalidated web messages. |

## Current working assumptions

- The first software milestone is transport validation, not robot control.
- Official docs and source repositories outrank mirrors and third-party datasets.
- Local PDFs are useful for project context but should not override manufacturer manuals or current API docs.

## Implementation notes

- Use Bengesht when the Grasshopper definition should stay visual and plugin-based.
- Use Rhino 8 ScriptEditor when the project needs explicit conversion code and testable JSON.
- Use browser receiving first because it exposes schema, timing, units, and frame mistakes without ROS or robot risk.
- Use `roslibpy` only after a rosbridge server is available and the target ROS topic/message type is chosen.
- Treat community OnRobot repositories as implementation candidates, not authoritative hardware references. Verify message contracts, Modbus behavior, URDF frames, and adapter offsets before integrating them into any ROS2 motion workflow.

## Code or command patterns

See [WebSocket pose pipeline](websocket_pose_pipeline.md).

## Risks

- Food4Rhino did not expose parseable text in this session. Use the listed URL for installation and the GrasshopperDocs mirror for component details.
- The URDF dataset is not the authoritative UR ROS2 driver description.
- Community RG6/RG2 ROS2 packages may lag current ROS2 distributions, OnRobot firmware, or lab hardware wiring. Pin tested commits before relying on them.
- The Polito thesis is a 2025/2026 academic reference. It supports validation strategy, not this project's exact hardware setup.

## Open questions

- Should the Webots UR10e model be used for Level 2, or should the project standardize on URSim plus MoveIt2 mock hardware?
- Should local PDFs be copied into `raw/references/` with metadata, or left at the workspace root?
- Which official UR10e manual revision should be pinned for hardware specifications?
- Which OnRobot ROS2 gripper path should be tested first: ABC-iRobotics controller, Runtime Robotics topic driver, or direct URCap/Modbus control?

## Related raw files

- `../../../../Robotics in UR Robots_March 2019_r1.pdf`
- `../../../../1-s2.0-S2772991525000040-main.pdf`
- `../../outputs/2026-04-29/reference_cache/polito_38675_tesi.pdf`

## Related wiki pages

- [WebSocket pose pipeline](websocket_pose_pipeline.md)
- [Pose and frame rules](pose_frame_rules.md)
- [Grasshopper bridge](grasshopper_bridge.md)
- [ROS2 bridge](ros2_bridge.md)

## Last updated

2026-04-30
