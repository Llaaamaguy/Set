"""
THIS CODE WORKS
"""

import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import threading
import base64
import zmq
import numpy as np


# You must first run the command ngrok tcp 8485
ngrokip = input("Enter given ngrok ip: ")


context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect(ngrokip)


"""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ngrokip, ngrokport))
connection = client_socket.makefile('wb')
"""

cam = cv2.VideoCapture(0)

cam.set(3, 320)
cam.set(4, 240)

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]


def recv():
    while True:
        data = footage_socket.recv(4096).decode()
        if not data:
            pass
        else:
            print(str(data))


while True:
    ret, frame = cam.read()

    frame = cv2.resize(frame, (640, 480))
    encoded, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)
    footage_socket.send(jpg_as_text)

    """
    result, frame = cv2.imencode('.jpg', frame, encode_param)

    #    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    size = len(data)

    #print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    """
    img_counter += 1
    if img_counter == 1:
        print("Started listening")
        threading.Thread(target=recv).start()


cam.release()
cv2.destroyAllWindows()
