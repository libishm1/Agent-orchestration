# Pose and Frame Rules

This page is the gold-standard reference for how poses and frames are handled across UR10e + RG6 + ROS2 + Grasshopper. Pose conversion errors are the single most common source of bugs in this stack. This page exists to prevent them.

This page is also the **example of what a good wiki page looks like**. New pages should aim for this level of structure, citation, and clarity.

## Purpose

Define every coordinate frame used in the UR10e + RG6 + ROS2 + Grasshopper pipeline. State the conversion rules between them. Lock down units, rotation conventions, and the difference between a TCP pose and a motion-target pose. Provide copy-pasteable conversion patterns.

## Confirmed facts

### Hardware specifications

These are pulled from official datasheets. Last verified 2026-04-29.

- **UR10e payload:** 12.5 kg.
- **UR10e reach:** 1300 mm from base joint to wrist 3 axis.
- **UR10e pose repeatability:** ±0.05 mm per ISO 9283.
- **UR10e maximum TCP speed:** 1 m/s typical, 4 m/s peak.
- **UR10e joint range:** ±360° on every joint.
- **RG6 force-fit payload:** 6 kg.
- **RG6 form-fit payload:** 10 kg.
- **RG6 stroke:** 150 mm (adjustable).
- **RG6 gripping force:** 25–120 N (programmable).
- **RG6 mass:** 1.25 kg. This must be added to the configured payload on the teach pendant or via `set_payload()`.
- **RG6 dimensions:** 262 × 212 × 42 mm.

### Coordinate frames

The pipeline uses the following named frames. Always use these names. Do not invent synonyms.

| Frame | Origin | Convention | Notes |
|---|---|---|---|
| `base` | UR10e base joint center | Right-handed, +Z up | The robot's native frame. URScript reports poses here unless told otherwise. |
| `flange` | Tool flange face center | Right-handed, +Z out of the flange | The mechanical end of the arm, before any tool. Sometimes called `tool0` in ROS. |
| `tcp` | Working tip of the mounted tool | Right-handed, +Z out of the tool | Defined by the user via `set_tcp(p[x,y,z,rx,ry,rz])`. **For RG6 with standard fingertips, the TCP offset must be measured per installation.** Do not assume a fixed value. |
| `world` | User-defined fixed frame | Right-handed | The fabrication workspace. Rhino model space typically maps here. |
| `feature` | Workpiece-attached frame | Right-handed | A user-defined feature plane (e.g. table corner, workpiece origin). Used for `movej_p` with feature argument. |

Within ROS2 / `ur_robot_driver` the same frames exist with conventional names: `base_link`, `tool0`, `tcp` (when configured), `world`. The ROS2 TF tree mirrors this hierarchy.

### Units

- **Translation in URScript and `ur_rtde`:** meters. Always.
- **Rotation in URScript and `ur_rtde`:** radians. Axis-angle rotation vector format.
- **Translation in ROS2 (`geometry_msgs/Pose`):** meters.
- **Rotation in ROS2 (`geometry_msgs/Pose.orientation`):** quaternion.
- **Translation in Grasshopper (Rhino):** project document units. Default is **millimeters** in this project. Convert at the bridge boundary.
- **Rotation in Grasshopper:** typically a `Plane` (origin + X axis + Y axis vectors), not Euler. Convert at the bridge boundary.

This is the most common error source. **Grasshopper uses millimeters; URScript uses meters. Multiply or divide by 1000 at the bridge.**

### Rotation conventions

UR10e native: **axis-angle rotation vector** `(rx, ry, rz)`.

- The vector's direction is the rotation axis (a unit vector after normalization).
- The vector's magnitude `θ = sqrt(rx² + ry² + rz²)` is the rotation angle in radians.
- A pose `p[0, 0, 0.5, 0, 0, π]` means: 500 mm above base, rotated 180° around the Z axis.

ROS2 native: **quaternion** `(x, y, z, w)`.

Grasshopper native: **plane** (`origin`, `x_axis`, `y_axis`). The `z_axis` is implicit as the cross product.

Conversion is required at every bridge boundary. There are no shortcuts.

## Current working assumptions

- The Rhino document for fabrication uses **millimeters** as document units. Verify with `Rhino.RhinoDoc.ActiveDoc.ModelUnitSystem` before any export.
- The TCP for the RG6 is measured per setup. Default placeholder used in code: `tcp_offset_z = 0.159 m` (159 mm), but this is a stub. **Verify by jogging to a known point and reading the pose.**
- The fabrication world frame is aligned with the UR10e base frame for the current setup. If the robot is moved, this assumption breaks.
- Wrist rotation has no preferred sign. Trajectories that minimize wrist 3 travel are preferred but not enforced.

## Implementation notes

### When to apply the TCP

`set_tcp()` (URScript) or `setTcp()` (ur_rtde) defines an offset from the flange to the working tip.

Once set:
- `get_actual_tcp_pose()` returns the TCP pose in base frame.
- `movel(p[...])` interprets the target as a TCP pose in base frame.
- The previous TCP setting persists until overridden.

