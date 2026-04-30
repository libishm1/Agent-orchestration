# Dataset Notes

## Purpose

{Fill in.}

## Confirmed facts

- `Adventurous-Systems/topologicpy_MCP` is a candidate MCP server for TopologicPy-backed spatial modeling, topology queries, graph operations, and IFC/BREP/OBJ import-export. Repository checked 2026-04-30: https://github.com/Adventurous-Systems/topologicpy_MCP
- Latest TopologicPy docs must be checked before using that MCP server. Docs checked 2026-04-30: https://topologicpy.readthedocs.io/en/latest/topologicpy.html, version `0.9.22`.

## Current working assumptions

- Dataset construction remains deterministic and scriptable. MCP-assisted geometry or graph generation may be used for exploration, but generated outputs must be exported and validated before becoming benchmark inputs.
- Do not accept TopologicPy MCP outputs as benchmark inputs until the MCP wrapper has passed compatibility checks against the latest TopologicPy docs and the local installed package.

## Implementation notes

- If TopologicPy MCP is tested, first run a minimal building adjacency case and compare the resulting graph nodes, edges, and metadata against a manually specified expected graph.
- Any TopologicPy-derived IFC or adjacency artifact should be stored as raw/intermediate data with source prompt, tool version or commit, and validation notes.
- Include the TopologicPy docs version, installed `topologicpy` version, and `topologicpy_MCP` commit in any dataset construction notes that use this tool.

## Code or command patterns

{Fill in.}

## Risks

- LLM-driven geometry generation can change topology assumptions without obvious code diffs.
- IFC export/import may introduce schema or coordinate-system changes that affect graph labels and adjacency.
- Using an MCP server in preprocessing can reduce reproducibility unless the commit, environment, and prompts are pinned.
- `topologicpy_MCP` IFC import/export paths are unverified against TopologicPy `0.9.22`; smoke-test those paths before relying on them.

## Open questions

- Should TopologicPy MCP be limited to exploratory modeling, or can it be accepted as a reproducible preprocessing component after validation?
- What is the smallest IFC/topology fixture that should become the graph-construction smoke test?

## Related raw files

(populate via /ingest_raw)

## Related wiki pages

- [Overview](overview.md)
- [TopologicPy MCP](../local_ai_workflow/topologicpy_mcp.md)

## Last updated

2026-04-30
