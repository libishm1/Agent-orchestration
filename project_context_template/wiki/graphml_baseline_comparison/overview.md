# Graph Machine Learning Baseline Comparison Overview

## Purpose

Map of the GraphML pipelines compared in this project: DGL, PyTorch Geometric (PyG), and an SVM baseline. Defines the fairness rules for the comparison.

## Confirmed facts

- The comparison runs three pipelines against the same dataset, the same features (where applicable), the same split, and the same metric.
- DGL and PyG are both message-passing GNN frameworks. They are not interchangeable but they cover the same conceptual space.
- DGL has had no major release since late 2024. PyG has a more active 2025–2026 release cadence and is the dominant framework in the AEC GraphML literature for Libish's PRISMA review window.
- SVM is the non-graph baseline. It operates on flattened or aggregated features extracted from the same graph.

## Current working assumptions

- Dataset and split rules are documented in [dataset_notes](dataset_notes.md). Follow them strictly.
- New experiments default to PyG. DGL is maintained for legacy comparison only.
- The SVM baseline uses scikit-learn with RBF kernel by default. Hyperparameters are documented in [svm_baseline](svm_baseline.md).

## Implementation notes

- Define graph construction once, in [dataset_notes](dataset_notes.md). All pipelines read from the same constructed graph.
- Feature extraction must be identical across DGL and PyG pipelines.
- For SVM, the feature extraction must be a documented, defensible aggregation (mean, max, concat, graph-level pooling) of the per-node features.

## Code or command patterns

(populate as pipelines stabilize)

## Risks

- **Different splits.** Easy to introduce by accident. Pin the seed and the split file.
- **Leakage.** Especially for graphs where train and test nodes share edges. Use inductive splits where possible.
- **Implicit feature differences.** PyG and DGL have subtle differences in normalization defaults. Verify per-feature.
- **Calling DGL or PyG "the better framework".** They are different tools. Compare end-to-end model performance, not framework choice.

## Open questions

- Should a third GNN framework (e.g. NetworkX + custom JAX) be added for sanity check?
- Are graph-level or node-level tasks the primary target? Affects the split strategy.

## Related raw files

(populate via `/ingest_raw`)

## Related wiki pages

- [Dataset notes](dataset_notes.md)
- [DGL pipeline](dgl_pipeline.md)
- [PyG pipeline](pyg_pipeline.md)
- [SVM baseline](svm_baseline.md)
- [Comparison matrix](comparison_matrix.md)
- [Metrics](metrics.md)

## Last updated

2026-04-29
