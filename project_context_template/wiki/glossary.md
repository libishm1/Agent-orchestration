# Glossary

Terms used across the wiki. Define on first use in any page; cross-link here.

## Robotics

- **UR10e** — Universal Robots collaborative arm. Payload 12.5 kg, reach 1300 mm, pose repeatability ±0.05 mm. e-Series generation.
- **RG6** — OnRobot 2-finger collaborative gripper. Force-fit payload 6 kg, form-fit 10 kg, stroke 150 mm, force range 25–120 N, mass 1.25 kg.
- **TCP** — Tool Center Point. The reference frame at the working tip of the tool, defined relative to the flange. UR10e default flange-to-TCP offset depends on the mounted tool. RG6 with standard fingertips: see `ur10e_ros2_grasshopper/pose_frame_rules.md`.
- **TCP pose** — Position and orientation of the TCP, expressed in the base frame. Format on UR: `p[x, y, z, rx, ry, rz]` where x,y,z are in meters and rx,ry,rz are an axis-angle rotation vector in radians.
- **Motion pose** — Synonym some teams use for the target pose passed to a movel/movej. Distinct from the *current* TCP pose. Mixing them up is the most common source of bugs.
- **URScript** — Universal Robots' interpreted scripting language. Runs on the robot controller, not the external PC. Sent to port 30002 (secondary interface).
- **Axis-angle rotation vector** — Three-component representation `(rx, ry, rz)`. Direction is the rotation axis. Magnitude `sqrt(rx² + ry² + rz²)` is the rotation angle in radians. UR's native rotation format.
- **ROS2** — Second-generation Robot Operating System. Default distros for this project: Humble Hawksbill (Ubuntu 22.04) and Jazzy Jalisco (Ubuntu 24.04).
- **MoveIt2** — Motion planning framework for ROS2. Provides IK, planning, collision checking, trajectory execution.
- **`ur_robot_driver`** — Official ROS2 driver for UR e-series. Repository: `Universal_Robots_ROS2_Driver`.
- **Universal_Robots_ROS2_Driver** — Official Universal Robots ROS2 driver repository. Includes `ur_robot_driver`, `ur_controllers`, `ur_calibration`, `ur_dashboard_msgs`, and `ur_moveit_config`.
- **`ur_rtde`** — Python/C++ library by SDU Robotics for direct UR control via the RTDE interface. Independent of ROS2.
- **OnRobot ROS2 gripper candidates** — Community repositories for RG2/RG6 ROS2 integration, currently `ABC-iRobotics/onrobot-ros2` and `runtimerobotics/onrobot_rg2_ros2`. Evaluate and pin before using in lab motion workflows.
- **RG6 gripper description** — Community RG6 URDF/Xacro reference from `Zhengxuez/rg6_gripper_description`. Useful for visualization/modeling only after adapter, origin, and TCP offsets are verified.
- **Grasshopper** — Visual scripting environment inside Rhino. Two Python runtimes: legacy GHPython (IronPython 2.7) and ScriptEditor (CPython 3, Rhino 8+).

## Graph Machine Learning

- **Point cloud** — A set of 3D points, usually with coordinates and optional attributes such as color, intensity, normals, classification, or timestamp.
- **Registration** — Alignment of two or more 3D datasets into a shared coordinate frame. Often coarse alignment followed by ICP-style refinement.
- **ICP** — Iterative Closest Point, a fine-registration method that refines alignment by iteratively matching nearby geometry.
- **RANSAC** — Robust model-fitting method often used to detect planes or other primitives in noisy point clouds.
- **Voxelization** — Conversion of 3D space into a regular grid of volumetric cells.
- **DGL** — Deep Graph Library. Graph neural network framework. Last major release: late 2024. Considered mature; see `graphml_baseline_comparison/dgl_pipeline.md`.
- **PyG (PyTorch Geometric)** — Dominant 2026 GNN framework. Default for new pipelines in this project.
- **GNN** — Graph Neural Network. Generic term covering GCN, GAT, GraphSAGE, GIN, and variants.
- **SVM** — Support Vector Machine. Used here as a non-graph baseline trained on flattened/aggregated node or graph features.
- **Node feature** — Per-node attribute vector input to the GNN.
- **Edge feature** — Per-edge attribute vector. Optional input depending on model.
- **Graph construction** — The procedure that turns raw data (e.g. an IFC building model) into a graph. Defined per dataset; documented in `graphml_baseline_comparison/dataset_notes.md`.
- **Bridge to GNN (Categories A–D)** — Inclusion framework for the project's PRISMA review on GraphML in AEC.
- **TopologicPy MCP** — Candidate MCP server from `Adventurous-Systems/topologicpy_MCP` that exposes TopologicPy spatial modeling, topology query, graph, and IFC/BREP/OBJ tools to MCP clients.

## Local AI Workflow

- **Context7** — Upstash's MCP server for current API documentation. Used as a controlled, current-docs tool, not as project memory.
- **MCP** — Model Context Protocol. Anthropic's open standard for tool-server communication.
- **Codex** — OpenAI's coding agent CLI. Reads `AGENTS.md` at the repo root.
- **Claude Code** — Anthropic's coding agent. Reads `CLAUDE.md` (which imports `AGENTS.md` here).
- **LM Studio** — Local LLM runtime with GUI. Compatible with GGUF models and OpenAI-compatible API.
- **Ollama** — Local LLM runtime, CLI-first. Pulls quantized models on demand.
- **llama.cpp** — Reference C++ inference engine for LLaMA-family models. Backbone of LM Studio and Ollama.
- **vLLM** — High-throughput LLM inference server. GPU-focused. Used for batched serving experiments.
- **Qwen coder** — Alibaba's open-weight code-specialized model family. Default local-coding model in this workflow.
