import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils  # Ref: https://github.com/google/mediapipe/blob/master/mediapipe/python/solutions/drawing_utils.py
mp_pose = mp.solutions.pose  # Ref: https://github.com/google/mediapipe/blob/master/docs/solutions/pose.md

cap = cv2.VideoCapture(0)

with mp_pose.Pose(
    static_image_mode = False, # The solution treats the input images as a video stream. Default: False.
    model_complexity = 1,  # Complexity of the pose landmark model: 0, 1 or 2. Default: 1.
    smooth_landmarks = True,  # The solution filters pose landmarks across different input images to reduce jitter. Default: True.
    enable_segmentation = True,  #  In addition to the pose landmarks the solution also generates the segmentation mask. Default: False.
    smooth_segmentation = True,  # The solution filters pose landmarks across different input images to reduce jitter. Default: True.
    min_detection_confidence = 0.4,  # Minimum confidence value ([0.0, 1.0]) from the person-detection model for the detection to be considered successful. Default to 0.5.
    min_tracking_confidence = 0.6 ) as pose:  # Minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the pose landmarks to be considered tracked successfully.  Setting it to a higher value can increase robustness of the solution, at the expense of a higher latency. Default to 0.5.
    
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            print("Ignoring empty camera frame.")
            break
        
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        frame.flags.writeable = False
        height, width, _ = frame.shape
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame)

        # Draw the pose annotation on the image.
        #frame.flags.writeable = True
        #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = np.ones_like(frame)* 255

        #frame =results.segmentation_mask
        #cv2.imshow('MediaPipe Pose',segmentation_mask)

        if results.pose_landmarks is not None:
            
            mp_drawing.draw_landmarks(
                frame, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(128, 0, 250), thickness=3, circle_radius=5),
                mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2))
            
            print(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width))

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Pose', cv2.flip(frame, 1))
        #cv2.imshow('MediaPipe Pose', cv2.flip(black_image, 1))
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()