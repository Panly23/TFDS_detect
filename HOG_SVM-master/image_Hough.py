# -*- coding=GBK -*-
import cv2 as cv
import numpy as np


def line_image(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # 灰度图像
    edges = cv.Canny(gray, 50, 200)
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 30, minLineLength=60, maxLineGap=10)
    lines1 = lines[:, 0, :]  # 提取为二维

    for x1, y1, x2, y2 in lines1[:]:
        cv.line(image, (x1, y1), (x2, y2), (255, 0, 0), 1)
    cv.imshow("line", image)


src = cv.imread("C:/PLY/Graduation Design/HOG_SVM-master/image/train_SJB_canny/58_1_5.jpg_2.jpg")
cv.imshow("before", src)
line_image(src)
cv.waitKey(0)
cv.destroyAllWindows()

