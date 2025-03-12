import cv2
import numpy as np
import random


def grey_world(nimg):
    # nimg = np.array(nimg)
    # nimg = nimg.transpose(2, 0, 1).astype(np.uint32)
    avgR = np.average(nimg[0])
    avgG = np.average(nimg[1])
    avgB = np.average(nimg[2])
    avg = (avgB + avgG + avgR) / 3
    nimg[0] = np.minimum(nimg[0] * (avg / avgR), 255)
    nimg[1] = np.minimum(nimg[1] * (avg / avgG), 255)
    nimg[2] = np.minimum(nimg[2] * (avg / avgB), 255)
    # return nimg.transpose(1, 2, 0).astype(np.uint8)
    return nimg

path = r'C:\PLY\Graduation Design\software_GUI\image\test_1.jpg'
img = cv2.imread(path, cv2.COLOR_GRAY2RGB)
img1 = grey_world(img)
# img_1 = np.copy(img1)
cv2.imwrite(path + '_AWB' + '.jpg', img1)
cv2.imshow('image', img1)
cv2.waitKey(0)
