from ultralytics import YOLO
import cv2
import cvzone
import math
import Opening
import time

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

hand1 = []
hand2 = []
step = 1
last_detection_time = 0
delay_after_detection = 3  # deteksi setelah 3 detik tenang

while True:
    success, img = cap.read()
    results = model(img, stream=True)
    current_hand = []

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))

            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])

            if conf > 0.5:
                current_hand.append(classNames[cls])
                cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

    current_hand = list(set(current_hand))
    
    if step == 1 and len(current_hand) == 13:
        hand1 = current_hand
        bid1 = Opening.openingBridgeHand(hand1)
        print(f"Opening Bid (Hand 1): {bid1}")
        cvzone.putTextRect(img, f'Opening: {bid1}', (100, 75), scale=2, thickness=2)
        step = 2
        last_detection_time = time.time()
    
    elif step == 2 and len(current_hand) == 13 and time.time() - last_detection_time > delay_after_detection:
        hand2 = current_hand
        bid2 = Opening.openingBridgeHand(hand2)
        print(f"Response Bid (Hand 2): {bid2}")
        cvzone.putTextRect(img, f'Response: {bid2}', (100, 125), scale=2, thickness=2)
        step = 3
        last_detection_time = time.time()

    elif step == 3:
        # Masukkan ke fungsi get_contract
        from kombinasi_bid import analyze_combined_hand  # kamu bisa pisah logika kontrak ke file ini

        strain, level = analyze_combined_hand(hand1, hand2)
        print(f"Kontrak Rekomendasi: {level}{strain}")
        cvzone.putTextRect(img, f'Contract: {level}{strain}', (100, 175), scale=2, thickness=2)
        step = 4

    cv2.imshow("Image", img)
    cv2.waitKey(1)
