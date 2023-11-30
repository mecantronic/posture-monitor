import math as m
import cv2

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

def sitting_process(frame, lm,lmPose,h,w,offset_threshold, neck_angle_threshold, torso_angle_threshold):
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

    # Left ear.
    l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
    l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)

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
    neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
    torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

    # Draw landmarks.
    cv2.circle(frame, (l_shldr_x, l_shldr_y), 7, white, 2)
    cv2.circle(frame, (l_ear_x, l_ear_y), 7, white, 2)

    # Let's take y - coordinate of P3 100px above x1,  for display elegance.
    # Although we are taking y = 0 while calculating angle between P1,P2,P3.
    cv2.circle(frame, (l_shldr_x, l_shldr_y - 100), 7, white, 2)
    cv2.circle(frame, (r_shldr_x, r_shldr_y), 7, pink, -1)
    cv2.circle(frame, (l_hip_x, l_hip_y), 7, yellow, -1)

    # Similarly, here we are taking y - coordinate 100px above x1. Note that
    # you can take any value for y, not necessarily 100 or 200 pixels.
    cv2.circle(frame, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

    # Put text, Posture and angle inclination.
    # Text string for display.
    angle_text_string_neck = 'Neck inclination: ' + str(int(neck_inclination))
    angle_text_string_torso = 'Torso inclination: ' + str(int(torso_inclination))

    # Determine whether good posture or bad posture.
    # The threshold angles have been set based on intuition.
    if neck_inclination < neck_angle_threshold and torso_inclination < torso_angle_threshold:
        bad_frames = 0
        good_frames += 1

        cv2.putText(frame, angle_text_string_neck, (10, 30), font, 0.6, light_green, 2)
        cv2.putText(frame, angle_text_string_torso, (10, 60), font, 0.6, light_green, 2)
        cv2.putText(frame, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
        cv2.putText(frame, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)

        # Join landmarks.
        cv2.line(frame, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 2)
        cv2.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 2)
        cv2.line(frame, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 2)
        cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 2)

    else:
        good_frames = 0
        bad_frames += 1

        cv2.putText(frame, angle_text_string_neck, (10, 30), font, 0.6, red, 2)
        cv2.putText(frame, angle_text_string_torso, (10, 60), font, 0.6, red, 2)
        cv2.putText(frame, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
        cv2.putText(frame, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)

        # Join landmarks.
        cv2.line(frame, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 2)
        cv2.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 2)
        cv2.line(frame, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 2)
        cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 2)
    
    return frame, good_frames, bad_frames

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