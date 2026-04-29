# UR10e RG6 Control

## Purpose

How to command the UR10e arm and the RG6 gripper together. Synchronization, payload updates, and the trade-offs between control paths.

## Confirmed facts

- The RG6 mounts on the UR10e tool flange via the OnRobot Quick Changer.
- RG6 has three documented control paths on UR:
  1. **URCap on the teach pendant.** PolyScope program calls into the OnRobot URCap. Native to the controller.
  2. **`ur_rtde` Modbus interface.** Read/write Modbus registers exposed by the URCap.
  3. **OnRobot Compute Box.** External controller, Modbus or ROS2 driver. Required for some non-UR robots; optional for UR.
- RG6 mass: 1.25 kg. **Must be added to the configured payload** via `set_payload()` or the pendant.
- Force programmable in the range 25–120 N. Stroke programmable up to 150 mm.
- TCP must be set to include the RG6 fingertip offset. See [pose_frame_rules](pose_frame_rules.md).

## Current working assumptions

- Default control path: URCap on the pendant for setup, `ur_rtde` Modbus for runtime control from Python.
- Stable Modbus registers for grip width and force are documented in the OnRobot URCap manual. Verify register addresses against the firmware version installed on the lab gripper.

## Implementation notes

- After picking up a workpiece, update the payload: `rtde_c.setPayload(rg6_mass + workpiece_mass, [cog_x, cog_y, cog_z])`.
- After releasing, restore the payload to the gripper-only value.
- Open/close commands take time to complete. Either poll the grip-detection register or `time.sleep()` for the worst-case actuation time.
- `width_measure` reports the actual grip width, useful for verifying the part shape after grip.

## Code or command patterns

```python
# ur_rtde + Modbus example (verify register addresses against your firmware)
from rtde_control import RTDEControlInterface
from rtde_io import RTDEIOInterface

robot_ip = "192.168.1.10"
rtde_c = RTDEControlInterface(robot_ip)
rtde_io = RTDEIOInterface(robot_ip)

# Set TCP and payload for RG6 only
rtde_c.setTcp([0.0, 0.0, 0.159, 0.0, 0.0, 0.0])  # VERIFY offset for your install
rtde_c.setPayload(1.25, [0.0, 0.0, 0.06])         # 1.25 kg, COG approx 60 mm out

# Command grip width and force via Modbus (placeholder addresses)
# Check the OnRobot URCap manual for the actual registers on your firmware.
WIDTH_REG = 12345  # placeholder — verify
FORCE_REG = 12346  # placeholder — verify
rtde_io.setStandardDigitalOut(WIDTH_REG, target_width_mm)
rtde_io.setStandardDigitalOut(FORCE_REG, target_force_n)

# After picking up a 2 kg part, update payload
rtde_c.setPayload(1.25 + 2.0, [0.0, 0.0, 0.06])
```

```urscript
# URScript path — using the OnRobot URCap function calls
rg6_grip(width=80, force=40, payload=1.25, depth_compensation=False)
movej(WP_pickup, a=0.5, v=0.1)
rg6_grip(width=40, force=80, payload=3.25, depth_compensation=False)  # post-grip payload
movel(WP_place, a=0.5, v=0.1)
rg6_release()
```

## Risks

- **Wrong payload after pickup.** Causes protective stops on accelerations. Always update.
- **Modbus register drift between firmware versions.** Re-verify after any URCap update.
- **Grip not completed before motion.** Polling grip-detected registers is more reliable than `time.sleep()`.
- **Custom fingertips change the TCP.** Update `setTcp()` whenever fingertips change.

## Open questions

- Are the lab's RG6 firmware version and Modbus register map documented? If not, run `/ingest_raw` after taking notes from the URCap manual on the pendant.
- Is depth compensation needed for the current fabrication tasks, or only for pick-and-place from a flat surface?

## Related raw files

(populate via `/ingest_raw`)

## Related wiki pages

- [Overview](overview.md)
- [Pose and frame rules](pose_frame_rules.md)
- [ROS2 bridge](ros2_bridge.md)
- [Testing checklist](testing_checklist.md)

## Last updated

2026-04-29
