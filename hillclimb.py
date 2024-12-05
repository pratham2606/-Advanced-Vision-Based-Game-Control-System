import cv2
import mediapipe as mp
import PostEstimationModule as pem
import pyautogui  # Import pyautogui for keyboard control

cap = cv2.VideoCapture(0)
detector = pem.poseDetector()

# Flags to track key states
left_key_pressed = False
right_key_pressed = False

while True:
    success, img = cap.read()
    img = cv2.resize(img, (750, 550))
    img = cv2.flip(img, 1)
    detector.findPose(img, draw=False)
    lmList = detector.getPosition(img, draw=False)

    if lmList:
        # Extract key landmark positions
        left_hand = lmList[18][1:]  # Left hand landmark
        right_hand = lmList[19][1:]  # Right hand landmark

        # Move left action (left hand to the left)
        if left_hand[0] < 150:  # Left hand moves to the left
            if not left_key_pressed:  # If the left key isn't already pressed
                pyautogui.keyDown('left')  # Hold down the left arrow key
                left_key_pressed = True
                print("Move Left")
        else:
            if left_key_pressed:  # If the left key is pressed but hand is no longer left
                pyautogui.keyUp('left')  # Release the left arrow key
                left_key_pressed = False

        # Move right action (right hand to the right)
        if right_hand[0] > 600:  # Right hand moves to the right
            if not right_key_pressed:  # If the right key isn't already pressed
                pyautogui.keyDown('right')  # Hold down the right arrow key
                right_key_pressed = True
                print("Move Right")
        else:
            if right_key_pressed:  # If the right key is pressed but hand is no longer right
                pyautogui.keyUp('right')  # Release the right arrow key
                right_key_pressed = False

    cv2.imshow("Hill Climb Racing Control", img)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
