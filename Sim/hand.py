import pybullet as pb
import pybullet_data
from time import sleep
import math

physicsClient = pb.connect(pb.GUI)
pb.setGravity(0, 0, -9.81) #Earth Gravity
pb.setAdditionalSearchPath(pybullet_data.getDataPath())
pb.loadURDF("plane.urdf")

models = pb.loadMJCF("./MPL/MPL.xml")
hand = models[0]

constraint = pb.createConstraint(
    parentBodyUniqueId=hand,
    parentLinkIndex=-1,   
    childBodyUniqueId=-1,  
    childLinkIndex=-1,
    jointType=pb.JOINT_FIXED,
    jointAxis=[0, 0, 0],
    parentFramePosition=[0, 0, 0],
    childFramePosition=[0, 0, 0.5] 
)

pb.resetDebugVisualizerCamera(cameraDistance=0.5, cameraYaw=45, cameraPitch=-20, cameraTargetPosition=[0, 0, 0.5])

def degToRad(degrees):
    return (degrees * math.pi) / 180.0

sliders = {}
nameIndex = {}

ROM_LIMITS = {
    # Wrist
    "wrist_PRO":    (degToRad(-140.0), degToRad(60.0)),
    "wrist_UDEV":   (degToRad(-10.0), degToRad(17.0)),
    "wrist_FLEX":   (degToRad(-40.0), degToRad(70.0)),
    # Thumb
    "thumb_ABD":    (degToRad(-7.5), degToRad(7.5)),
    "thumb_MCP":    (degToRad(0.0), degToRad(90.0)),
    "thumb_PIP":    (degToRad(0.0), degToRad(120.0)),
    "thumb_DIP":    (degToRad(0.0), degToRad(80.0)),
    # Index
    "index_ABD":    (degToRad(-7.5), degToRad(7.5)),
    "index_MCP":    (degToRad(0.0), degToRad(90.0)),
    "index_PIP":    (degToRad(0.0), degToRad(120.0)),
    "index_DIP":    (degToRad(0.0), degToRad(80.0)),
    # Middle
    "middle_ABD":   (degToRad(-7.5), degToRad(7.5)),
    "middle_MCP":   (degToRad(0.0), degToRad(90.0)),
    "middle_PIP":   (degToRad(0.0), degToRad(120.0)),
    "middle_DIP":   (degToRad(0.0), degToRad(80.0)),
    # Ring
    "ring_ABD":     (degToRad(-7.5), degToRad(7.5)),
    "ring_MCP":     (degToRad(0.0), degToRad(90.0)),
    "ring_PIP":     (degToRad(0.0), degToRad(120.0)),
    "ring_DIP":     (degToRad(0.0), degToRad(80.0)),
    # Pinky
    "pinky_ABD":    (degToRad(-7.5), degToRad(7.5)),
    "pinky_MCP":    (degToRad(0.0), degToRad(90.0)),
    "pinky_PIP":    (degToRad(0.0), degToRad(120.0)),
    "pinky_DIP":    (degToRad(0.0), degToRad(80.0)),
}

for i in range(pb.getNumJoints(hand)):
    info = pb.getJointInfo(hand, i)
    type = info[2]
    jointName = info[1].decode()
    nameIndex[info[1].decode()] = i

    if type == pb.JOINT_FIXED:
        continue
    if jointName in ROM_LIMITS:
        lower, upper = ROM_LIMITS[jointName]
    
    q0 = pb.getJointState(hand, i)[0]


    sliderID = pb.addUserDebugParameter(jointName, lower, upper, q0)
    sliders[jointName] = sliderID

while True:
    for name, sliderID in sliders.items():
        angle = pb.readUserDebugParameter(sliderID)
        pb.resetJointState(hand, nameIndex[name], angle)

    pb.stepSimulation()
    sleep(0.01)