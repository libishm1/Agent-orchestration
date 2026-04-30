# Chapter 13 Study Notes - Graphs and Foundation Models for Unsupervised Segmentation

## Source

- Book: Florent Poux, *3D Data Science with Python*
- Chapter: 13, "Graphs and Foundation Models for Unsupervised Segmentation"
- Local extraction: `3d_data_science_python.md`
- Prepared: 2026-04-30

## Study Goal

Connect graph-based segmentation, connected components, Euclidean clustering, and foundation-model-assisted segmentation.

## Core Takeaways

- Graphs encode relationships between spatial entities.
- Connected components can segment point clouds when adjacency rules are meaningful.
- Euclidean clustering is a geometry-based graph/connectivity idea.
- Foundation models such as image segmentation models can assist 3D segmentation through projections, but require validation.

## Project Implications

- This chapter is central to the GraphML baseline work.
- Graph construction rules must be explicit before comparing DGL, PyG, or SVM.
- Projection-based workflows can generate candidate labels, but labels must be checked in 3D.

## Graph Construction Questions

- What is a node: point, voxel, segment, surface, room, or building element?
- What is an edge: distance threshold, contact, shared boundary, visibility, or semantic relation?
- What features belong on nodes versus edges?
- How is the graph validated?

## Study Questions

1. How do connected components support point cloud segmentation?
2. What are the risks of projecting 3D data into 2D for segmentation?
3. How should foundation-model labels be validated in 3D?
4. Which graph choices affect ML results the most?

## My notes

```text
Add personal notes here.
```

## Related Pages

- [GraphML dataset notes](../graphml_baseline_comparison/dataset_notes.md)
- [3D reconstruction knowledge base](3d_reconstruction_knowledge_base.md)

## Last updated

2026-04-30
