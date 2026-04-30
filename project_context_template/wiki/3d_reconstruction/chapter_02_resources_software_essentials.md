# Chapter 2 Study Notes - Resources and Software Essentials

## Source

- Book: Florent Poux, *3D Data Science with Python*
- Chapter: 2, "Resources and Software Essentials"
- Local extraction: `3d_data_science_python.md`
- Prepared: 2026-04-30

## Study Goal

Identify the mathematical, computational, hardware, and software foundations needed for practical 3D data science.

## Core Takeaways

- 3D workflows require a mix of math, computer science, domain expertise, and AI literacy.
- Hardware choices matter because point clouds, meshes, and deep learning workloads can become memory- and GPU-intensive.
- A productive environment separates reconstruction, processing, visualization, and application development tools.
- Tool choice should follow the task: acquisition/reconstruction, processing/analysis, visualization, or deployment.

## Key Concepts

| Concept | Why It Matters |
|---|---|
| Linear algebra | transformations, PCA, normals, rotations, registration |
| Geometry | shapes, distances, neighborhoods, primitives |
| Computer science | data structures, complexity, memory, file I/O |
| 3D expertise | sensor limitations, coordinate systems, reconstruction artifacts |
| AI for 3D | segmentation, classification, automation, inference |
| Local vs cloud compute | cost, GPU availability, privacy, scale |

## Project Implications

- Pin a standard Python environment before running point cloud experiments.
- Choose tooling per workflow stage rather than forcing one application to do everything.
- Treat visualization software as inspection support, not as proof of correctness.
- For GraphML, prioritize reproducible preprocessing over interactive-only operations.

## Study Questions

1. Which math concepts show up repeatedly in registration and feature extraction?
2. When should a workflow move from local compute to cloud/GPU compute?
3. What is the difference between reconstruction software and processing software?
4. Which tools are required for reproducible experiments versus visual inspection?

## My notes

```text
Add personal notes here.
```

## Related Pages

- [3D reconstruction knowledge base](3d_reconstruction_knowledge_base.md)
- [GraphML dataset notes](../graphml_baseline_comparison/dataset_notes.md)

## Last updated

2026-04-30
