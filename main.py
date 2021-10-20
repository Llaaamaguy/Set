import cv2 as cv
import numpy as np
from isSet import isSet


cam = cv.VideoCapture(0)
qrCodeDetector = cv.QRCodeDetector()

