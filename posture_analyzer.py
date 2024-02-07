import cv2
import mediapipe as mp
from process import decant_process
import numpy as np
from tqdm import tqdm

# Initialize mediapipe pose class.
mp_drawing = mp.solutions.drawing_utils  # Ref: https://github.com/google/mediapipe/blob/master/mediapipe/python/solutions/drawing_utils.py
mp_pose = mp.solutions.pose  # Ref: https://github.com/google/mediapipe/blob/master/docs/solutions/pose.md

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


def sendWarning(x):
    """
    Placeholder function for sending a warning.
    """
    pass

#def process_frame_video(frame, fps, offset_threshold=100, neck_angle_threshold=25, torso_angle_threshold=10, time_threshold=180):
def process_frame_video(video_path, offset_threshold=100, neck_angle_threshold=25, torso_angle_threshold=10, time_threshold=180):
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

    # For file input, replace file name with <path>.
    cap = cv2.VideoCapture(video_path) 
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
        min_detection_confidence = 0.4,  # Minimum confidence value ([0.0, 1.0]) from the person-detection model for the detection to be considered successful. Default to 0.5.
        min_tracking_confidence = 0.6 ) as pose:  # Minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the pose landmarks to be considered tracked successfully.  Setting it to a higher value can increase robustness of the solution, at the expense of a higher latency. Default to 0.5.

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
                #frame = np.ones_like(frame)* 255

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
                    #print(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width))
                
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

                # If you stay in bad posture for more than 3 minutes (180s) send an alert.
                if bad_time > time_threshold:
                    sendWarning()
        
                # Flip the image horizontally for a selfie-view display.
                #cv2.imshow('MediaPipe Pose', cv2.flip(frame, 1))
                #cv2.imshow('MediaPipe Pose', cv2.flip(black_image, 1))
                #if cv2.waitKey(1) & 0xFF == 27:
                #    break
                out.write(frame)
                pbar.update(1)  # Update the tqdm progress bar
    cap.release()
    out.release()
    return 

