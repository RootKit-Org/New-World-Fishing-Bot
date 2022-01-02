import cv2
import numpy as np


while (1):
    image = cv2.imread('imgs/cap_with_red.PNG')

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only red colors
    mask2 = cv2.inRange(hsv, (179, 210, 200), (180, 212, 255))

    # Bitwise-AND mask and original image
    output = cv2.bitwise_and(image, image, mask=mask2)

    cv2.imshow('mask', mask2)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
