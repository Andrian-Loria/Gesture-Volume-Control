import cv2
from cvzone.HandTrackingModule import HandDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import math

# Set up the camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Pycaw setup to control system volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get the volume range (Windows volume control is usually in the range of -96.0 to 0.0)
volRange = volume.GetVolumeRange()
minVol = volRange[0]  # Minimum volume (-96.0 dB)
maxVol = volRange[1]  # Maximum volume (0.0 dB)
vol = 0
volBar = 350

def fingers_up(lmList):
    fingers = []
    
    # Thumb (check if the x-coordinate of the tip is greater/smaller than the joint for right/left hand)
    if lmList[4][0] > lmList[3][0]:  # For right hand
        fingers.append(1)  # Thumb is up
    else:
        fingers.append(0)  # Thumb is down
    
    # For other fingers (Index, Middle, Ring, Pinky)
    for i in range(1, 5):
        if lmList[i * 4][1] < lmList[i * 4 - 2][1]:  # Tip y-coordinate < Joint y-coordinate
            fingers.append(1)  # Finger is up
        else:
            fingers.append(0)  # Finger is down

    return fingers

while True:
    success, img = cap.read()
    
    # Detect hand and landmarks
    hands, img = detector.findHands(img)
    
    if hands:
        # Get the first hand detected
        hand = hands[0]
        lmList = hand['lmList']  # List of 21 hand landmark points
        
        fingers = fingers_up(lmList)
        
        if fingers == [1, 1, 0, 0, 0]:
        
            # Get coordinates for the thumb tip (landmark 4) and index finger tip (landmark 8)
            x1, y1 = lmList[4][1], lmList[4][2]  # Thumb tip
            x2, y2 = lmList[8][1], lmList[8][2]  # Index finger tip
            
            # Draw a circle at thumb and index finger tips
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            
            # Draw a line between thumb and index finger
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            
            # Calculate the distance between thumb and index finger
            length = math.hypot(x2 - x1, y2 - y1)
            
            # Map the length to the volume range
            vol = np.interp(length, [20,100], [minVol, maxVol])
            # Display the current volume on the image
            volbar = np.interp(length, [20,100], [350,150])  # Map distance to volume bar height
            
            volume.SetMasterVolumeLevel(vol, None)
            cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'Vol: {int(np.interp(vol, [minVol, maxVol], [0, 100]))} %', (40, 450), 
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    
    # Display the result
    cv2.imshow("Image", img)
    
    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
