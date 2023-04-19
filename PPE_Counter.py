from ultralytics import YOLO
import cv2
import cvzone
import math

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)

#cap = cv2.VideoCapture("../Videos/ppe-1.mp4")#for Video


model = YOLO("../YOLO_weights/best.pt")

classNames = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone', 'Safety Vest', 'machinery', 'vehicle']

unSafe = (0,0,255)
safe = (0,255,0)
while True:
    success,img = cap.read()
    results = model(img,stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:

            #bounding boxes
            x1,y1,x2,y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
            print(x1,y1,x2,y2)
            #cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)

            w,h = x2-x1,y2-y1
            #cvzone.cornerRect(img,(x1,y1,w,h))
            cv2.rectangle(img,(x1,y1),(x2,y2),unSafe,3)


            #confidene
            conf = math.ceil((box.conf[0]*100))/100
            #print(conf)

            #Class name
            cls = int(box.cls[0])
            currentClass = classNames[cls]
            if conf>0.5:
                if currentClass =='Hardhat' or currentClass =='Mask' or currentClass =='Safety Vast':
                    myColor = (0,0,255)

                elif currentClass =='NO-Hardhat' or currentClass =='NO-Mask' or currentClass =='NO-Safety Vest':
                    myColor = (0,255,0)
                else:
                    myColor = (255,0,0)
                cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 3)
                cvzone.putTextRect(img, f'{classNames[cls]},{conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1,
                                   colorB=myColor,
                                   colorT=(255, 255, 255), colorR=myColor)



    cv2.imshow("image",img)
    cv2.waitKey(1)