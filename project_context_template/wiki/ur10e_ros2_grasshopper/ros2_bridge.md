# ROS2 Bridge

## Purpose

How ROS2 connects to the UR10e and how external clients (Grasshopper, web viewers) talk to ROS2.

## Confirmed facts

- Official driver: `ur_robot_driver` from Universal_Robots_ROS2_Driver. ROS2 v2.x branch matches the active distro (Humble or Jazzy).
- Official UR ROS2 driver source: https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver. The repository includes `ur_robot_driver`, `ur_controllers`, `ur_calibration`, `ur_dashboard_msgs`, `ur_moveit_config`, and the `ur` metapackage.
- The driver requires the **ExternalControl URCap** to be installed and the corresponding program running on the teach pendant before the dev machine takes control.
- Default ports used by the driver: 50001 (reverse interface), 50002 (script sender), 50003 (trajectory). These are forwarded from the dev machine to the robot controller.
- MoveIt2 config for the UR family is provided by `ur_moveit_config`. Do not regenerate from the Setup Assistant unless the URDF has changed.
- ROS2 controllers available: `scaled_joint_trajectory_controller` (default), `joint_trajectory_controller`, `forward_position_controller`, `forward_velocity_controller`, `passthrough_trajectory_controller`. Verify with `ros2 control list_controllers`.
- `roslibpy` connects to ROS through rosbridge over WebSockets. It is useful for web/Rhino experiments, but the package still marks ROS2 support as in progress. Use it as an integration experiment, not as the final ROS2 motion-control abstraction.

## Current working assumptions

- Project targets ROS2 Humble (Ubuntu 22.04, Python 3.10). Move to Jazzy (Ubuntu 24.04, Python 3.12) is open.
- DDS implementation: rmw_cyclonedds_cpp. CycloneDDS handles unicast peers reliably; FastDDS has had multicast issues on some lab networks.
- Dev machine and robot controller are on the same `ROS_DOMAIN_ID`.
- First ROS-facing version of the WebSocket pose pipeline publishes a pose target only. It does not call MoveIt2 or send a trajectory until Level 2 simulation checks pass.

## Implementation notes

- Launch sequence: bring up the driver, start ExternalControl on the pendant, switch the active controller, then send trajectories.
- For mock hardware: `use_mock_hardware:=true` in the driver launch. No real robot needed.
- For URSim: run in Docker, expose ports 30001-30004 and 50001-50003. Driver connects to URSim's IP on the host network.
- For browser/Grasshopper to ROS experiments, two bridge choices remain open: a native `rclpy` node that subscribes to the local WebSocket relay and publishes `geometry_msgs/PoseStamped`, or a `roslibpy` client that publishes through rosbridge on port 9090.
- For RG6 gripper ROS2 integration, community candidates are:
  - `ABC-iRobotics/onrobot-ros2`: RG2/RG6 controller packages with Modbus TCP/IP, messages, description, CLI, service, and `GripperCommand` action server.
  - `runtimerobotics/onrobot_rg2_ros2`: ROS2 Jazzy RG2/RG6 driver using a simple `/send_gripper_cmd` `std_msgs/msg/Int32` command topic.
  - `Zhengxuez/rg6_gripper_description`: RG6 URDF/Xacro and meshes for visualization/modeling.

## Code or command patterns

```bash
# Bring up the driver against a real robot
ros2 launch ur_robot_driver ur_control.launch.py \
  ur_type:=ur10e \
  robot_ip:=192.168.1.10 \
  launch_rviz:=true

# Bring up against URSim
ros2 launch ur_robot_driver ur_control.launch.py \
  ur_type:=ur10e \
  robot_ip:=127.0.0.1 \
  use_mock_hardware:=false \
  launch_rviz:=true

# Bring up MoveIt2
ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur10e launch_rviz:=true

# Verify controller state
ros2 control list_controllers

# Switch controllers
ros2 control switch_controllers \
  --activate scaled_joint_trajectory_controller \
  --deactivate forward_position_controller
```

```bash
# Future rosbridge experiment, not a robot motion command
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

```powershell
# Future Python side, after roslibpy is installed and ROS bridge is running
python outputs\2026-04-29\grasshopper_websocket_pose_pipeline\roslibpy_pose_publisher_stub.py `
  --topic /grasshopper/target_pose
```

## Risks

- **QoS mismatch.** Publisher and subscriber must agree on QoS profile. `ur_robot_driver` uses default profiles; custom nodes must match.
- **Velocity safety gate.** ROS2 commands can be sent fast enough to violate safety limits. A rate-limiting node between command source and driver is a useful precaution. Software, not safety-rated.
- **Driver version drift.** `ur_robot_driver` updates can change topic names or controller defaults. Pin the version in `package.xml` and record the version in this page.
- **Community gripper driver drift.** OnRobot community ROS2 packages may not match the lab's ROS2 distro, firmware, Compute Box setup, or safety expectations. Pin commits and bench-test before use.
- **Gripper description frame mismatch.** Community RG6 URDF origins and adapter rotations must be checked against the physical quick changer and TCP calibration.
- **URCap not running.** The ExternalControl program must be running on the pendant. If not, the driver connects but no motion executes.
- **rosbridge ambiguity.** A successful rosbridge publish does not mean MoveIt2 or `ur_robot_driver` will accept or execute the target.
- **ROS2 support gap in roslibpy.** Confirm exact ROS2 message/action behavior before relying on it. Native `rclpy` may be cleaner for the production bridge.

## Open questions

- Pin a tested commit of `ur_robot_driver` once the lab setup is stable.
- Decide on a velocity gate rate (Hz) for the lab safety policy.
- Decide whether the first ROS bridge target is `geometry_msgs/PoseStamped`, a trajectory action, or a custom checked command message.
- Decide which RG6 ROS2 candidate to evaluate first: `ABC-iRobotics/onrobot-ros2`, `runtimerobotics/onrobot_rg2_ros2`, or a direct URCap/Modbus implementation.

## Related raw files

(populate via `/ingest_raw`)

## Related wiki pages

- [Overview](overview.md)
- [Architecture](architecture.md)
- [Pose and frame rules](pose_frame_rules.md)
- [WebSocket pose pipeline](websocket_pose_pipeline.md)
- [Testing checklist](testing_checklist.md)

## Last updated

2026-04-30
