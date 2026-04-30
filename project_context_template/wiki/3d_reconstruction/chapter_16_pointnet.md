# Chapter 16 Study Notes - PointNet for 3D Object Classification

## Source

- Book: Florent Poux, *3D Data Science with Python*
- Chapter: 16, "PointNet for 3D Object Classification"
- Local extraction: `3d_data_science_python.md`
- Prepared: 2026-04-30

## Study Goal

Understand PointNet as a point-based architecture and how it supports object classification and point cloud inference.

## Core Takeaways

- PointNet processes unordered point sets and is a foundational point cloud deep learning architecture.
- Dataset preparation, normalization, sampling, and labels are critical.
- Classification metrics must be paired with spatial/error inspection.
- Real-world inference can fail when training data does not match operational data.

## PointNet Workflow

1. Curate dataset.
2. Normalize point sets.
3. Sample consistent point counts.
4. Define architecture and loss.
5. Train and validate.
6. Evaluate metrics.
7. Run real-world inference.
8. Inspect errors.

## Project Implications

- PointNet is useful as a reference architecture, but GraphML work may prioritize GNNs.
- Point sampling can lose geometry important to AEC objects.
- Real-world inference needs strict preprocessing parity.

## Study Questions

1. Why must point cloud normalization be consistent?
2. What does PointNet gain by operating directly on points?
3. What can be lost when sampling to a fixed point count?
4. How should real-world inference be validated?

## My notes

```text
Add personal notes here.
```

## Related Pages

- [3D reconstruction knowledge base](3d_reconstruction_knowledge_base.md)
- [GraphML overview](../graphml_baseline_comparison/overview.md)

## Last updated

2026-04-30
