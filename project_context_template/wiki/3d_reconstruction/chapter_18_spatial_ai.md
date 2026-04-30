# Chapter 18 Study Notes - From 3D Generative AI to Spatial AI

## Source

- Book: Florent Poux, *3D Data Science with Python*
- Chapter: 18, "From 3D Generative AI to Spatial AI"
- Local extraction: `3d_data_science_python.md`
- Prepared: 2026-04-30

## Study Goal

Understand advanced directions: generative AI for 3D reconstruction, deep registration, semantic modeling, transformers, Gaussian splatting, and spatial AI reasoning.

## Core Takeaways

- Generative 3D methods can accelerate exploration but require strong validation.
- Deep registration and semantic modeling extend classic workflows with learned components.
- Gaussian splatting is relevant for visualization and scene representation, not automatically for metric reconstruction.
- Spatial AI requires geometry, topology, semantics, and reasoning to work together.

## Advanced Topics Map

| Topic | Project Interpretation |
|---|---|
| generative 3D reconstruction | exploratory modeling, not measured truth |
| deep point cloud registration | candidate research direction after classical registration baseline |
| semantic modeling | bridge from reconstruction to AEC/robotics meaning |
| transformers | possible semantic extraction and open-vocabulary workflows |
| Gaussian splatting | visualization/scene representation candidate |
| spatial reasoning | long-term goal for agents operating over 3D environments |

## Project Implications

- Do not confuse generated geometry with measured geometry.
- Keep classical baselines before adopting learned or generative methods.
- Spatial AI outputs must be auditable before they influence robot motion or construction decisions.

## Study Questions

1. What validation is needed before using generative 3D outputs?
2. How is Gaussian splatting different from a mesh or point cloud?
3. What makes semantic modeling useful for AEC and robotics?
4. Which spatial AI outputs require human approval?

## My notes

```text
Add personal notes here.
```

## Related Pages

- [3D reconstruction knowledge base](3d_reconstruction_knowledge_base.md)
- [GraphML overview](../graphml_baseline_comparison/overview.md)
- [UR10e ROS2-Grasshopper overview](../ur10e_ros2_grasshopper/overview.md)

## Last updated

2026-04-30
