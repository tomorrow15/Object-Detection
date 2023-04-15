from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *

#cap = cv2.VideoCapture(0)
#cap.set(3,1920)
#cap.set(4,1080)

cap = cv2.VideoCapture("../Videos/cars.mp4")#for Video


model = YOLO("../YOLO_weights/yolov8l.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]
mask = cv2.imread("../Videos/mask.png")

#Tracking
tracker = Sort(max_age=20,min_hits=3,iou_threshold=0.3)
limit = [400,297,673,297]
totalCount = []



while True:
    success,img = cap.read()
    imgGraphic = cv2.imread("../Videos/graphics.png",cv2.IMREAD_UNCHANGED)
    img = cvzone.overlayPNG(img,imgGraphic,(0,0))

    #print(img.shape, img.dtype)
    #print(mask.shape, mask.dtype)

    imgRegion = cv2.bitwise_and(img,mask)
    results = model(imgRegion, stream=True)

    detections = np.empty((0,5))
    for r in results:
        boxes = r.boxes
        for box in boxes:

            #bounding boxes
            x1,y1,x2,y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
            print(x1,y1,x2,y2)
            #cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w,h = x2-x1,y2-y1

            #confidene
            conf = math.ceil((box.conf[0]*100))/100
            #print(conf)

            #Class name
            cls = int(box.cls[0])
            currentClass = classNames[cls]
            if currentClass == "car" or currentClass == "truck"or currentClass == "bus"or currentClass == "motorbike" and conf>0.3:
                #cvzone.putTextRect(img, f'{currentClass},{conf}', (max(0, x1), max(35, y1)),scale=0.6,thickness=1,offset=3)
                #cvzone.cornerRect(img,(x1,y1,w,h),l=9,rt = 9,colorR=(255,0,0))
                currentArray = np.array([x1,y1,x2,y2,conf])
                detections = np.vstack((detections,currentArray))

    resultsTracker = tracker.update(detections)
    cv2.line(img,(limit[0],limit[1]),(limit[2],limit[3]),(0,0,255),5)

    for result in resultsTracker:
        x1,y1,x2,y2,id = result
        x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
        w, h = x2 - x1, y2 - y1
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2,colorR=(255,0,255))
        cvzone.putTextRect(img, f'{int(id)}', (max(0, x1), max(35, y1)), scale=2, thickness=3, offset=6)
        cx,cy = x1+w//2,y1+h//2
        cv2.circle(img,(cx,cy),5,(255,0,255 ),cv2.FILLED)

        if limit[0]<cx<limit[2] and limit[1]-15 < limit[1]+15:
             if totalCount.count(id)==0:
                 totalCount.append(id)
                 cv2.line(img,(limit[0],limit[1]),(limit[2],limit[3]),(0,255,0),5)


        cvzone.putTextRect(img,f'Count: {len(totalCount)}',(50,50))
        #cv2.putText(img, str(len(totalCount)), (255, 100), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 255), 8)
        #finding center
        #cx,cy = x1+w//2

        print(result)








    cv2.imshow("image", img)
    cv2.imshow("imageRegion", imgRegion)
    cv2.waitKey(1)