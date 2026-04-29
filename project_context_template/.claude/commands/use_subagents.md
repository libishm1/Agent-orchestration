# /use_subagents <task>

Read CLAUDE.md.

Use specialist routing before editing.

Task: $ARGUMENTS

Workflow:
1. Use repo-archaeologist if relevant files are unclear.
2. Use api-doc-checker if current external APIs are involved.
3. Use robotics-reviewer for UR10e, RG6, ROS2, Grasshopper, URScript, IK/FK, or pose work.
4. Use graphml-reviewer for DGL, PyG, SVM, metrics, or dataset comparisons.
5. Use local-model-coordinator if the task must run offline, with Qwen, or across checkpoints.
6. Return one compact plan before editing.

Do not edit until the plan is clear.
