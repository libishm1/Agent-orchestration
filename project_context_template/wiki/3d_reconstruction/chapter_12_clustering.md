# Chapter 12 Study Notes - 3D Machine Learning: Clustering

## Source

- Book: Florent Poux, *3D Data Science with Python*
- Chapter: 12, "3D Machine Learning: Clustering"
- Local extraction: `3d_data_science_python.md`
- Prepared: 2026-04-30

## Study Goal

Understand unsupervised segmentation through clustering, including k-means, DBSCAN, and hybrid multi-RANSAC refinement.

## Core Takeaways

- Clustering groups points or features without labels.
- k-means is simple but assumes compact clusters and known cluster count.
- DBSCAN handles noise and unknown cluster count but depends on density parameters.
- Hybrid workflows can combine primitive fitting with density-based refinement.

## Method Comparison

| Method | Strength | Weakness |
|---|---|---|
| k-means | simple and fast | requires cluster count; weak for irregular geometry |
| DBSCAN | finds density clusters and noise | sensitive to epsilon and min-points |
| multi-RANSAC | extracts repeated primitives | needs model assumptions |
| RANSAC + DBSCAN | robust primitive detection plus cluster cleanup | more parameters to validate |

## Project Implications

- Unsupervised segmentation is useful before manual labeling or semantic ML.
- Parameters must be recorded because cluster output can change dramatically.
- Clusters can become graph nodes only after deterministic construction rules are defined.

## Study Questions

1. When is DBSCAN preferable to k-means?
2. Why does clustering representativity matter?
3. How can RANSAC and DBSCAN complement each other?
4. Which clustering parameters must be logged?

## My notes

```text
Add personal notes here.
```

## Related Pages

- [3D reconstruction knowledge base](3d_reconstruction_knowledge_base.md)
- [GraphML dataset notes](../graphml_baseline_comparison/dataset_notes.md)

## Last updated

2026-04-30
