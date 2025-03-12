import cv2
import numpy as np

path = r'C:\PLY\Graduation Design\software_GUI\image\test_1.jpg'
img = cv2.imread(path)

kernel = np.array([[0, -1, 0], [0, 5, 0], [0, -1, 0]])  # 定义卷积核
imageEnhance = cv2.filter2D(img, -1, kernel)  # 进行卷积运算

cv2.imshow('output', imageEnhance)
cv2.waitKey(0)
cv2.imwrite(path + '_Laplace' + '.jpg', imageEnhance)