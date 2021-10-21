import cv2 as cv
import numpy as np
import isSet
import pyzbar.pyzbar as pyzbar
import threading


def tts_set():
    # Does TTS
    pass


cam = cv.VideoCapture(0)
qrCodeDetector = cv.QRCodeDetector()

font = cv.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cam.read()

    objs = pyzbar.decode(frame)

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

        barCode = str(decodedObject.data)

        cv.putText(frame, barCode, (x, y), font, 1, (0, 255, 255), 2, cv.LINE_AA)

    cv.imshow("Preview", frame)

    # _, decoded_info, points, straight_qrcode = qrCodeDetector.detectAndDecodeMulti(frame)
    #
    # if points is not None:
    #     if len(decoded_info) == 2:
    #         if '' not in decoded_info:
    #             x = threading.Thread(target=tts_set)
    #             x.start()
    #
    #             print(decoded_info)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()