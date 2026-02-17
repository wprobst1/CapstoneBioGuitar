import pybullet as p
import pybullet_data
from time import sleep
import numpy as np

p.connect(p.GUI)
p.setGravity(0, 0, -10)
p.setAdditionalSearchPath(pybullet_data.getDataPath())  
p.loadURDF("plane.urdf")

# Load hand
objects = p.loadMJCF("./MPL/MPL.xml")
hand = objects[0]

# FIX 1: Keep hand floating in air (useFixedBase=True equivalent for MJCF)
# We need to create a fixed constraint
constraint = p.createConstraint(
    hand, -1, -1, -1, 
    p.JOINT_FIXED, 
    [0, 0, 0], 
    [0, 0, 0], 
    [0, 0, 0.5]  # Position in space
)

# Get joint info
num_joints = p.getNumJoints(hand)
print(f"\n{num_joints} joints in MPL hand:")
for i in range(num_joints):
    info = p.getJointInfo(hand, i)
    print(f"  Joint {i}: {info[1].decode()} - Range: {info[8]:.2f} to {info[9]:.2f}")

# FIX 2: Add sliders with proper range (PyBullet sliders work better with specific ranges)
sliders = []
for i in range(num_joints):
    info = p.getJointInfo(hand, i)
    if info[2] != p.JOINT_FIXED:  # Only movable joints
        lower = info[8]
        upper = info[9]
        
        # Make sure we have a valid range
        if lower == upper:
            lower = -1.5
            upper = 1.5
        
        slider = p.addUserDebugParameter(
            info[1].decode(),  # Joint name
            lower,             # Lower limit
            upper,             # Upper limit
            (lower + upper) / 2  # Start at middle position
        )
        sliders.append((i, slider))

print(f"\n{len(sliders)} sliders added. Use them to control the hand!")

# Control loop
while True:
    # Read sliders and control joints
    for joint_id, slider_id in sliders:
        target = p.readUserDebugParameter(slider_id)
        p.setJointMotorControl2(hand, joint_id, p.POSITION_CONTROL, target, force=5.0)
    
    p.stepSimulation()
    sleep(0.01)