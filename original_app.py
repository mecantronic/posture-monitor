# Ref: https://learnopencv.com/building-a-body-posture-analysis-system-using-mediapipe/

import cv2
import time
import math as m
import mediapipe as mp
import argparse

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

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
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1))
    degree = int(180/m.pi) * theta
    return degree

def sendWarning(x):
    """
    Placeholder function for sending a warning.
    """
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(description='Posture Monitor with MediaPipe')
    parser.add_argument('--video', type=str, default=0, help='Path to the input video file. If not provided, the webcam will be used.')
    parser.add_argument('--offset-threshold', type=int, default=100, help='Threshold value for shoulder alignment.')
    parser.add_argument('--neck-angle-threshold', type=int, default=25, help='Threshold value for neck inclination angle.')
    parser.add_argument('--torso-angle-threshold', type=int, default=10, help='Threshold value for torso inclination angle.')
    parser.add_argument('--time-threshold', type=int, default=180, help='Time threshold for triggering a posture alert.')
    return parser.parse_args()

def main(video_path=None, offset_threshold=100, neck_angle_threshold=25, torso_angle_threshold=10, time_threshold=180):
    # Initialize frame counters.
    good_frames = 0
    bad_frames = 0

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

    # Initialize mediapipe pose class.
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # For file input, replace file name with <path>.
    cap = cv2.VideoCapture(video_path) if video_path else cv2.VideoCapture(0)

    # Meta.
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    while True:
        # Capture frames.
        success, image = cap.read()
        if not success:
            print("Null.Frames")
            break

        # Get fps.
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Get height and width of the frame.
        h, w = image.shape[:2]

        # Convert the BGR image to RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image.
        keypoints = pose.process(image)

        # Convert the image back to BGR.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Use lm and lmPose as representative of the following methods.
        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark

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
            cv2.putText(image, str(int(offset)) + ' Shoulders aligned', (w - 280, 30), font, 0.6, green, 2)
        else:
            cv2.putText(image, str(int(offset)) + ' Shoulders not aligned', (w - 280, 30), font, 0.6, red, 2)

        # Calculate angles.
        neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
        torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

        # Draw landmarks.
        cv2.circle(image, (l_shldr_x, l_shldr_y), 7, white, 2)
        cv2.circle(image, (l_ear_x, l_ear_y), 7, white, 2)

        # Let's take y - coordinate of P3 100px above x1,  for display elegance.
        # Although we are taking y = 0 while calculating angle between P1,P2,P3.
        cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, white, 2)
        cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
        cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)

        # Similarly, here we are taking y - coordinate 100px above x1. Note that
        # you can take any value for y, not necessarily 100 or 200 pixels.
        cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

        # Put text, Posture and angle inclination.
        # Text string for display.
        angle_text_string_neck = 'Neck inclination: ' + str(int(neck_inclination))
        angle_text_string_torso = 'Torso inclination: ' + str(int(torso_inclination))

        # Determine whether good posture or bad posture.
        # The threshold angles have been set based on intuition.
        if neck_inclination < neck_angle_threshold and torso_inclination < torso_angle_threshold:
            bad_frames = 0
            good_frames += 1

            cv2.putText(image, angle_text_string_neck, (10, 30), font, 0.6, light_green, 2)
            cv2.putText(image, angle_text_string_torso, (10, 60), font, 0.6, light_green, 2)
            cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
            cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)

            # Join landmarks.
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 2)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 2)
            cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 2)
            cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 2)

        else:
            good_frames = 0
            bad_frames += 1

            cv2.putText(image, angle_text_string_neck, (10, 30), font, 0.6, red, 2)
            cv2.putText(image, angle_text_string_torso, (10, 60), font, 0.6, red, 2)
            cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
            cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)

            # Join landmarks.
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 2)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 2)
            cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 2)
            cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 2)

        # Calculate the time of remaining in a particular posture.
        good_time = (1 / fps) * good_frames
        bad_time = (1 / fps) * bad_frames

        # Pose time.
        if good_time > 0:
            time_string_good = 'Good Posture Time : ' + str(round(good_time, 1)) + 's'
            cv2.putText(image, time_string_good, (10, h - 20), font, 0.9, green, 2)
        else:
            time_string_bad = 'Bad Posture Time : ' + str(round(bad_time, 1)) + 's'
            cv2.putText(image, time_string_bad, (10, h - 20), font, 0.9, red, 2)

        # If you stay in bad posture for more than 3 minutes (180s) send an alert.
        if bad_time > time_threshold:
            sendWarning()

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Pose', image)

        # Exit the loop if the 'q' key is pressed.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the windows.
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    args = parse_arguments()
    
    print("Arguments:")
    print(f"Video: {args.video}")
    print(f"Offset Threshold: {args.offset_threshold}")
    print(f"Neck Angle Threshold: {args.neck_angle_threshold}")
    print(f"Torso Angle Threshold: {args.torso_angle_threshold}")
    print(f"Time Threshold: {args.time_threshold}")

    main(args.video)