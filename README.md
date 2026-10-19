# Autonomous Robotic Lawn Mower (ROS 2 Navigation & SLAM Stack)

![ROS 2](https://img.shields.io/badge/ROS_2-Humble%20%2F%20Jazzy-blue)
![Platform](https://img.shields.io/badge/Target_Compute-NVIDIA_Jetson-76B900)
![Simulation](https://img.shields.io/badge/Simulation-Gazebo-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An open-source, **simulation-first** autonomous navigation and coverage planning software stack for robotic lawn mowers, developed at **Iran University of Science and Technology (IUST)**.

## Overview

This project focuses on designing and validating a robust, low-cost autonomous software stack capable of reliable outdoor localization and full-area coverage in unstructured garden environments. 

Adopting a **Simulation-First & Edge-Ready** methodology, the entire perception, multi-sensor fusion, SLAM, and coverage path planning pipeline is rigorously evaluated using real-world field datasets (**M3DGR**) and high-fidelity physics simulation (**Gazebo**). The software architecture is strictly constrained and profiled for seamless deployment on embedded edge compute platforms (**NVIDIA Jetson Orin** series) using standard hardware abstraction (`ros2_control`).

---

## System Architecture

The software pipeline decouples high-level autonomy from low-level actuation using `ros2_control`, ensuring that the exact same codebase runs in Gazebo simulation and on physical embedded hardware.

### Target Compute & Sensor Suite (Simulated & Dataset-Backed)
- **Edge Compute Target:** NVIDIA Jetson Orin Nano (8GB)
- **Exteroceptive Sensors:** 3D/2D LiDAR, RGB Camera, RTK-GNSS Receiver
- **Proprioceptive Sensors:** 9-DOF IMU, Wheel Quadrature Encoders
- **Actuation Interface:** Differential Drive (`diff_drive_controller` via `ros2_control`)

### Autonomy Pipeline (ROS 2)

```text
[Wheel Encoders] + [IMU] ──> [Local EKF (odom -> base_link)] ──┐
                                                               ├──> [Nav2 & Fields2Cover] ──> [ros2_control]
[LiDAR] + [RGB Camera] ────> [SLAM / Visual-LiDAR Odometry] ───┤     (Boustrophedon Coverage    │
                                                               │      & Obstacle Avoidance)     ├──> [Gazebo Sim]
[GNSS Receiver] ───────────> [Global EKF (map -> odom)] ───────┘                                └──> [Physical Hardware]
```

---

## Repository Structure

```text
autonomous-lawnmower-IUST/
├── docs/                       # System specifications, sensor survey & PRD
│   └── product_requirements.md # System & Software Requirements Document
├── lawnmower_description/      # Robot URDF/Xacro, sensor frames & meshes
├── lawnmower_gazebo/           # Gazebo simulation worlds, launch files & plugins
├── lawnmower_localization/     # Dual-EKF configs (robot_localization) & SLAM integration
├── lawnmower_navigation/       # Nav2 stack & Fields2Cover coverage path planning
└── README.md
```

---

## Roadmap

### Phase 1 – Research & System Specification
- [x] Existing commercial products survey
- [x] Sensor suite & compute price/performance comparison
- [x] Select the core SLAM framework
- [x] [Product & Software Requirements Definition (PRD)](docs/product_requirements.md)

### Phase 2 – Dataset Benchmarking & Localization
- [ ] Evaluate the selected SLAM framework on the **M3DGR** outdoor lawn dataset
- [ ] Benchmark localization accuracy (ATE / RPE metrics using `evo`)
- [ ] Configure Dual-EKF sensor fusion (`robot_localization`) for IMU, Wheel Odometry, and GNSS

### Phase 3 – Simulation & Autonomous Coverage
- [ ] Build the differential drive robot URDF and Gazebo lawn environment
- [ ] Integrate simulated sensors with realistic Gaussian noise profiles
- [ ] Implement full-area lawn coverage planning (**Nav2** + **Fields2Cover**)
- [ ] Validate dynamic obstacle avoidance during active coverage missions

### Phase 4 – Edge Readiness & Profiling (NVIDIA Jetson Target)
- [ ] Containerize the autonomy stack using Docker (ARM64 / L4T compatible)
- [ ] Profile CPU, GPU, and RAM utilization against Jetson Orin Nano compute budgets
- [ ] Hardware-in-the-Loop (HIL) / Physical platform integration *(Optional Future Extension)*

---

## Technologies & Tools

- **Core:** C++, Python, ROS 2
- **Simulation:** Gazebo, RViz2, URDF/Xacro
- **Localization & Mapping:** LiDAR-Inertial SLAM, `robot_localization` (Dual-EKF), `navsat_transform`
- **Navigation & Planning:** Nav2, Fields2Cover (Coverage Path Planning)
- **Perception & Compute:** OpenCV, PCL (Point Cloud Library), CUDA, Docker
- **Benchmarking:** `evo` (Trajectory Evaluation), M3DGR Dataset

---

## Status

🚧 **Active Development** — Currently benchmarking SLAM localization on the M3DGR dataset and setting up the Gazebo simulation environment.
