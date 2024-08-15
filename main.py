import os
import os.path
import csv
from cvzone.HandTrackingModule import HandDetector
import datetime
import uuid
import time
import tkinter as tk
from PIL import ImageTk, Image
from threading import Timer
def display(r):

    def d():
        root.destroy()

    order = r
    root = tk.Tk()
    root.title("Order Successfull !")
    root.geometry("320x360")
    root.resizable(0, 0)
    root.configure(background='#23064d')

    img = ImageTk.PhotoImage(Image.open("Resources/success.png"))
    i = tk.Label(root, image=img)

    l1 = tk.Label(root, text="Order ID - " + str(order[0]), width=100, font=('calibre', 10, 'bold'),
                  background="#ffff00", anchor="w")
    l2 = tk.Label(root, text="Datetime - " + str(order[1]), width=100, font=('calibre', 10, 'bold'), background="#fff",
                  anchor="w")
    l3 = tk.Label(root, text="Dish - " + str(order[2]), width=100, font=('calibre', 10, 'bold'), background="#fff",
                  anchor="w")
    l4 = tk.Label(root, text="Choice - " + str(order[3]), width=100, font=('calibre', 10, 'bold'), background="#fff",
                  anchor="w")
    l5 = tk.Label(root, text="Serving Size - " + str(order[4]), width=100, font=('calibre', 10, 'bold'), background="#fff",
                  anchor="w")
    i.pack(pady=10)
    l1.pack(pady=10)
    l2.pack()
    l3.pack()
    l4.pack()
    l5.pack()

    t = Timer(3.0, d)
    t.start()

    root.mainloop()

def main():
    file_exists = os.path.exists('Orders.csv')
    if not file_exists:
        f = open("Orders.csv", "w", newline="")
        cw = csv.writer(f)
        cw.writerow(["Order ID", "Datetime", "Dish", "Choice", "Serving Size"])
        f.close()
    else:
        print("File already Present !")

    import cv2

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)

    imgBackground = cv2.imread("Resources/Background.png")

    folderPathModes = "Resources/Modes"
    listImgModesPath = os.listdir(folderPathModes)
    listImgModes = []
    for imgModePath in listImgModesPath:
        listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgModePath)))

    folderPathIcons = "Resources/Icons"
    listImgIconsPath = os.listdir(folderPathIcons)
    listImgIcons = []
    for imgIconsPath in listImgIconsPath:
        listImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIconsPath)))

    modeType = 0
    selection = -1
    counter = 0
    selectionSpeed = 7
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    modePositions = [(1136, 196), (1000, 384), (1136, 581)]
    counterPause = 0
    selectionList = [-1, -1, -1]

    while True:
        success, img = cap.read()
        # img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=True)

        imgBackground[139:139 + 480, 50:50 + 640] = img
        imgBackground[0:720, 847: 1280] = listImgModes[modeType]

        if hands and counterPause == 0 and modeType < 3:

            hand1 = hands[0]
            fingers1 = detector.fingersUp(hand1)

            if fingers1 == [0, 1, 0, 0, 0]:
                if selection != 1:
                    counter = 1
                selection = 1
            elif fingers1 == [0, 1, 1, 0, 0]:
                if selection != 2:
                    counter = 1
                selection = 2
            elif fingers1 == [0, 1, 1, 1, 0]:
                if selection != 3:
                    counter = 1
                selection = 3
            else:
                selection = -1
                counter = 0

            if counter > 0:
                counter += 1
                print(counter)

                cv2.ellipse(imgBackground, modePositions[selection - 1], (103, 103), 0, 0,
                            counter * selectionSpeed, (0, 255, 0), 20)
                if counter * selectionSpeed > 360:
                    selectionList[modeType] = selection
                    modeType += 1
                    counter = 0
                    selection = -1
                    counterPause = 1

        if counterPause > 0:
            counterPause += 1
            if counterPause > 20:
                counterPause = 0

        if selectionList[0] != -1:
            imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]
        if selectionList[1] != -1:
            imgBackground[636:636 + 65, 340:340 + 65] = listImgIcons[2 + selectionList[1]]
        if selectionList[2] != -1:
            imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionList[2]]

        if modeType == 3:
            imgBackground[0:720, 847: 1280] = listImgModes[3]
            print("Order Placed !")
            r = [uuid.uuid4(), datetime.datetime.now().strftime("%c")]

            if selectionList[0] == 1:
                r.append("Burger")
            if selectionList[0] == 2:
                r.append("Pizza")
            if selectionList[0] == 3:
                r.append("Pasta")

            if selectionList[1] == 1:
                r.append("VEG")
            if selectionList[1] == 2:
                r.append("NON VEG")
            if selectionList[1] == 3:
                r.append("EGG")

            if selectionList[2] == 1:
                r.append("Small")
            if selectionList[2] == 2:
                r.append("Medium")
            if selectionList[2] == 3:
                r.append("Large")

            f = open("Orders.csv", "a", newline="")
            cw = csv.writer(f)
            cw.writerow(r)
            f.close()

            if f.closed:
                time.sleep(2)
                display(r)
                main()

        cv2.imshow("GESTURE BASED ORDERING SYSTEM BY SUBHOJIT GHOSH", imgBackground)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.waitKey(1)


main()
