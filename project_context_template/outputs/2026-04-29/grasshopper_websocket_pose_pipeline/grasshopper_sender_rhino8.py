"""Rhino 8 ScriptEditor sender for the local pose relay.

Expected Grasshopper inputs:
- plane: Rhino.Geometry.Plane
- send: bool
- uri: optional string, defaults to ws://127.0.0.1:8765

Execution level: 1. This only sends JSON to the local relay.
"""

import json
import math
from datetime import datetime, timezone

import Rhino.Geometry as rg


SCHEMA = "cm-itad.ur10e.pose.v1"


def _normalize(vector):
    length = math.sqrt(vector.X * vector.X + vector.Y * vector.Y + vector.Z * vector.Z)
    if length <= 1e-12:
        raise ValueError("Plane axis has near-zero length")
    return vector.X / length, vector.Y / length, vector.Z / length


def _clamp(value, low, high):
    return max(low, min(high, value))


def matrix_to_rotvec(m):
    trace = m[0][0] + m[1][1] + m[2][2]
    angle = math.acos(_clamp((trace - 1.0) * 0.5, -1.0, 1.0))
    if angle < 1e-12:
        return [0.0, 0.0, 0.0]

    sin_angle = math.sin(angle)
    if abs(sin_angle) > 1e-8:
        axis = [
            (m[2][1] - m[1][2]) / (2.0 * sin_angle),
            (m[0][2] - m[2][0]) / (2.0 * sin_angle),
            (m[1][0] - m[0][1]) / (2.0 * sin_angle),
        ]
        return [axis[0] * angle, axis[1] * angle, axis[2] * angle]

    # 180-degree case: derive an axis from the diagonal.
    xx = max(0.0, (m[0][0] + 1.0) * 0.5)
    yy = max(0.0, (m[1][1] + 1.0) * 0.5)
    zz = max(0.0, (m[2][2] + 1.0) * 0.5)
    axis = [math.sqrt(xx), math.sqrt(yy), math.sqrt(zz)]
    if m[0][1] < 0.0:
        axis[1] = -axis[1]
    if m[0][2] < 0.0:
        axis[2] = -axis[2]
    return [axis[0] * angle, axis[1] * angle, axis[2] * angle]


def plane_to_pose_event(plane, sequence=1):
    if not isinstance(plane, rg.Plane) or not plane.IsValid:
        raise ValueError("Expected a valid Rhino.Geometry.Plane")

    x_axis = _normalize(plane.XAxis)
    y_axis = _normalize(plane.YAxis)
    z_axis = _normalize(plane.ZAxis)
    rotation_matrix = [
        [x_axis[0], y_axis[0], z_axis[0]],
        [x_axis[1], y_axis[1], z_axis[1]],
        [x_axis[2], y_axis[2], z_axis[2]],
    ]

    return {
        "type": "robot_pose",
        "schema": SCHEMA,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "source": "rhino8_grasshopper",
        "sequence": sequence,
        "frame_id": "base",
        "units": {"linear": "m", "angular": "rad"},
        "pose": {
            "position": [
                plane.OriginX * 0.001,
                plane.OriginY * 0.001,
                plane.OriginZ * 0.001,
            ],
            "rotation_vector": matrix_to_rotvec(rotation_matrix),
        },
        "speed": 0.1,
        "acceleration": 0.1,
    }


def send_text_websocket(uri, text):
    import clr

    clr.AddReference("System")
    clr.AddReference("System.Net.WebSockets.Client")
    from System import Array, ArraySegment, Byte, Uri
    from System.Net.WebSockets import ClientWebSocket, WebSocketMessageType
    from System.Text import Encoding
    from System.Threading import CancellationToken

    client = ClientWebSocket()
    client.ConnectAsync(Uri(uri), CancellationToken.None).Wait()
    payload = Encoding.UTF8.GetBytes(text)
    segment = ArraySegment[Byte](payload, 0, payload.Length)
    client.SendAsync(segment, WebSocketMessageType.Text, True, CancellationToken.None).Wait()
    client.CloseAsync(1000, "done", CancellationToken.None).Wait()


if "uri" not in globals() or not uri:
    uri = "ws://127.0.0.1:8765"
if "send" not in globals():
    send = False
if "plane" not in globals() or plane is None:
    plane = rg.Plane.WorldXY

payload = json.dumps(plane_to_pose_event(plane))
status = "ready"

if send:
    send_text_websocket(uri, payload)
    status = "sent"
