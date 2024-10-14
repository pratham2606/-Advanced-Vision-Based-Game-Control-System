import time
import cv2
import mediapipe as mp
import PostEstimationModule as pem
import pyautogui  # Import pyautogui for keyboard control

cap = cv2.VideoCapture(0)
detector = pem.poseDetector()

counter = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (750, 550))
    img = cv2.flip(img, 1)
    detector.findPose(img, draw=False)
    lmList = detector.getPosition(img, draw=False)

    if lmList:
        p1, p2 = lmList[1][1:], lmList[23][1:]  # Nose and hip landmarks
        left, right = lmList[18][1:], lmList[19][1:]  # Left and right hands
        l1, _, _ = detector.findDistance(left, right)

        # Jump action (hands together)
        if l1 < 80:  # Hands close together
            if counter == 0:
                pyautogui.press('up')  # Press up arrow key for jump
                print("Jump")

        # Duck action (nose below threshold)
        if p1[1] > 250:  # Nose is below a certain level (duck)
            if counter == 0:
                pyautogui.press('down')  # Press down arrow key for duck
                print("Duck")

        # Move left action (left hand to the left)
        if left[0] < 150:  # Left hand moves to the left
            pyautogui.press('left')  # Press left arrow key
            print("Move Left")

        # Move right action (right hand to the right)
        if right[0] > 600:  # Right hand moves to the right
            pyautogui.press('right')  # Press right arrow key
            print("Move Right")

        counter += 1
    if counter == 11:
        counter = 0

    cv2.imshow("Arcade Game Frame", img)
    cv2.waitKey(1)
