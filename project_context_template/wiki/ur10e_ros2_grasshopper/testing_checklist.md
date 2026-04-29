# Testing Checklist

## Purpose

Concrete pre-flight checklist to run before any motion code touches Level 2 (sim) or Level 3 (hardware). Print this. Stick it next to the pendant.

## Confirmed facts

The execution ladder is:

- **Level 1:** offline (no robot connection). Runs on the dev machine.
- **Level 2:** simulation (URSim or MoveIt2 mock hardware). Validate motion behavior here.
- **Level 3:** real hardware. Default to no.

Do not skip levels.

## Level 1 checks (offline)

- [ ] Code compiles or imports without error.
- [ ] Unit tests pass (`pytest`).
- [ ] All poses have a frame tag in the variable name (`<thing>_in_<frame>`).
- [ ] Unit assertions exist at every bridge boundary (mm vs m, rad vs deg).
- [ ] No hard-coded robot IP. Robot IP is parameterized.
- [ ] The `use_real_hardware` flag exists and defaults to `False`.
- [ ] WebSocket relay smoke test passes: `python outputs\2026-04-29\grasshopper_websocket_pose_pipeline\smoke_test.py`.
- [ ] Browser receiver displays the same pose that the sample sender transmits.
- [ ] Invalid units are rejected by the relay (`mm` must not be accepted as robot-ready translation units).

## Level 2 checks (simulation)

- [ ] URSim or MoveIt2 mock hardware is running.
- [ ] Driver connects and reports `Hardware Interface OK`.
- [ ] `ros2 control list_controllers` shows the expected controller as `active`.
- [ ] A no-op trajectory (current pose → current pose) executes successfully.
- [ ] A simple `moveL` to a nearby pose executes within ±0.1 mm of the expected target.
- [ ] Pose conversion round-trip test: Grasshopper Plane → URScript pose → back to Plane. Origin matches within 0.01 mm.
- [ ] Pose conversion round-trip with rotation: Plane with non-trivial rotation → URScript pose → back. Frame axes match within 0.01° per axis.

## Level 3 checks (hardware)

Pre-power:

- [ ] Workspace is clear of people and obstructions.
- [ ] E-stop is reachable.
- [ ] Operator wearing required PPE per lab policy.

Power-on sequence:

- [ ] Robot powered on, no protective or e-stop active.
- [ ] Robot is in **Remote Control** mode on the pendant.
- [ ] **ExternalControl URCap program is running** (for ROS2 driver path).
- [ ] Network: ping robot IP succeeds. `nc -zv <ip> 30002` and `nc -zv <ip> 30004` succeed.

Configuration:

- [ ] TCP is set to the correct value for the currently mounted tool. **Verify by jogging to a known fixture point.**
- [ ] Payload is set to RG6 + workpiece (if held), with COG.
- [ ] Safety planes on the pendant match the physical workspace.
- [ ] Speed and acceleration in the code are conservative (`speed=0.1, acceleration=0.1`) for first run.

First motion:

- [ ] First commanded motion is a small (≤ 50 mm) move from current pose, executed slowly.
- [ ] Operator's hand is on the e-stop or pendant freedrive.
- [ ] After the first motion, verify the actual TCP pose matches the commanded target within ±0.5 mm.

Gripper (RG6):

- [ ] Gripper power on (24 V).
- [ ] `setPayload()` matches gripper + held mass.
- [ ] Test grip-open and grip-close from a safe pose, no workpiece.
- [ ] Verify grip-detected register reports correctly with and without an object.

## Code or command patterns

```bash
# Quick connectivity tests
ping 192.168.1.10
nc -zv 192.168.1.10 30002
nc -zv 192.168.1.10 30004

# Check ROS2 state
ros2 control list_controllers
ros2 topic list
ros2 topic echo /joint_states --once
```

```python
# Smoke test before motion
def smoke_test(rtde_r, rtde_c):
    assert rtde_c.isConnected(), "RTDE not connected"
    assert not rtde_r.isProtectiveStopped(), "Robot in protective stop"
    assert not rtde_r.isEmergencyStopped(), "Robot in emergency stop"
    pose = rtde_r.getActualTCPPose()
    print(f"TCP in base: {pose}")
    print(f"Joint positions: {rtde_r.getActualQ()}")
```

## Risks

- **Skipping Level 2.** Untested motion code on hardware is the highest-risk action in this stack. Do not.
- **TCP not verified after a tool change.** Every motion is wrong by the offset. Verify.
- **Payload not updated after pickup.** Trips protective stops on fast moves.
- **First motion too fast.** Always start slow on hardware. Speed up only after the path is verified.

## Open questions

- Should the lab adopt a written sign-off form before any Level 3 session? Worth deciding before the next student cohort.

## Related raw files

(populate via `/ingest_raw`)

## Related wiki pages

- [Overview](overview.md)
- [Pose and frame rules](pose_frame_rules.md)
- [WebSocket pose pipeline](websocket_pose_pipeline.md)
- [ROS2 bridge](ros2_bridge.md)
- [UR10e RG6 control](ur10e_rg6_control.md)

## Last updated

2026-04-29
