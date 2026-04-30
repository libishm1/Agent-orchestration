# WebSockets Library Notes

**Cached from:** Context7  
**Library version:** Latest (checked 2026-04-30)  
**Library ID:** `/pypi/websockets`  

## Usage in This Project

The grasshopper_websocket_pose_pipeline server uses websockets to relay UR10e robot pose data:
- **Schema:** `cm-itad.ur10e.pose.v1`
- **Server:** `ws://127.0.0.1:8765` (default)

## Key API Patterns

### Import (v14+ / fallback)

```python
try:
    from websockets.asyncio.server import serve as websocket_serve
except ImportError:  # websockets < 14
    from websockets import serve as websocket_serve
```

### Server Handler

```python
async def handler(websocket, path=None):
    async for message in websocket:
        # Process message
        await websocket.send(json.dumps(response))

async with websocket_serve(handler, host, port):
    await asyncio.Future()  # Run forever
```

## Message Format (Project-Specific)

**Inbound robot_pose:**
```json
{
  "type": "robot_pose",
  "pose": [x, y, z, rx, ry, rz],
  "units": {"linear": "m", "angular": "rad"},
  "timestamp": "ISO 8601 UTC",
  "frame_id": "base",
  "source": "grasshopper"
}
```

**Outbound pose_ack:**
```json
{
  "type": "pose_ack",
  "schema": "cm-itad.ur10e.pose.v1",
  "timestamp": "ISO 8601 UTC",
  "status": "accepted",
  "client_count": 1
}
```

## Safe Defaults

- Translation validation: max 2.0 m
- Rotation vector: max 2π + 1e-6 radians
- All poses must be in meters/radians before sending
- Execution level: 1 (offline relay only, no robot motion)

---

**Next refresh:** 2026-07-30 (90-day cache) or if websockets publishes a major version bump.
