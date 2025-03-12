# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import cv2

filePath = r'C:\PLY\Graduation Design\software_GUI\image\test_1.jpg'

#对数变换
def log(c, img):
    output = c * np.log(1.0 + img)
    output = np.uint8(output + 0.5)
    return output
#读取原始图像
img = cv2.imread(filePath)
#图像灰度对数变换
output = log(42, img)
#显示图像
cv2.imshow('Output', output)
cv2.waitKey(0)
cv2.imwrite(filePath + '_log' + '.jpg', output)
