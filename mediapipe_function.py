import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

def process_video(input_file_path):
    cap = cv2.VideoCapture(input_file_path)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    output_file_path = 'pose_skeleton_output.mp4'

    # Define the codec and create VideoWriter object
    out = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                print("Ignoring empty camera frame.")
                break

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Make detection
            results = pose.process(image)
            
            # Create a black background
            black_background = np.zeros(frame.shape, dtype=np.uint8)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                if landmarks:
                    # Get coordinates
                    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

                    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

                    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

                    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

                    right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    # Calculate angle
                    angle_right_elbow = calculate_angle(right_shoulder, right_elbow, right_wrist)
                    angle_right_hip = calculate_angle(right_shoulder, right_hip, right_knee)
                    angle_right_knee = calculate_angle(right_hip, right_knee, right_ankle)

                    # Calculate angles for the left side
                    angle_left_elbow = calculate_angle(left_shoulder, left_elbow, left_wrist)
                    angle_left_hip = calculate_angle(left_shoulder, left_hip, left_knee)
                    angle_left_knee = calculate_angle(left_hip, left_knee, left_ankle)

                    # Display angles for the right side
                    cv2.putText(black_background, f'Right Elbow: {angle_right_elbow:.2f}', 
                                (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (57, 255, 20), 2, cv2.LINE_AA)
                    cv2.putText(black_background, f'Right Hip: {angle_right_hip:.2f}', 
                                (10, 70), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (57, 255, 20), 2, cv2.LINE_AA)
                    cv2.putText(black_background, f'Right Knee: {angle_right_knee:.2f}', 
                                (10, 110), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (57, 255, 20), 2, cv2.LINE_AA)

                    # Display angles for the left side
                    cv2.putText(black_background, f'Left Elbow: {angle_left_elbow:.2f}', 
                                (10, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (57, 255, 20), 2, cv2.LINE_AA)
                    cv2.putText(black_background, f'Left Hip: {angle_left_hip:.2f}', 
                                (10, 190), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (57, 255, 20), 2, cv2.LINE_AA)
                    cv2.putText(black_background, f'Left Knee: {angle_left_knee:.2f}', 
                                (10, 230), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (57, 255, 20), 2, cv2.LINE_AA)

            except Exception as e:
                print(f"Error: {e}")
            
            # Render detections
            mp_drawing.draw_landmarks(black_background, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Write the frame to the video file
            out.write(black_background)

            cv2.imshow('Pose Skeleton', black_background)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    return output_file_path

# Example usage:
input_path = 'IMG_8101.mp4'
output_path = process_video(input_path)
print(f'Output saved to: {output_path}')