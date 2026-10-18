import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from moveit_msgs.msg import PlanningScene, AttachedCollisionObject, CollisionObject
import time

rclpy.init()
node = Node('smart_pick_place')

arm_pub = node.create_publisher(JointTrajectory, '/panda_arm_controller/joint_trajectory', 10)
hand_pub = node.create_publisher(JointTrajectory, '/panda_hand_controller/joint_trajectory', 10)
scene_pub = node.create_publisher(PlanningScene, '/planning_scene', 10)
time.sleep(1.0)

def attach_cube(attach=True):
    scene = PlanningScene()
    scene.is_diff = True
    obj = AttachedCollisionObject()
    obj.link_name = 'panda_hand'
    obj.object.id = 'target_cube'
    obj.object.header.frame_id = 'panda_hand'
    if attach:
        obj.object.operation = CollisionObject.ADD
        obj.touch_links = ['panda_hand', 'panda_leftfinger', 'panda_rightfinger']
    else:
        obj.object.operation = CollisionObject.REMOVE
    scene.robot_state.attached_collision_objects.append(obj)
    scene_pub.publish(scene)
    time.sleep(0.5)

def move_arm(positions, duration=3.0):
    msg = JointTrajectory()
    msg.joint_names = [
        'panda_joint1', 'panda_joint2', 'panda_joint3',
        'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7'
    ]
    pt = JointTrajectoryPoint()
    pt.positions = positions
    pt.time_from_start.sec = int(duration)
    pt.time_from_start.nanosec = int((duration - int(duration)) * 1e9)
    msg.points.append(pt)
    arm_pub.publish(msg)
    time.sleep(duration + 0.8)

def move_hand(pos, duration=1.0):
    msg = JointTrajectory()
    msg.joint_names = ['panda_finger_joint1', 'panda_finger_joint2']
    pt = JointTrajectoryPoint()
    pt.positions = [pos, pos]
    pt.time_from_start.sec = int(duration)
    msg.points.append(pt)
    hand_pub.publish(msg)
    time.sleep(duration + 0.5)

# 1. Open gripper
print("1. Opening gripper...")
move_hand(0.04)

# 2. Move directly above cube (Pre-grasp)
print("2. Moving straight above cube...")
move_arm([0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785], duration=3.0)

# 3. Lower onto cube
print("3. Lowering onto cube...")
move_arm([0.0, -0.45, 0.0, -2.65, 0.0, 2.20, 0.785], duration=2.5)

# 4. Grasp
print("4. Grasping cube...")
move_hand(0.01)
attach_cube(True)

# 5. Lift up
print("5. Lifting cube vertically...")
move_arm([0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785], duration=2.5)

# 6. Move to side drop location
print("6. Moving to drop location...")
move_arm([0.85, -0.70, 0.0, -2.20, 0.0, 1.571, 0.785], duration=3.0)

# 7. Release
print("7. Releasing cube...")
move_hand(0.04)
attach_cube(False)

print("=== Pick and Place Completed Successfully! ===")
rclpy.shutdown()
