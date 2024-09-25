import time
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
   
   success, img = cap.read()
   imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
   results = hands.process(imgrgb)
#    print(results.multi_hand_landmarks)

   if results.multi_hand_landmarks:
        for handl in results.multi_hand_landmarks:
                for id, lm in enumerate(handl.landmark):
                        print(id,lm)
                        h, w, c=img.shape
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        print(id,cx,cy)
                        if id == 0:
                                cv2.circle(img, (cx,cy), 25, (255,0,255), cv2.FILLED)
                           
        mpdraw.draw_landmarks(img, handl, mphands.HAND_CONNECTIONS)
   
   cTime = time.time()
   fps =  1 / (cTime-pTime)
   pTime = cTime
   
   cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3,
               (255,0,255),3)
        
   cv2.imshow('Image',img)
        
   if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# cap.release()
# cv2.destroyAllWindows()
   