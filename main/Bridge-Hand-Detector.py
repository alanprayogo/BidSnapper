from ultralytics import YOLO
import cv2
import cvzone
import math
import Opening

cap = cv2.VideoCapture(1)
cap.set(3, 720)
cap.set(4, 640)

model = YOLO('../yolo-weights/playingCards.pt')

classNames= ["10C", "10D", "10H", "10S",
            "2C", "2D", "2H", "2S",
            "3C", "3D", "3H", "3S",
            "4C", "4D", "4H", "4S",
            "5C", "5D", "5H", "5S",
            "6C", "6D", "6H", "6S",
            "7C", "7D", "7H", "7S",
            "8C", "8D", "8H", "8S",
            "9C", "9D", "9H", "9S",
            "AC", "AD", "AH", "AS",
            "JC", "JD", "JH", "JS",
            "KC", "KD", "KH", "KS",
            "QC", "QD", "QH", "QS"
]

while True:
    success, img = cap.read()
    results = model(img, stream=True)
    # results = model('main/images/hand1.jpg', show=True)
    hand = []
    for r in results:
        boxes = r.boxes
        for box in boxes:

            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0] 
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),3)
            w, h = x2-x1, y2-y1
            cvzone.cornerRect(img, (x1, y1, w, h))

            # Confidence
            conf = math.ceil((box.conf[0]*100))/100

            # Class Name
            cls = int(box.cls[0])

            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            if conf > 0.6:
                hand.append(classNames[cls])

    hand = list(set(hand))
    print(hand)

    if len(hand) == 13:
        results = Opening.openingBridgeHand(hand)
        print(results)
        cvzone.putTextRect(img, f'Bid: {results}', (100, 75), scale=3, thickness=3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