If the TCP is wrong, every motion is wrong by the same offset. Check the TCP at session start, every time.

### TCP pose vs motion pose: the most common bug

A *TCP pose* is the current measured pose of the tool tip:
```python
current = rtde_r.getActualTCPPose()  # base frame
```

A *motion pose* is a target you pass to a motion command:
```python
target = [0.4, 0.2, 0.3, 0, math.pi, 0]
rtde_c.moveL(target, speed=0.1, acceleration=0.1)  # base frame
```

Both look like `[x, y, z, rx, ry, rz]`. They are not interchangeable.

Common mistakes:
- Reading `getActualTCPPose()`, applying a small delta, then sending it back as a target. The math has to account for axis-angle composition, not a vector add. For axis-angle, **rotation components do not add linearly**.
- Computing a target in the flange frame and sending it as a TCP target without applying the inverse TCP offset.
- Mixing a base-frame target with a feature-frame motion command.

Rule: every pose in the codebase carries a frame tag in its variable name or a comment. Examples: `tcp_in_base`, `target_in_feature`, `flange_in_world`. **Untyped poses are bugs waiting to happen.**

### Composing rotations

Do not add axis-angle components to compose rotations. Convert to rotation matrix or quaternion, multiply, convert back.

In `ur_rtde` this is provided:
```python
from ur_rtde import rtde_control
import numpy as np
from scipy.spatial.transform import Rotation as R

rtde_c = rtde_control.RTDEControlInterface("192.168.1.10")

# Get current TCP pose
current = rtde_c.getActualTCPPose()  # [x,y,z, rx,ry,rz]

# Add a 90° rotation around base Z to the current orientation
delta_rotvec = np.array([0, 0, np.pi/2])
current_rot = R.from_rotvec(current[3:])
delta_rot = R.from_rotvec(delta_rotvec)
new_rot = (delta_rot * current_rot).as_rotvec()  # base-frame rotation applied first

target = list(current[:3]) + list(new_rot)
rtde_c.moveL(target, 0.1, 0.1)
```

If `delta_rot` should be applied in the *tool frame* instead of the *base frame*, the order is `current_rot * delta_rot` instead.

### Grasshopper → URScript conversion

```python
# Inside Grasshopper ScriptEditor (Rhino 8 CPython 3)
import Rhino.Geometry as rg
import math

def plane_to_urscript_pose(plane: rg.Plane, units_mm: bool = True) -> str:
    """Convert a Rhino Plane to a URScript pose literal.

    Args:
        plane: Rhino plane in document units.
        units_mm: True if document units are millimeters. Translation
            is divided by 1000. False means document is already in meters.

    Returns:
        URScript pose literal: 'p[x,y,z,rx,ry,rz]' in meters and radians.
    """
    scale = 0.001 if units_mm else 1.0
    x, y, z = plane.OriginX * scale, plane.OriginY * scale, plane.OriginZ * scale

    # Build rotation matrix from plane's X and Y axes
    xv = plane.XAxis
    yv = plane.YAxis
    zv = rg.Vector3d.CrossProduct(xv, yv)

    # Convert to axis-angle (rotation vector)
    # See scipy.spatial.transform.Rotation.from_matrix in CPython 3
    import numpy as np
    from scipy.spatial.transform import Rotation as R
    M = np.array([
        [xv.X, yv.X, zv.X],
        [xv.Y, yv.Y, zv.Y],
        [xv.Z, yv.Z, zv.Z],
    ])
    rv = R.from_matrix(M).as_rotvec()
    rx, ry, rz = rv[0], rv[1], rv[2]

    return f"p[{x:.6f},{y:.6f},{z:.6f},{rx:.6f},{ry:.6f},{rz:.6f}]"
```

This requires CPython 3 (Rhino 8 ScriptEditor). **It will not run in legacy GHPython** because IronPython 2.7 has no scipy and no f-strings. For legacy GHPython, hand-roll the matrix-to-rotation-vector math.

### URScript waypoint preservation rule

When generating URScript with multiple waypoints, the format must be:

```urscript
global WP_1 = p[0.4, 0.2, 0.3, 0, 3.14159, 0]
global WP_2 = p[0.4, 0.3, 0.3, 0, 3.14159, 0]
global WP_3 = p[0.5, 0.3, 0.3, 0, 3.14159, 0]

movel(WP_1, a=0.5, v=0.1)
movel(WP_2, a=0.5, v=0.1)
movel(WP_3, a=0.5, v=0.1)
```

Do not inline pose literals into `movel()` calls. The `global WP_n = p[...]` form matches the format produced by the PolyScope teach pendant and lets the user read and edit waypoints separately from motion commands.

### ROS2 quaternion ↔ UR rotation vector

