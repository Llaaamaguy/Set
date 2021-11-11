import zbarlight
import cv2 as cv

img = cv.imread("codes.png", 0)

codes = zbarlight.scan_codes("qrcode", img)

print('Data: %s' % codes)
