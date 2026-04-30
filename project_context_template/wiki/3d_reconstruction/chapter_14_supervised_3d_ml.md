# Chapter 14 Study Notes - Supervised 3D Machine Learning Fundamentals

## Source

- Book: Florent Poux, *3D Data Science with Python*
- Chapter: 14, "Supervised 3D Machine Learning Fundamentals"
- Local extraction: `3d_data_science_python.md`
- Prepared: 2026-04-30

## Study Goal

Understand supervised learning for 3D semantic segmentation, including feature preparation, metrics, models, inference, and generalization.

## Core Takeaways

- Supervised 3D ML depends on label quality, feature consistency, and split discipline.
- Semantic segmentation assigns meaning at point, voxel, segment, or object level.
- Metrics must match the task and class imbalance.
- Generalization is a separate problem from training accuracy.

## Supervised Pipeline

1. Define label schema.
2. Prepare point/segment features.
3. Split data without leakage.
4. Train baseline models.
5. Evaluate with task-appropriate metrics.
6. Run inference on held-out data.
7. Inspect errors spatially.

## Project Implications

- GraphML experiments need leakage-aware splits.
- Labels should preserve geometry IDs.
- Baselines should precede deep learning.

## Study Questions

1. What is the difference between classification and semantic segmentation?
2. Which metrics are useful when classes are imbalanced?
3. How can spatial leakage enter train/test splits?
4. What should be inspected after inference?

## My notes

```text
Add personal notes here.
```

## Related Pages

- [GraphML overview](../graphml_baseline_comparison/overview.md)
- [3D reconstruction knowledge base](3d_reconstruction_knowledge_base.md)

## Last updated

2026-04-30
