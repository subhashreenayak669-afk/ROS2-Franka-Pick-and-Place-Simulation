import rclpy
from rclpy.node import Node
from moveit_msgs.msg import PlanningScene, CollisionObject, ObjectColor
from shape_msgs.msg import SolidPrimitive
from geometry_msgs.msg import Pose
from std_msgs.msg import ColorRGBA
import time

if not rclpy.ok():
    rclpy.init()

node = Node('scene_publisher')
scene_pub = node.create_publisher(PlanningScene, '/planning_scene', 10)
time.sleep(1.0)

scene = PlanningScene()
scene.is_diff = True

# 1. Green Table (Video Dimensions)
table = CollisionObject()
table.header.frame_id = 'panda_link0'
table.id = 'table'
table_box = SolidPrimitive()
table_box.type = SolidPrimitive.BOX
table_box.dimensions = [0.6, 0.7, 0.4]
table_pose = Pose()
table_pose.position.x = 0.5
table_pose.position.y = 0.0
table_pose.position.z = 0.2
table_pose.orientation.w = 1.0
table.primitives.append(table_box)
table.primitive_poses.append(table_pose)
table.operation = CollisionObject.ADD

# 2. Target Purple Cube (Center of Table)
cube = CollisionObject()
cube.header.frame_id = 'panda_link0'
cube.id = 'target_cube'
cube_box = SolidPrimitive()
cube_box.type = SolidPrimitive.BOX
cube_box.dimensions = [0.05, 0.05, 0.08]
cube_pose = Pose()
cube_pose.position.x = 0.5
cube_pose.position.y = 0.0
cube_pose.position.z = 0.44
cube_pose.orientation.w = 1.0
cube.primitives.append(cube_box)
cube.primitive_poses.append(cube_pose)
cube.operation = CollisionObject.ADD

scene.world.collision_objects = [table, cube]

# Color styling
color_table = ObjectColor()
color_table.id = 'table'
color_table.color = ColorRGBA(r=0.2, g=0.8, b=0.2, a=1.0)

color_cube = ObjectColor()
color_cube.id = 'target_cube'
color_cube.color = ColorRGBA(r=0.6, g=0.1, b=0.9, a=1.0)

scene.object_colors = [color_table, color_cube]

for _ in range(3):
    scene_pub.publish(scene)
    time.sleep(0.3)

print("Scene setup: Table and purple cube added to environment.")
rclpy.shutdown()
