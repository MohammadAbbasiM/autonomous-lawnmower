# Autonomous Robotic Lawn Mower

An open-source autonomous robotic lawn mower project developed at Iran University of Science and Technology (IUST).

## Overview

This project aims to develop a low-cost autonomous lawn mower capable of reliable outdoor navigation using sensor fusion and modern SLAM algorithms.

The long-term goal is to build a robust robotic platform that can operate in real-world gardens and lawns with minimal human intervention.

## System Architecture

- NVIDIA Jetson
- LiDAR
- RGB Camera
- GNSS Receiver
- IMU
- Differential Drive Platform
- ROS 2
  
```
RGB Camera
      \
LiDAR --> Sensor Fusion --> SLAM --> Navigation --> Motors
      /
GNSS + IMU
```

## Roadmap

### Market Research

- [x] Existing products survey
- [x] Sensor comparison
- [x] Price comparison
- [ ] Product requirements definition

### Phase 1 – Simulation
- [x] Select the SLAM framework
- [ ] Build a ROS2 simulation environment
- [ ] Evaluate the M3DGR dataset
- [ ] Benchmark localization accuracy

### Phase 2 – Hardware
- [ ] Design the robotic platform
- [ ] Integrate LiDAR, Camera, IMU and GNSS
- [ ] Implement localization on NVIDIA Jetson
- [ ] Implement autonomous navigation

### Phase 3 – Product
- [ ] Obstacle avoidance
- [ ] Lawn coverage planning
- [ ] Automatic docking and charging
- [ ] Field testing
- [ ] Performance optimization

## Technologies

- C++
- Python
- ROS2
- OpenCV
- CUDA
- SLAM
- Sensor Fusion
- GNSS
- NVIDIA Jetson

## Status

🚧 Early Development
