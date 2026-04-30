# Wiki Log

Append entries. Do not rewrite history.

## Entry template

### YYYY-MM-DD HH:MM

Action:
Source:
Pages created:
Pages updated:
Contradictions found (P0/P1/P2):
Open questions:
Next action:

---

### 2026-04-29 00:00

Action: Template initialized.
Source: project_context_template patched build.
Pages created: All wiki skeleton pages, plus fully-detailed `ur10e_ros2_grasshopper/pose_frame_rules.md` and `local_ai_workflow/context7_usage.md`.
Pages updated: index.md, health.md.
Contradictions found: None.
Open questions: None.
Next action: User to run `/ingest_raw` once raw material is added.

---

### 2026-04-29 14:40

Action: Built and documented a Level 1 WebSocket pose pipeline for Grasshopper-to-browser testing.
Source: User request plus official `websockets`, RhinoCommon, roslibpy, Cyberbotics/Webots, Bengesht, URDF, Polito thesis, and local PDF references.
Pages created: `ur10e_ros2_grasshopper/websocket_pose_pipeline.md`, `ur10e_ros2_grasshopper/reference_digest.md`.
Pages updated: `index.md`, `ur10e_ros2_grasshopper/overview.md`, `architecture.md`, `grasshopper_bridge.md`, `ros2_bridge.md`, `testing_checklist.md`, `open_questions.md`, `local_ai_workflow/context7_usage.md`, `project_management/decisions.md`, `project_management/risks.md`, `project_management/tasks.md`.
Contradictions found: None. Caveat: Food4Rhino page was reachable but not text-extractable, so GrasshopperDocs mirror was used for component details.
Open questions: First ROS2 target message type; Bengesht vs Rhino 8 ScriptEditor standard; simulator choice for Level 2.
Next action: Run the local receiver with `python outputs/2026-04-29/grasshopper_websocket_pose_pipeline/server.py` and test from Grasshopper.

---

### 2026-04-30 00:00

Action: Added user-provided UR10e/RG6 ROS2 GitHub repositories to the project knowledge base.
Source: GitHub repositories `ABC-iRobotics/onrobot-ros2`, `Zhengxuez/rg6_gripper_description`, `runtimerobotics/onrobot_rg2_ros2`, and `UniversalRobots/Universal_Robots_ROS2_Driver`.
Pages created: None.
Pages updated: `ur10e_ros2_grasshopper/reference_digest.md`, `ur10e_ros2_grasshopper/ros2_bridge.md`, `ur10e_ros2_grasshopper/ur10e_rg6_control.md`, `ur10e_ros2_grasshopper/overview.md`, `glossary.md`.
Contradictions found: None. Caveat: community OnRobot repositories are candidates only until commits, ROS2 distro compatibility, gripper firmware, and frame offsets are verified locally.
Open questions: Which RG6 ROS2 path should be tested first: ABC-iRobotics action/service controller, Runtime Robotics topic driver, or direct URCap/Modbus.
Next action: Bench-test one gripper integration path before connecting it to arm motion.

---

### 2026-04-30 00:00

Action: Added `Adventurous-Systems/topologicpy_MCP` to the project knowledge base.
Source: GitHub repository https://github.com/Adventurous-Systems/topologicpy_MCP.
Pages created: `local_ai_workflow/topologicpy_mcp.md`.
Pages updated: `index.md`, `local_ai_workflow/overview.md`, `graphml_baseline_comparison/overview.md`, `graphml_baseline_comparison/dataset_notes.md`, `glossary.md`.
Contradictions found: None. Caveat: this is recorded as a candidate MCP tool only, not an installed or validated project dependency.
Open questions: Should TopologicPy MCP be installed for a controlled smoke test, and should it become a GraphML preprocessing dependency or remain exploratory.
Next action: If requested, run a local install/smoke test and record commit, environment, prompts, and graph-output validation.

---

### 2026-04-30 00:00

Action: Added a standing compatibility rule for TopologicPy MCP against latest TopologicPy docs.
Source: User instruction plus latest TopologicPy docs at https://topologicpy.readthedocs.io/en/latest/topologicpy.html and `Adventurous-Systems/topologicpy_MCP` source files.
Pages created: None.
Pages updated: `local_ai_workflow/topologicpy_mcp.md`, `graphml_baseline_comparison/overview.md`, `graphml_baseline_comparison/dataset_notes.md`.
Contradictions found: Possible API drift: the MCP wrapper calls `Topology.ExportToIFC`, while TopologicPy `0.9.22` docs checked on 2026-04-30 did not list that API in the top-level Topology index. Treat IFC import/export paths as unverified until smoke-tested or patched.
Open questions: Should `topologicpy_MCP` be patched for current BIM/IFC export APIs before installation?
Next action: Before using TopologicPy MCP, check latest docs, record the docs version, pin the MCP commit and installed TopologicPy version, then run a minimal creation/query/graph/export smoke test.

