# Chapter 7 Study Notes - Building 3D Analytical Apps

## Source

- Book: Florent Poux, *3D Data Science with Python*
- Chapter: 7, "Building 3D Analytical Apps"
- Local extraction: `3d_data_science_python.md`
- Prepared: 2026-04-30

## Study Goal

Connect point cloud processing to usable analytical applications with features, thresholds, interaction, and export.

## Core Takeaways

- Analytical apps should expose the reasoning path, not just the final visualization.
- k-d trees, covariance, eigenvalues, and eigenvectors support local geometry descriptors.
- Interactive thresholds are useful for exploration but must be recorded when used in reproducible workflows.
- Results export is part of the app design.

## Key Features

- planarity
- linearity
- omnivariance
- verticality
- normals
- local neighborhoods
- thresholded selections

## Project Implications

- Any interactive analysis used for dataset construction must export parameters.
- Feature engineering apps can support GraphML preprocessing.
- Exported results should include both geometry IDs and derived attributes.

## Study Questions

1. Which geometric features are most useful for separating planar and linear structures?
2. Why should interactive thresholds be recorded?
3. What should a 3D analytical app export for reproducibility?

## My notes

```text
Add personal notes here.
```

## Related Pages

- [3D reconstruction knowledge base](3d_reconstruction_knowledge_base.md)
- [GraphML dataset notes](../graphml_baseline_comparison/dataset_notes.md)

## Last updated

2026-04-30
