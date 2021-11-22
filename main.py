import cv2 as cv
import numpy as np
import functools
import isSet
from Card import Card
import pyzbar.pyzbar as pyzbar
import PySimpleGUI as sg
from threading import Thread
import pyttsx3 as tts


def tts_set(cards):
    engine = tts.init()
    toSay = f"Found a set. {cards[0]}, {cards[1]}, {cards[2]}"
    engine.say(toSay)
    engine.runAndWait()


cam = cv.VideoCapture(0)
qrCodeDetector = cv.QRCodeDetector()

font = cv.FONT_HERSHEY_SIMPLEX

decodedCards = []


neededCards = 12
while True:
    ret, frame = cam.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    bwthresh, frame = cv.threshold(frame, 127, 255, cv.THRESH_BINARY)

    objs = pyzbar.decode(frame)
    h, w= frame.shape

    for o in objs:
        print(o)

    decodedObjects = pyzbar.decode(frame)

    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        # Number of points in the convex hull
        n = len(hull)
        # Draw the convext hull
        for j in range(0, n):
            cv.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        print(x, y)

        print('Type : ', decodedObject.type)
        print('Data : ', decodedObject.data, '\n')
        if str(decodedObject.data.decode('utf-8')) not in decodedCards:
            decodedCards.append(str(decodedObject.data.decode('utf-8')))

        barCode = str(decodedObject.data)

        cv.putText(frame, barCode, (x, y), font, 1, (0, 255, 255), 2, cv.LINE_AA)
        #toShow = f"Looking for {neededCards} cards"
        #offset = int(h/8)-10
        #cv.putText(frame, toShow, (20, offset), font, 1, (0,255,255), 2)
        #toShow = f"Currently have {str(len(decodedCards))} cards"
        #cv.putText(frame, toShow, (20, offset*2), font, 1, (0,255,255), 2)
    cv.imshow("beta v1.4", frame)

    if len(decodedCards) >= neededCards:
        cards = []
        for i in decodedCards:
            attrs = i.split()
            card = Card(attrs[0], attrs[1], attrs[2], attrs[3])
            cards.append(card)

        print("Card objects:\n", cards)

        useSet = isSet.find_first_set(cards)
        if useSet:
            print("SET found:", useSet, "\n")

            layout = [[sg.Text(f"SET: {useSet}")], [sg.Button("OK")]]
            window = sg.Window("Set window", layout)

            # Call TTS voice asyncronously
            Thread(target=functools.partial(tts_set, useSet)).start()

            while True:
                event, values = window.read()
                if event == "OK" or event == sg.WIN_CLOSED:
                    break
            window.close()
        else:
            print("No sets found with these cards")
            neededCards += 3
            layout = [[sg.Text(f"No sets found")], [sg.Button("OK")]]
            window = sg.Window("Set window", layout)
            while True:
                event, values = window.read()
                if event == "OK" or event == sg.WIN_CLOSED:
                    break
            window.close()

        for i in useSet:
            decodedCards.pop(useSet.index(i))

    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cam.release()
cv.destroyAllWindows()



