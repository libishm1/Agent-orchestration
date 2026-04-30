# Chapter 15 Study Notes - 3D Deep Learning with PyTorch

## Source

- Book: Florent Poux, *3D Data Science with Python*
- Chapter: 15, "3D Deep Learning with PyTorch"
- Local extraction: `3d_data_science_python.md`
- Prepared: 2026-04-30

## Study Goal

Understand the PyTorch workflow for 3D deep learning and compare major 3D architecture families.

## Core Takeaways

- PyTorch workflows require clear dataset, dataloader, model, loss, optimizer, training, and inference components.
- 3D architecture choices depend on representation: voxels, points, graphs, or views.
- Serving a trained model requires the same preprocessing assumptions used during training.
- Transfer learning, fine-tuning, and augmentation can help but do not replace validation.

## Architecture Map

| Architecture | Input | Use |
|---|---|---|
| 3D CNN | voxels | volumetric patterns |
| GNN | graph | relational/spatial topology |
| PointNet-style | point sets | point cloud classification/segmentation |
| Multiview CNN | images/views | projection-based 3D reasoning |

## Project Implications

- PyG is the default for graph deep learning in this project.
- Keep preprocessing identical across training and inference.
- Start with small deterministic fixtures before full-scale training.

## Study Questions

1. How does representation choice determine architecture choice?
2. What must a PyTorch `Dataset` provide for 3D data?
3. Why is inference preprocessing a deployment risk?
4. When is a GNN preferable to a point-based model?

## My notes

```text
Add personal notes here.
```

## Related Pages

- [PyG pipeline](../graphml_baseline_comparison/pyg_pipeline.md)
- [3D reconstruction knowledge base](3d_reconstruction_knowledge_base.md)

## Last updated

2026-04-30