```python
# rclpy node
from geometry_msgs.msg import Pose
from scipy.spatial.transform import Rotation as R

def pose_to_ur_rotvec(pose: Pose) -> list[float]:
    """Convert ROS2 geometry_msgs/Pose to a UR-style [x,y,z,rx,ry,rz] in meters/radians."""
    rotvec = R.from_quat([
        pose.orientation.x,
        pose.orientation.y,
        pose.orientation.z,
        pose.orientation.w,
    ]).as_rotvec()
    return [
        pose.position.x, pose.position.y, pose.position.z,
        rotvec[0], rotvec[1], rotvec[2],
    ]
```

ROS2's quaternion order is `(x, y, z, w)`. SciPy's `from_quat()` expects the same order. tf2's `tf2_geometry_msgs` uses the same order. Be careful when interfacing with libraries that use `(w, x, y, z)` (Eigen, ROS1 tf).

## Code or command patterns

### Verify the active TCP at session start

```python
from rtde_control import RTDEControlInterface
from rtde_receive import RTDEReceiveInterface

rtde_r = RTDEReceiveInterface("192.168.1.10")
print("Current TCP pose (base frame):", rtde_r.getActualTCPPose())

rtde_c = RTDEControlInterface("192.168.1.10")
# Set TCP for RG6 with standard fingertips. VERIFY this for your install.
rtde_c.setTcp([0.0, 0.0, 0.159, 0.0, 0.0, 0.0])  # 159 mm Z offset, no rotation
```

### Check unit conversions at the bridge

In any Grasshopper-to-robot bridge, the first defensive step is a unit assert:

```python
import Rhino
units = Rhino.RhinoDoc.ActiveDoc.ModelUnitSystem
assert str(units) == "Millimeters", f"Document is {units}, expected Millimeters"
```

### Validate the target before motion

```python
# Before any moveL/moveJ on hardware:
target = [0.4, 0.2, 0.3, 0, 3.14159, 0]

# 1. Bounds check
assert -1.3 < target[0] < 1.3, "X out of UR10e reach"
assert -1.3 < target[1] < 1.3, "Y out of UR10e reach"
assert 0.0 < target[2] < 1.3,  "Z below table or out of reach"

# 2. Rotation sanity
import math
angle = math.sqrt(sum(c*c for c in target[3:6]))
assert angle <= 2 * math.pi, "Rotation magnitude exceeds 2π; suspect bad conversion"

# 3. UR safety planes (uses configured safety zones on the controller)
assert rtde_c.isPoseWithinSafetyLimits(target), "Target violates safety limits"

# 4. Conservative defaults
rtde_c.moveL(target, speed=0.1, acceleration=0.1)
```

## Risks

- **Frame confusion.** Sending a feature-frame target with a base-frame motion command produces wildly wrong motion. Mitigation: variable naming convention `<thing>_in_<frame>`.
- **Unit mismatch.** Grasshopper millimeters interpreted as meters sends the robot 1000× too far. Mitigation: unit assert at every bridge boundary.
- **Stale TCP.** Forgetting to set the TCP after a tool change or a controller reboot makes every motion wrong by the offset. Mitigation: `setTcp()` at session start, every script.
- **Axis-angle composition.** Adding rotation vector components is mathematically wrong. Mitigation: always convert to matrix or quaternion for composition.
- **Quaternion convention drift.** ROS2 uses `(x,y,z,w)`; some libraries use `(w,x,y,z)`. Mitigation: explicit element-by-element packing, never `list(quat)`.
- **Payload not updated.** RG6 (1.25 kg) plus a 5 kg workpiece must be set as 6.25 kg payload. Forgetting trips the protective stop on fast moves. Mitigation: `set_payload()` after pickup, restore after release.

## Open questions

- What is the actual measured TCP offset for the current RG6 + custom fingertip configuration? Need a calibration measurement, not the 159 mm placeholder.
- Should the world frame be defined by the UR base frame or by a workspace fiducial? Current setup uses the base frame; this breaks if the robot is moved or remounted.
- Is the project committing to ROS2 Humble or Jazzy long-term? Affects Python version (3.10 vs 3.12) and several library compatibility decisions.
- Is wrist-3 unwinding required for long jobs? Open question pending a multi-hour fabrication trial.

## Related raw files

- `raw/ur10e_ros2_grasshopper/ur_rtde_pose_examples.md` — example RTDE pose commands (to be added).
- `raw/ur10e_ros2_grasshopper/onrobot_rg6_datasheet.pdf` — official RG6 datasheet (to be added).
- `raw/ur10e_ros2_grasshopper/ur10e_techsheet.pdf` — official UR10e tech sheet (to be added).

## Related wiki pages

- [UR10e ROS2-Grasshopper Overview](overview.md)
- [Architecture](architecture.md)
- [ROS2 bridge](ros2_bridge.md)
- [Grasshopper bridge](grasshopper_bridge.md)
- [UR10e RG6 control](ur10e_rg6_control.md)
- [Testing checklist](testing_checklist.md)
- [Open questions](open_questions.md)
- [Glossary](../glossary.md)

## Last updated

2026-04-29
