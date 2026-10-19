
# System & Software Requirements Specification (PRD)

**Project:** Autonomous Robotic Lawn Mower (Software & Simulation Stack)  
**Institution:** Iran University of Science and Technology (IUST)  
**Design Methodology:** Simulation-First, Edge-Compute Ready (NVIDIA Jetson Target)

---

## 1. Objective & Scope

The primary objective of this project is to develop, simulate, and benchmark a complete ROS 2 autonomy stack for an outdoor robotic lawn mower. While the validation is conducted in high-fidelity simulation (**Gazebo**) and against real-world outdoor robotics datasets (**M3DGR**), all algorithmic choices and architectural interfaces are strictly constrained to run in real-time on an embedded **NVIDIA Jetson** platform without code modification.

---

## 2. Operational & Kinematic Assumptions (Simulated Platform)

To ensure realistic simulation physics and path planning constraints, the virtual robot model adheres to the following physical envelope:

| Parameter | Target Specification | Rationale / Impact on Software |
| :--- | :--- | :--- |
| **Drive Kinematics** | Differential Drive (2 driven wheels + 2 caster wheels) | Compatible with `diff_drive_controller` in `ros2_control`. |
| **Footprint (L × W × H)** | `650 mm × 450 mm × 300 mm` | Defines the robot polygon for Nav2 local and global costmaps. |
| **Cutting Deck Width** | `280 mm` | Determines the swath width and overlap percentage in Coverage Path Planning. |
| **Max Linear Velocity** | `0.6 m/s` (Mowing) / `1.0 m/s` (Transit) | Constrains controller velocity limits and sensor motion-blur/skew bounds. |
| **Max Angular Velocity** | `1.2 rad/s` | Prevents grass tearing during zero-radius turns in simulation/reality. |
| **Max Traversable Slope** | `15° (~27% grade)` | Requires 6-DOF IMU integration and 3D terrain-aware localization. |

---

## 3. Sensor Suite Specifications (Simulation & Dataset Equivalents)

The software pipeline expects the following sensor topics and noise profiles:

1. **3D LiDAR**
   - **Update Rate:** `10 Hz`
   - **Range:** `0.3 m` to `30.0 m`
   - **Role:** Primary input for LiDAR-Inertial Odometry/SLAM and 3D obstacle detection.
2. **IMU (9-DOF)**
   - **Update Rate:** `100 Hz – 200 Hz`
   - **Role:** High-rate state estimation, LiDAR deskewing, and Local EKF orientation fusion.
3. **RTK-GNSS Receiver**
   - **Update Rate:** `5 Hz – 10 Hz`
   - **Simulated Accuracy:** `±0.02 m` (RTK Fixed) to `±1.5 m` (Degraded/Multipath)
   - **Role:** Drift-free global position anchoring in open, featureless lawn areas.
4. **RGB Camera**
   - **Resolution / FPS:** `1280×720 @ 30 FPS`
   - **Role:** Visual loop closure, semantic grass/obstacle segmentation (future extension).
5. **Wheel Encoders**
   - **Update Rate:** `50 Hz` (via `ros2_control` joint states)
   - **Role:** Dead-reckoning velocity feedback for Local EKF.

---

## 4. Functional Software Requirements

### 4.1. State Estimation & Localization
- **Dual-EKF Architecture:** The system must maintain a smooth, continuous local frame (`odom -> base_link`) fusing wheel odometry and IMU at `≥50 Hz`, and an accurate global frame (`map -> odom`) fusing SLAM and GNSS data.
- **Feature-Poor Resilience:** The localization pipeline must smoothly transition between LiDAR-dominant SLAM (near trees, walls, and fences) and GNSS/Odometry-dominant fusion (in wide-open, featureless grass fields).
- **Accuracy Target:**
  - **Absolute Trajectory Error (ATE):** `< 0.08 m` RMS (to ensure overlapping mowing stripes without missed patches).
  - **Relative Pose Error (RPE):** `< 0.03 m` per meter traveled.

### 4.2. Coverage Path Planning & Navigation
- **Swath Generation:** Given a closed 2D polygon boundary of a lawn and static obstacle polygons, the planner must generate an optimal Boustrophedon (zig-zag) coverage path with a configurable stripe overlap (`10% – 15%`).
- **Path Following Accuracy:** Cross-track error during straight-line mowing must remain `< 0.05 m` on flat terrain.
- **Dynamic Obstacle Avoidance:** Upon detecting an unexpected obstacle within the mowing corridor, the local planner must safely deviate around the obstacle and rejoin the subsequent coverage swath without aborting the mission.

---

## 5. Edge-Readiness & Computational Constraints (NVIDIA Jetson Target)

To guarantee that the simulated software stack can be deployed onto an **NVIDIA Jetson Orin Nano (8GB RAM, 6-core ARM Cortex-A78AE)**, the software must satisfy the following non-functional requirements:

| Metric | Target Budget (Desktop / Sim Equivalent) | Edge Deployment Strategy |
| :--- | :--- | :--- |
| **CPU Utilization (Autonomy Stack)** | `< 60%` across 4 threads (excluding Gazebo GUI) | Implement core SLAM and point-cloud filtering in **C++** using multi-threading. |
| **Memory (RAM) Footprint** | `< 3.5 GB` total for all ROS 2 nodes | Bound sliding-window map sizes and downsample point clouds (`VoxelGrid` filter). |
| **Control Loop Latency** | `< 20 ms` (Perception to `cmd_vel`) | Use ROS 2 Intra-Process Communication / Composable Nodes where applicable. |
| **Hardware Abstraction** | 100% decoupled via `ros2_control` | Switching from Gazebo to physical MCU requires only swapping the URDF hardware plugin. |
