import cv2
import mediapipe as mp
from process import sitting_desk

# Initialize mediapipe pose class.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def sendWarning(x):
    """
    Placeholder function for sending a warning.
    """
    pass

def process_frame(frame, fps, offset_threshold=100, neck_angle_threshold=25, torso_angle_threshold=10, time_threshold=180):
    """
    Processes a single frame to analyze posture and provides visual feedback.

    Parameters:
    - frame (numpy.ndarray): The input frame (BGR format) to be processed.
    - fps (float): Frames per second of the video stream.
    - offset_threshold (int, optional): Threshold for shoulder alignment. Default is 100.
    - neck_angle_threshold (int, optional): Threshold for neck inclination angle. Default is 25.
    - torso_angle_threshold (int, optional): Threshold for torso inclination angle. Default is 10.
    - time_threshold (int, optional): Time threshold (in seconds) for triggering an alert on bad posture. Default is 180.

    Returns:
    - numpy.ndarray: The processed frame with visual feedback.
    """

    # Font type.
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Colors.
    blue = (255, 127, 0)
    red = (50, 50, 255)
    green = (127, 255, 0)
    dark_blue = (127, 20, 0)
    light_green = (127, 233, 100)
    yellow = (0, 255, 255)
    pink = (255, 0, 255)
    white = (255, 255, 255)

    # Get height and width of the frame.
    h, w = frame.shape[:2]

    # Convert the BGR image to RGB.
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image.
    keypoints = pose.process(frame)

    # Convert the image back to BGR.
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Use lm and lmPose as representative of the following methods.
    lm = keypoints.pose_landmarks
    lmPose = mp_pose.PoseLandmark

    frame, good_frames, bad_frames = sitting_desk(frame,lm,lmPose,h,w,offset_threshold, neck_angle_threshold, torso_angle_threshold)

    # Calculate the time of remaining in a particular posture.
    good_time = (1 / fps) * good_frames
    bad_time = (1 / fps) * bad_frames

    # Pose time.
    if good_time > 0:
        time_string_good = 'Good Posture Time : ' + str(round(good_time, 1)) + 's'
        cv2.putText(frame, time_string_good, (10, h - 20), font, 0.9, green, 2)
    else:
        time_string_bad = 'Bad Posture Time : ' + str(round(bad_time, 1)) + 's'
        cv2.putText(frame, time_string_bad, (10, h - 20), font, 0.9, red, 2)

    # If you stay in bad posture for more than 3 minutes (180s) send an alert.
    if bad_time > time_threshold:
        sendWarning()
    
    return frame

