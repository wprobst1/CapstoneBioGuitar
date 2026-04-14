import cv2
import mediapipe as mp
import time
import csv
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode
import numpy as np
import time
from adafruit_extended_bus import ExtendedI2C as I2C
from adafruit_pca9685 import PCA9685

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=r"MediaPipe\hand_landmarker.task"),
    running_mode=RunningMode.IMAGE,
    num_hands=1
)

i2c = I2C(7)
pca = PCA9685(i2c, address = 0x40)
pca.frequency = 50

FINGER_INDICES = {
    "thumb":  [1, 2, 3, 4],
    "index":  [5, 6, 7, 8],
    "middle": [9, 10, 11, 12],
    "ring":   [13, 14, 15, 16],
    "pinky":  [17, 18, 19, 20],
}

FINGER_CHANNELS = {
                "index":  15,
                "middle": 14,
                "ring":   13,
                "pinky":  12,
}

def angle_between(a, b, c):
    ba = np.array([a.x - b.x, a.y - b.y])
    bc = np.array([c.x - b.x, c.y - b.y])
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cos_angle, -1, 1)))

def get_finger_angles(hand_landmarks):
    angles = {}
    for name, idx in FINGER_INDICES.items():
        a = hand_landmarks[idx[0]]
        b = hand_landmarks[idx[1]]
        c = hand_landmarks[idx[3]]
        angles[name] = angle_between(a, b, c)
    return angles

def move(servo, pulse): #max is 8191 min is 1638, DO NOT EXCEED 7000
    pca.channels[servo].duty_cycle = pulse

def angle(angle):
    return int((angle) / (270) * (6553) + 1638)

capture = cv2.VideoCapture(0)

with HandLandmarker.create_from_options(options) as landmarker:
    while capture.isOpened():

        ret, frame = capture.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        results = landmarker.detect(mp_image)

        landmarks = []
        if results.hand_landmarks:
            hand = results.hand_landmarks[0]
            joint_count = 0
            for landmark in hand:     #loops over each of the 21 hand landmarks
                height, width, _ = frame.shape  #extracts height and width of camera frame
                x_pix, y_pix = int(landmark.x * width), int(landmark.y * height)    #converts landmark position (0-1) into pixel
                cv2.circle(frame, (x_pix, y_pix), 5, (0, 0, 0), -1)   #draws circle at given pixels
                if joint_count % 4 == 0:
                    landmarks += [landmark.x, landmark.y, landmark.z]
                joint_count += 1

            angles = get_finger_angles(hand)
            servo_positions = {name: angle(deg) for name, deg in angles.items()}

            for name, pwm in servo_positions.items():
                move(FINGER_CHANNELS[name], pwm) 

        pass