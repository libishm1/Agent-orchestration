# Chapter 4 Study Notes - 3D Data Representation and Structuration

## Source

- Book: Florent Poux, *3D Data Science with Python*
- Chapter: 4, "3D Data Representation and Structuration"
- Local extraction: `3d_data_science_python.md`
- Prepared: 2026-04-30

## Study Goal

Understand the main ways to represent 3D data and how to choose structures for processing, storage, and ML.

## Core Takeaways

- Point clouds, meshes, voxels, rasters, images, and high-level semantic models each serve different purposes.
- Converting between representations changes what information is easy to preserve or lose.
- Data structures such as k-d trees, octrees, and BVHs make large 3D workflows practical.
- File organization is part of reproducibility.

## Representation Decision Table

| Representation | Good For | Avoid When |
|---|---|---|
| Point cloud | measured reality, flexible analysis | topology or watertight surfaces are required |
| Mesh | surface visualization, simulation, export | uncertainty must remain explicit |
| Voxel | occupancy, volumetric ML, regular grids | fine details exceed memory limits |
| Raster/depth image | projection and image pipelines | full 3D relationships are needed |
| Graph/topology | relationships, adjacency, semantics | construction rules are unclear |

## Project Implications

- GraphML preprocessing must document how geometry becomes nodes and edges.
- AEC reconstruction should preserve source geometry IDs through representation changes.
- Robotics workflows must avoid hidden unit/frame changes during conversion.

## Study Questions

1. What information is lost when a point cloud becomes a mesh?
2. When is a voxel grid preferable to a point cloud?
3. Why do k-d trees and octrees matter for large point clouds?
4. How does representation choice affect GraphML features?

## My notes

```text
Add personal notes here.
```

## Related Pages

- [3D reconstruction knowledge base](3d_reconstruction_knowledge_base.md)
- [TopologicPy MCP](../local_ai_workflow/topologicpy_mcp.md)

## Last updated

2026-04-30
