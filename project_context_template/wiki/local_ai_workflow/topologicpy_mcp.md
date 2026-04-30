# TopologicPy MCP

## Purpose

Record the project knowledge for `Adventurous-Systems/topologicpy_MCP`, a Model Context Protocol server that exposes TopologicPy spatial modeling tools to MCP clients.

## Confirmed facts

- Repository: https://github.com/Adventurous-Systems/topologicpy_MCP
- Checked: 2026-04-30.
- Latest TopologicPy API docs checked: https://topologicpy.readthedocs.io/en/latest/topologicpy.html
- Latest docs version observed on 2026-04-30: TopologicPy `0.9.22`.
- The MCP repository `pyproject.toml` declares `topologicpy>=0.7.0` without an upper bound; compatibility must be checked against the installed TopologicPy version before use.
- The repository describes itself as a TopologicPy MCP server for Claude Code, Claude Desktop, and other MCP clients.
- It keeps a named object session across a conversation, for example named cells, cell complexes, and graphs.
- The README lists 36 tools covering geometry creation, boolean operations, transformations, topology queries, graph operations, metadata dictionaries, import/export, and session management.
- Import/export tools include BREP, OBJ, and IFC.
- Graph tools include `create_graph_from_topology` and `graph_shortest_path`.
- Setup examples are provided for Claude Code, Claude Desktop, standalone stdio transport, and MCP Inspector.
- License listed by GitHub: AGPL-3.0.

## Current working assumptions

- Treat this as a candidate local MCP tool for AEC spatial modeling and graph construction experiments.
- Do not treat it as project memory. Durable project knowledge still lives in this wiki.
- Do not add it to the active MCP configuration until the user explicitly asks to install or test it.
- Always check the latest TopologicPy docs before using or modifying the MCP wrapper. Do not assume the wrapper remains compatible with current TopologicPy.

## Implementation notes

- Potential use in this project: generate or inspect building topologies, derive adjacency graphs, and export IFC/BREP/OBJ artifacts for GraphML experiments.
- The session-store pattern may help agents refer to named geometry objects across multi-step design conversations.
- Before using it for experiments, verify TopologicPy API compatibility, OpenCASCADE/BREP behavior, IfcOpenShell availability, and Windows installation constraints in the local environment.

## Compatibility Check

Required before installing, running, or editing this MCP server:

1. Open the latest TopologicPy docs: https://topologicpy.readthedocs.io/en/latest/topologicpy.html
2. Record the docs version and date in this page.
3. Compare every MCP wrapper method against the current TopologicPy API names and parameter names.
4. Run a minimal smoke test for creation, query, graph generation, and export/import before using it for project data.
5. Pin the tested `topologicpy_MCP` commit and the installed `topologicpy` version.

Initial compatibility notes from 2026-04-30:

- Current docs list modules and methods used by the MCP wrapper, including `Vertex.ByCoordinates`, `Edge.ByVertices`, `Wire.ByVertices`, `Face.ByWire`, `Face.Rectangle`, `Face.Circle`, `Cell.ByFaces`, `Cell.Prism`, `Cell.Cylinder`, `CellComplex.ByCells`, `Cluster.ByTopologies`, `Topology.Translate`, `Topology.Rotate`, `Topology.Scale`, `Graph.ByTopology`, `Graph.ShortestPath`, `Dictionary.ByKeysValues`, `Topology.BREPString`, and `Topology.ExportToOBJ`.
- Current docs list `Graph.ByIFCFile` / `Graph.ByIFCPath` and many graph export methods.
- Potential incompatibility: the MCP wrapper calls `Topology.ExportToIFC` and `Topology.ByIFCFile`; in the latest docs checked, `Topology.ExportToIFC` was not listed in the top-level Topology API index, while `Topology.ExportToBIM` is listed. Treat the MCP `export_topology(..., format="ifc")` and `import_topology(..., format="ifc")` paths as unverified until a local smoke test passes or the wrapper is patched.

## Code or command patterns

From the repository README, the MCP server can be configured for Claude Code with a Python module command or an `uv run` command after installation. Do not run these until a test task is approved.

```json
{
  "mcpServers": {
    "topologic": {
      "command": "python",
      "args": ["-m", "topologic_mcp"],
      "cwd": "/path/to/topologic-mcp-server"
    }
  }
}
```

## Risks

- The repository has no releases listed at the time of checking; pin a commit before relying on it.
- The wrapper may drift from TopologicPy latest API because it allows `topologicpy>=0.7.0` with no upper bound.
- The IFC import/export wrapper is specifically unverified against TopologicPy `0.9.22`.
- Geometry and IFC export pipelines can be sensitive to dependency versions and operating system setup.
- AGPL-3.0 licensing may matter if code or server modifications are redistributed. Confirm licensing before bundling it with project artifacts.
- LLM-generated geometry must still be validated with deterministic scripts before feeding GraphML or fabrication workflows.

## Open questions

- Should this MCP server be installed locally for a controlled TopologicPy smoke test?
- Should TopologicPy be part of the GraphML dataset construction pipeline, or only an exploratory assistant tool?
- Which minimal IFC-to-graph benchmark should be used to validate the server's adjacency graph output?
- Should `topologicpy_MCP` be patched to use `Topology.ExportToBIM` or another current IFC/BIM export API if `Topology.ExportToIFC` fails?

## Related raw files

(populate via `/ingest_raw`)

## Related wiki pages

- [Local AI workflow overview](overview.md)
- [Claude Code setup](claude_code_setup.md)
- [GraphML overview](../graphml_baseline_comparison/overview.md)
- [GraphML dataset notes](../graphml_baseline_comparison/dataset_notes.md)

## Last updated

2026-04-30
