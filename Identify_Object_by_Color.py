import cv2
import numpy as np

cap = cv2.VideoCapture(0)
TARGET_SIZE = (640,360)

while True:
    ret, img = cap.read()
    imgResized = cv2.resize(img, TARGET_SIZE)
    imgFlipped = cv2.flip(imgResized, 1)
    imgHSV = cv2.cvtColor(imgFlipped, cv2.COLOR_BGR2HSV)

    height, width = imgHSV.shape[:2]
    h = imgHSV[int(height/2),int(width/2),0]
    s = imgHSV[int(height/2),int(width/2),1]
    v = imgHSV[int(height/2),int(width/2),2]

    maskYarDom = cv2.inRange(imgHSV,(25,150,100),(35,200,250))
    maskShield = cv2.inRange(imgHSV,(-5,100,100),(10,200,150))
    maskBox = cv2.inRange(imgHSV,(95,100,100),(110,200,200))

    cv2.putText(imgFlipped, str(h), (20, 30),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0))
    cv2.putText(imgFlipped, str(s), (90, 30),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0))
    cv2.putText(imgFlipped, str(v), (160, 30),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255))

    if(np.sum(maskYarDom/255) > 0.03*height*width):
        cv2.putText(imgFlipped,'Yar Dom',(50,200),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255))
        mask = maskYarDom
    elif(np.sum(maskShield/255) > 0.03*height*width):
        cv2.putText(imgFlipped,'Shield',(50,200),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255))
        mask = maskShield
    elif(np.sum(maskBox/255) > 0.03*height*width):
        cv2.putText(imgFlipped,'Box',(50,200),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255))
        mask = maskBox
    else:
        mask = np.zeros_like(imgFlipped)


    cv2.imshow('HSV', imgHSV)
    cv2.imshow('RGB', imgFlipped)
    cv2.imshow('mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()