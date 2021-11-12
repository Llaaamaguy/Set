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

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.56.1', 8485))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 320)
cam.set(4, 240)

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]


def recv():
    while True:
        data = client_socket.recv(4096).decode()
        if not data:
            pass
        else:
            print(str(data))



while True:
    ret, frame = cam.read()


    result, frame = cv2.imencode('.jpg', frame, encode_param)

    #    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    size = len(data)

    #print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1
    if img_counter == 1:
        print("Started listening")
        threading.Thread(target=recv).start()


cam.release()
cv2.destroyAllWindows()
