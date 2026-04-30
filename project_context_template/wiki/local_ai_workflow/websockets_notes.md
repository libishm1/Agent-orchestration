# WebSockets Library Notes

**Cached from:** Context7
**Library version:** 16.0
**Library ID:** `/python-websockets/websockets/16.0`
**Last verified:** 2026-04-30

## Usage in This Project

The `grasshopper_websocket_pose_pipeline` server uses `websockets` to relay UR10e robot pose data:

- **Schema:** `cm-itad.ur10e.pose.v1`
- **Server:** `ws://127.0.0.1:8765` by default
- **Current local environment:** `websockets` 11.0.3, so the prototype keeps compatibility imports until the environment is upgraded.

## Current API Pattern

Context7 resolved the upstream docs to `/python-websockets/websockets`, with version `16.0` available. The current asyncio server API is:

```python
import asyncio
from websockets.asyncio.server import ServerConnection, serve

async def handler(websocket: ServerConnection) -> None:
    async for message in websocket:
        await websocket.send(message)

async def main() -> None:
    async with serve(handler, "127.0.0.1", 8765) as server:
        await server.serve_forever()

asyncio.run(main())
```

Important server details:

- Handler signature is one argument: `handler(websocket)`.
- The connection object is `websockets.asyncio.server.ServerConnection`.
- Request path and headers live on `websocket.request.path` and `websocket.request.headers`.
- Response headers live on `websocket.response.headers`.
- `serve()` returns a `Server` with `connections`, `close()`, `wait_closed()`, `serve_forever()`, `start_serving()`, and `sockets`.
- Use `websockets.asyncio.router.route()` for Werkzeug-based URL routing.

## Project Compatibility Pattern

The project artifact currently supports the installed `websockets` 11.0.3 while preferring the current API when available:

```python
try:
    from websockets.asyncio.server import serve as websocket_serve
except ImportError:  # websockets < 14
    from websockets import serve as websocket_serve

async def handler(websocket):
    async for message in websocket:
        await websocket.send(message)
```

Keep this fallback only for local/offline compatibility. New code should use the current `websockets.asyncio.*` imports directly when the runtime dependency is pinned to `websockets >= 16`.

## Migration Notes

- `websockets.legacy.*` is deprecated and planned for removal by 2030.
- The old `handler(websocket, path)` pattern is deprecated. Use `websocket.request.path` on current versions.
- `process_request` now receives `(connection, request)`.
- `extra_headers` is replaced by `process_response(connection, request, response)`.
- `create_protocol` is replaced by `create_connection`.

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
- Rotation vector: max `2*pi + 1e-6` radians
- All poses must be in meters/radians before sending
- Execution level: 1 (offline relay only, no robot motion)

## Sources

- Context7 query: `/python-websockets/websockets/16.0`, server API, checked 2026-04-30.
- Official docs: https://websockets.readthedocs.io/en/stable/reference/asyncio/server.html
- Official upgrade guide: https://websockets.readthedocs.io/en/stable/howto/upgrade.html

**Next refresh:** 2026-07-30 (90-day cache) or if `websockets` publishes a major version bump.
