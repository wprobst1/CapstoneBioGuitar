import cv2
import mediapipe as mp
import time
import csv
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode

first_frame = True
times = []
next_index = 0
joint_count = 0

#puts all timestamps into list 
with open(r"MediaPipe\test.csv", newline='') as csvfile:   #change csv path as needed
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        times.append(float(row[0]))

header = ["Time", "Wx", "Wy", "Wz", "Tx", "Ty", "Tz", "Ix", "Iy", "Iz", "Mx", "My", "Mz", "Rx", "Ry", "Rz", "Px", "Py", "Pz"]
with open(r"MediaPipe\test_output.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=r"MediaPipe\hand_landmarker.task"),
    running_mode=RunningMode.IMAGE,
    num_hands=1
)

capture = cv2.VideoCapture(0)

with HandLandmarker.create_from_options(options) as landmarker:
    while capture.isOpened():
        ret, frame = capture.read()

        if first_frame: 
            start_time = time.perf_counter()
            first_frame = False
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
                cv2.circle(frame, (x_pix, y_pix), 3, (0, 255, 0), 1)   #draws circle at given pixels
                if joint_count % 4 == 0:
                    landmarks += [landmark.x, landmark.y, landmark.z]
                joint_count += 1

        if next_index < len(times) and (time.perf_counter() - start_time) >= times[next_index]: 
            with open(r"MediaPipe\test_output.csv", 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([times[next_index]] + landmarks)
            next_index += 1
                

        cv2.imshow("landmarks", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

capture.release()
cv2.destroyAllWindows()