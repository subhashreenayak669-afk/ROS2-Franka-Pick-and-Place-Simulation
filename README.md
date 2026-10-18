# Autonomous Pick-and-Place Robotic Arm Simulation

An autonomous, collision-free pick-and-place manipulation system using the 7-DOF Franka Emika Panda robotic manipulator simulated natively within **ROS 2 Jazzy** and **MoveIt 2**.

---

## 🛠️ Tech Stack & Prerequisites
- **Operating System:** Ubuntu 24.04 LTS (x86_64)
- **Robotics Middleware:** ROS 2 Jazzy Jalisco
- **Motion Planning Framework:** MoveIt 2
- **Manipulator Model:** Franka Emika Panda (7-DOF Arm + 2-Finger Gripper)
- **Programming Language:** Python 3 (`rclpy`, `moveit_msgs`, `trajectory_msgs`)

---

## 🚀 Execution Instructions

### Terminal 1: Launch RViz 2 & MoveIt 2 Controllers
```bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
python3 add_scene.py && sleep 1 && python3 moveit_cartesian_task.py