---

### 2026-04-30 00:00

Action: Added a non-infringing 3D reconstruction knowledge page from the local Florent Poux PDF.
Source: Local PDF `3D Data Science with Python Building Accurate Digital Environments with 3D Point Cloud Workflows (Florent Poux).pdf`; metadata and outline inspected only.
Pages created: `3d_reconstruction/poux_3d_data_science_python.md`.
Pages updated: `index.md`, `glossary.md`.
Contradictions found: None. Copyright caveat: the full book was not converted or copied; the wiki page contains summaries, workflow checklists, and source pointers only.
Open questions: Which point cloud format and first reconstruction smoke test should become the project default.
Next action: If deeper notes are needed, summarize one chapter or workflow at a time without copying book text.

---

### 2026-04-30 00:00

Action: Restored curated 3D Data Science knowledge page and marked the full markdown extraction as a local source file.
Source: User-provided markdown extraction `3d_reconstruction/3d_data_science_python.md`.
Pages created: `3d_reconstruction/poux_3d_data_science_python.md`.
Pages updated: `3d_reconstruction/3d_data_science_python.md`, `log.md`.
Contradictions found: The index referenced `poux_3d_data_science_python.md`, but only the full extracted file existed. The curated page has been recreated.
Open questions: Which 3D reconstruction smoke test should be implemented first.
Next action: Use `poux_3d_data_science_python.md` for project knowledge; use `3d_data_science_python.md` only as a local source reference.

---

### 2026-04-30 00:00

Action: Added the first chapter-level study page for the 3D Data Science book notes.
Source: User request and local extraction `3d_reconstruction/3d_data_science_python.md`.
Pages created: `3d_reconstruction/chapter_01_intro_3d_data_science.md`.
Pages updated: `3d_reconstruction/poux_3d_data_science_python.md`, `index.md`, `log.md`.
Contradictions found: No distinct personal annotation markers were found in the extracted markdown, so the chapter page includes clean "My notes" placeholders for user annotations.
Open questions: Whether to continue with Chapter 2 or first annotate Chapter 1 manually.
Next action: Continue one chapter at a time, keeping each chapter page as summary, study questions, and project implications rather than copied book text.

---

### 2026-04-30 00:00

Action: Added study pages for all remaining chapters of the local 3D Data Science notes.
Source: User request and local extraction `3d_reconstruction/3d_data_science_python.md`.
Pages created: `3d_reconstruction/chapter_index.md`, `chapter_02_resources_software_essentials.md`, `chapter_03_python_3d_data_setup.md`, `chapter_04_data_representation_structuration.md`, `chapter_05_multimodal_3d_viewer.md`, `chapter_06_point_cloud_data_engineering.md`, `chapter_07_3d_analytical_apps.md`, `chapter_08_3d_data_analysis.md`, `chapter_09_3d_shape_recognition.md`, `chapter_10_advanced_3d_modeling.md`, `chapter_11_lidar_building_reconstruction.md`, `chapter_12_clustering.md`, `chapter_13_graphs_foundation_models.md`, `chapter_14_supervised_3d_ml.md`, `chapter_15_pytorch_3d_deep_learning.md`, `chapter_16_pointnet.md`, `chapter_17_workflow.md`, `chapter_18_spatial_ai.md`.
Pages updated: `3d_reconstruction/3d_reconstruction_knowledge_base.md`, `index.md`, `log.md`.
Contradictions found: None. The chapter pages are study summaries with personal-note slots, not a full book conversion.
Open questions: Which chapter should receive detailed personal annotations first.
Next action: Fill the `My notes` sections as the user reviews each chapter.

---

### 2026-04-30 00:00

Action: Renamed the curated 3D Data Science notes page to a clearer knowledge-base filename.
Source: User request.
Pages created: None.
Pages updated: `3d_reconstruction/3d_reconstruction_knowledge_base.md`, `3d_reconstruction/3d_data_science_python.md`, `3d_reconstruction/chapter_01_intro_3d_data_science.md`, `index.md`, `log.md`.
Contradictions found: None. Historical log entries still mention the old filename as history.
Open questions: None.
Next action: Use `3d_reconstruction/3d_reconstruction_knowledge_base.md` as the primary curated page.
