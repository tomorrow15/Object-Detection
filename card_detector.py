from ultralytics import YOLO
import cv2
import cvzone
import math
import card_function


cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)

#cap = cv2.VideoCapture("../Videos/testVd.m4v")  #for Video


model = YOLO("../YOLO_weights/playingCards.pt")

classNames = ['10C', '10D', '10H', '10S',
              '2C', '2D', '2H', '2S',
              '3C', '3D', '3H','3S',
              '4C', '4D', '4H', '4S',
              '5C', '5D', '5H', '5S',
              '6C', '6D', '6H','6S',
              '7C', '7D', '7H', '7S',
              '8C', '8D', '8H', '8S',
              '9C', '9D', '9H','9S',
              'AC', 'AD', 'AH', 'AS',
              'JC', 'JD', 'JH', 'JS',
              'KC', 'KD', 'KH','KS',
              'QC', 'QD', 'QH', 'QS']


while True:
    success,img = cap.read()
    results = model(img,stream=True)
    hand = []
    for r in results:
        boxes = r.boxes
        for box in boxes:

            #bounding boxes
            x1,y1,x2,y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
            print(x1,y1,x2,y2)
            #cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)

            w,h = x2-x1,y2-y1
            cvzone.cornerRect(img,(x1,y1,w,h))

            #confidene
            conf = math.ceil((box.conf[0]*100))/100
            #print(conf)

            #Class name
            cls = int(box.cls[0])

            cvzone.putTextRect(img, f'{classNames[cls]},{conf}', (max(0, x1), max(35, y1)))

            if conf>0.5:
                hand.append((classNames[cls]))
    print(hand)
    hand = list(set(hand))
    if len(hand)== 5:
        results = card_function.findPokerHand(hand)
        print(results)
        cvzone.putTextRect(img, f'Your Hand is {results}', (300,75),scale=3,thickness=5)
    cv2.imshow("image",img)
    cv2.waitKey(1)