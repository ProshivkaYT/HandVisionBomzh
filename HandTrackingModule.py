import cv2
import mediapipe as mp
from datetime import datetime

# Initialize hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def change_camera(new_camera):
    global cap
    cap.release()
    cap = cv2.VideoCapture(new_camera)

# Open the default camera
cap = cv2.VideoCapture(0)

# Initial positions of the clock widgets
clock_pos_x_eye1 = 10
clock_pos_y_eye1 = 50
clock_pos_x_eye2 = 10
clock_pos_y_eye2 = 50

while True:
    # Capture frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Duplicate the frame
    frame1 = frame.copy()

    # Resize one frame to be slightly wider
    height, width = frame.shape[:2]
    frame2 = cv2.resize(frame, (int(width * 1.1), height))  # Adjust the factor (1.1) for desired width

    # Resize frames to fit the window (if needed)
    frame1 = cv2.resize(frame1, (width, height))
    frame2 = cv2.resize(frame2, (width, height))

    # Detect hand landmarks in the first frame
    results1 = hands.process(frame1)
    if results1.multi_hand_landmarks:
        for hand_landmarks in results1.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp.solutions.drawing_utils.draw_landmarks(frame1, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the position of the index finger tip landmark
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_tip_x = int(index_finger_tip.x * width)
            index_finger_tip_y = int(index_finger_tip.y * height)

            # Check if the index finger is pointing at the clock widget
            if (clock_pos_x_eye1 - 5 < index_finger_tip_x < clock_pos_x_eye1 + 150) and \
               (clock_pos_y_eye1 - 5 < index_finger_tip_y < clock_pos_y_eye1 + 70):
                # Update the position of the first clock widget based on the index finger tip
                clock_pos_x_eye1 = index_finger_tip_x - 75
                clock_pos_y_eye1 = index_finger_tip_y - 35

    # Detect hand landmarks in the second frame
    results2 = hands.process(frame2)
    if results2.multi_hand_landmarks:
        for hand_landmarks in results2.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp.solutions.drawing_utils.draw_landmarks(frame2, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the position of the index finger tip landmark for the second hand
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_tip_x = int(index_finger_tip.x * width)
            index_finger_tip_y = int(index_finger_tip.y * height)

            # Check if the index finger is pointing at the clock widget
            if (clock_pos_x_eye2 - 5 < index_finger_tip_x < clock_pos_x_eye2 + 150) and \
               (clock_pos_y_eye2 - 5 < index_finger_tip_y < clock_pos_y_eye2 + 70):
                # Update the position of the second clock widget based on the index finger tip
                clock_pos_x_eye2 = index_finger_tip_x - 75
                clock_pos_y_eye2 = index_finger_tip_y - 35

    # Combine frames horizontally
    combined_frame = cv2.hconcat([frame1, frame2])

    # Get current time
    current_time = datetime.now().strftime("%H:%M:%S")

    # Add first clock widget to the combined frame
    clock_area_eye1 = combined_frame[clock_pos_y_eye1:clock_pos_y_eye1+70, clock_pos_x_eye1:clock_pos_x_eye1+150]
    clock_area_eye1[:] = (255, 255, 255)  # Fill clock area with white color
    cv2.putText(combined_frame, current_time, (clock_pos_x_eye1 + 10, clock_pos_y_eye1 + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)  # Black text color

    # Add second clock widget to the combined frame
    clock_area_eye2 = combined_frame[clock_pos_y_eye2:clock_pos_y_eye2+70, width + clock_pos_x_eye2:width + clock_pos_x_eye2+150]
    clock_area_eye2[:] = (255, 255, 255)  # Fill clock area with white color
    cv2.putText(combined_frame, current_time, (width + clock_pos_x_eye2 + 10, clock_pos_y_eye2 + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)  # Black text color

    # Display the combined frame
    cv2.imshow('Hand Vision Bomzh', combined_frame)

    # Display camera selection menu and switch camera if a new camera is selected
    key = cv2.waitKey(1) & 0xFF
    if key == ord('0'):
        change_camera(0)
    elif key == ord('1'):
        change_camera(1)
    elif key == ord('2'):
        change_camera(2)
    elif key == ord('3'):
        change_camera(3)
    elif key == ord('q'):
        break

# Release the capture object and close windows
cap.release()
cv2.destroyAllWindows()2