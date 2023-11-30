import cv2
import mediapipe as mp
import numpy as np
import math as m
from tqdm import tqdm

# Colors.
blue = (255, 127, 0)
red = (50, 50, 255)
green = (127, 255, 0)
dark_blue = (127, 20, 0)
light_green = (127, 233, 100)
yellow = (0, 255, 255)
pink = (255, 0, 255)
white = (255, 255, 255)

# Font type.
font = cv2.FONT_HERSHEY_SIMPLEX

def decant_process (frame, lm,lmPose,h,w,offset_threshold, shoulder_angle_threshold, elbow_angle_threshold):
    """
    Analyzes the posture of a person sitting at a desk and provides visual feedback.

    Parameters:
    - frame (numpy.ndarray): The input frame (BGR format) to be processed.
    - lm: Landmarks detected by the model (e.g., Mediapipe landmarks).
    - lmPose: Type of landmarks specific to pose analysis.
    - h (int): Height of the frame.
    - w (int): Width of the frame.
    - offset_threshold (int): Threshold for shoulder alignment.
    - neck_angle_threshold (int): Threshold for neck inclination angle.
    - torso_angle_threshold (int): Threshold for torso inclination angle.

    Returns:
    - numpy.ndarray: The processed frame with visual feedback.
    - int: Counter for frames with good posture.
    - int: Counter for frames with bad posture.
    """

    # Initialize frame counters.
    good_frames = 0
    bad_frames = 0

    # Left shoulder.
    l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
    l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)

    # Right shoulder.
    r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
    r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

    # Left ELBOW.
    l_elbow_x = int(lm.landmark[lmPose.LEFT_ELBOW].x * w)
    l_elbow_y = int(lm.landmark[lmPose.LEFT_ELBOW].y * h)

    # Left WRIST.
    l_wrist_x = int(lm.landmark[lmPose.LEFT_WRIST].x * w)
    l_wrist_y = int(lm.landmark[lmPose.LEFT_WRIST].y * h)

    # Left hip.
    l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
    l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

    # Calculate distance between left shoulder and right shoulder points.
    offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

    # Assist to align the camera to point at the side view of the person.
    # Offset threshold 30 is based on results obtained from analysis over 100 samples.
    if offset < offset_threshold:
        cv2.putText(frame, str(int(offset)) + ' Shoulders aligned', (w - 280, 30), font, 0.6, green, 2)
    else:
        cv2.putText(frame, str(int(offset)) + ' Shoulders not aligned', (w - 280, 30), font, 0.6, red, 2)

    # Calculate angles.
    shoulder_inclination = findAngle(l_elbow_x, l_elbow_y, l_shldr_x, l_shldr_y)
    elbow_inclination = findAngle(l_elbow_x, l_elbow_y, l_wrist_x, l_wrist_y)
    #torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

    # Draw landmarks.
    cv2.circle(frame, (l_shldr_x, l_shldr_y), 7, white, 2)
    cv2.circle(frame, (l_elbow_x, l_elbow_y), 7, white, 2)
    cv2.circle(frame, (l_wrist_x, l_wrist_y), 7, white, 2)

    # Let's take y - coordinate of P3 100px above x1,  for display elegance.
    # Although we are taking y = 0 while calculating angle between P1,P2,P3.
    #cv2.circle(frame, (l_shldr_x, l_shldr_y - 100), 7, white, 2)
    cv2.circle(frame, (r_shldr_x, r_shldr_y), 7, pink, -1)
    cv2.circle(frame, (l_hip_x, l_hip_y), 7, yellow, -1)

    # Similarly, here we are taking y - coordinate 100px above x1. Note that
    # you can take any value for y, not necessarily 100 or 200 pixels.
    #cv2.circle(frame, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

    # Put text, Posture and angle inclination.
    # Text string for display.
    angle_text_string_shoulder = 'Shoulder inclination: ' + str(int(shoulder_inclination))
    angle_text_string_elbow = 'Elbow inclination: ' + str(int(elbow_inclination))
    #angle_text_string_torso = 'Torso inclination: ' + str(int(torso_inclination))

    # Determine whether good posture or bad posture.
    # The threshold angles have been set based on intuition.
    #if neck_inclination < neck_angle_threshold and torso_inclination < torso_angle_threshold:
    if elbow_inclination < elbow_angle_threshold[1] and elbow_inclination > elbow_angle_threshold[0]:
        bad_frames = 0
        good_frames += 1

        #cv2.putText(frame, angle_text_string_shoulder, (10, 30), font, 0.6, light_green, 2)
        cv2.putText(frame, angle_text_string_elbow, (10, 60), font, 0.6, light_green, 2)
        #cv2.putText(frame, str(int(shoulder_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
        cv2.putText(frame, str(int(elbow_inclination)), (l_elbow_x + 10, l_elbow_y), font, 0.9, light_green, 2)

        # Join landmarks.
        cv2.line(frame, (l_shldr_x, l_shldr_y), (l_elbow_x, l_elbow_y), green, 2)
        #cv2.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 2)
        #cv2.line(frame, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 2)
        #cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 2)
        cv2.line(frame, (l_wrist_x, l_wrist_y), (l_elbow_x, l_elbow_y), green, 2)
        #cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 2)
    else:
        good_frames = 0
        bad_frames += 1

        #cv2.putText(frame, angle_text_string_shoulder, (10, 30), font, 0.6, red, 2)
        cv2.putText(frame, angle_text_string_elbow, (10, 60), font, 0.6, red, 2)
        #cv2.putText(frame, str(int(shoulder_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
        #cv2.putText(frame, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)
        cv2.putText(frame, str(int(elbow_inclination)), (l_elbow_x + 10, l_elbow_y), font, 0.9, red, 2)

        # Join landmarks.
        cv2.line(frame, (l_shldr_x, l_shldr_y), (l_elbow_x, l_elbow_y), red, 2)
        #cv2.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 2)
        #cv2.line(frame, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 2)
        #cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 2)
        cv2.line(frame, (l_wrist_x, l_wrist_y), (l_elbow_x, l_elbow_y), red, 2)
   
    if shoulder_inclination > 0 and shoulder_inclination < shoulder_angle_threshold[0]:
        bad_frames = 0
        good_frames += 1

        cv2.putText(frame, angle_text_string_shoulder, (10, 30), font, 0.6, light_green, 2)
        #cv2.putText(frame, angle_text_string_elbow, (10, 60), font, 0.6, light_green, 2)
        cv2.putText(frame, str(int(shoulder_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
        #cv2.putText(frame, str(int(elbow_inclination)), (l_elbow_x + 10, l_elbow_y), font, 0.9, light_green, 2)

        # Join landmarks.
        cv2.line(frame, (l_shldr_x, l_shldr_y), (l_elbow_x, l_elbow_y), green, 2)
        #cv2.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 2)
        cv2.line(frame, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 2)
        #cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 2)
        #cv2.line(frame, (l_wrist_x, l_wrist_y), (l_elbow_x, l_elbow_y), green, 2)
        #cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 2)
    elif shoulder_inclination > shoulder_angle_threshold[0] and shoulder_inclination < shoulder_angle_threshold[1]:
        bad_frames = 0
        good_frames += 1

        cv2.putText(frame, angle_text_string_shoulder, (10, 30), font, 0.6, yellow, 2)
        #cv2.putText(frame, angle_text_string_elbow, (10, 60), font, 0.6, light_green, 2)
        cv2.putText(frame, str(int(shoulder_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, yellow, 2)
        #cv2.putText(frame, str(int(elbow_inclination)), (l_elbow_x + 10, l_elbow_y), font, 0.9, light_green, 2)

        # Join landmarks.
        cv2.line(frame, (l_shldr_x, l_shldr_y), (l_elbow_x, l_elbow_y), yellow, 2)
        #cv2.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 2)
        cv2.line(frame, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), yellow, 2)
        #cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 2)
        #cv2.line(frame, (l_wrist_x, l_wrist_y), (l_elbow_x, l_elbow_y), green, 2)
        #cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 2)
    else:
        good_frames = 0
        bad_frames += 1

        cv2.putText(frame, angle_text_string_shoulder, (10, 30), font, 0.6, red, 2)
        #cv2.putText(frame, angle_text_string_elbow, (10, 60), font, 0.6, red, 2)
        cv2.putText(frame, str(int(shoulder_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
        #cv2.putText(frame, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)
        #cv2.putText(frame, str(int(elbow_inclination)), (l_elbow_x + 10, l_elbow_y), font, 0.9, red, 2)

        # Join landmarks.
        cv2.line(frame, (l_shldr_x, l_shldr_y), (l_elbow_x, l_elbow_y), red, 2)
        #cv2.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 2)
        cv2.line(frame, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 2)
        #cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 2)
        #cv2.line(frame, (l_wrist_x, l_wrist_y), (l_elbow_x, l_elbow_y), red, 2)
    
    return frame, good_frames, bad_frames

def findDistance(x1, y1, x2, y2):
    """
    Calculate the Euclidean distance between two points.

    Args:
        x1, y1: Coordinates of the first point.
        x2, y2: Coordinates of the second point.

    Returns:
        Distance between the two points.
    """
    dist = m.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    return dist

def findAngle(x1, y1, x2, y2):
    """
    Calculate the angle between two points with respect to the y-axis.

    Args:
        x1, y1: Coordinates of the first point.
        x2, y2: Coordinates of the second point.

    Returns:
        Angle in degrees.
    """
    # Verificar si y1 es cero para evitar la división por cero
    if y1 == 0:
        return 0  # Otra opción es devolver un valor especial para indicar infinito
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1))
    degree = int(180/m.pi) * theta
    
    return degree

mp_drawing = mp.solutions.drawing_utils  # Ref: https://github.com/google/mediapipe/blob/master/mediapipe/python/solutions/drawing_utils.py
mp_pose = mp.solutions.pose  # Ref: https://github.com/google/mediapipe/blob/master/docs/solutions/pose.md

cap = cv2.VideoCapture("static/assets/test-videos/Test_1.mp4")
fps = cap.get(cv2.CAP_PROP_FPS) # Get fps.
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames in the video
width = int(cap.get(3))
height = int(cap.get(4))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter('processing/downloads/video_output.mp4', fourcc, fps, (width, height))

with mp_pose.Pose(
    static_image_mode = False, # The solution treats the input images as a video stream. Default: False.
    model_complexity = 1,  # Complexity of the pose landmark model: 0, 1 or 2. Default: 1.
    smooth_landmarks = True,  # The solution filters pose landmarks across different input images to reduce jitter. Default: True.
    enable_segmentation = True,  #  In addition to the pose landmarks the solution also generates the segmentation mask. Default: False.
    smooth_segmentation = True,  # The solution filters pose landmarks across different input images to reduce jitter. Default: True.
    min_detection_confidence = 0.5,  # Minimum confidence value ([0.0, 1.0]) from the person-detection model for the detection to be considered successful. Default to 0.5.
    min_tracking_confidence = 0.5 ) as pose:  # Minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the pose landmarks to be considered tracked successfully.  Setting it to a higher value can increase robustness of the solution, at the expense of a higher latency. Default to 0.5.
    
    # Use tqdm to create a progress bar
    with tqdm(total=total_frames, desc="Processing frames") as pbar:
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
            
            # Apply inference to the frame
            results = pose.process(frame)

            # Draw the pose annotation on the image.
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = np.ones_like(frame)* 0

            #frame =results.segmentation_mask
            #cv2.imshow('MediaPipe Pose',segmentation_mask)
            
            # Use lm and lmPose as representative of the following methods.
            lm = results.pose_landmarks
            lmPose = mp_pose.PoseLandmark

            if results.pose_landmarks is not None:
                frame, good_frames, bad_frames = decant_process(frame,lm,lmPose,height, width,offset_threshold=100, shoulder_angle_threshold=(20,60), elbow_angle_threshold=(60,100))
                ''' METHOD TO DRAW Under Test
                mp_drawing.draw_landmarks(
                    frame, 
                    results.pose_landmarks, 
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(128, 0, 250), thickness=3, circle_radius=5),
                    mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2))
                '''
            # Calculate the time of remaining in a particular posture.
                good_time = (1 / fps) * good_frames
                bad_time = (1 / fps) * bad_frames

                # Pose time.
                if good_time > 0:
                    time_string_good = 'Good Posture Time : ' + str(round(good_time, 1)) + 's'
                    cv2.putText(frame, time_string_good, (10, height - 20), font, 0.9, green, 2)
                else:
                    time_string_bad = 'Bad Posture Time : ' + str(round(bad_time, 1)) + 's'
                    cv2.putText(frame, time_string_bad, (10, height - 20), font, 0.9, red, 2)
                
                # Flip the image horizontally for a selfie-view display.
                cv2.imshow('MediaPipe Pose', frame)
                #cv2.imshow('MediaPipe Pose', cv2.flip(black_image, 1))
                if cv2.waitKey(1) & 0xFF == 27:
                    break

                out.write(frame)
                pbar.update(1)  # Update the tqdm progress bar
        cap.release()
        out.release()
cv2.destroyAllWindows()

