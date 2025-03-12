import cv2
import numpy as np
import matplotlib.pyplot as plt

img_path = r'C:\PLY\Graduation Design\HOG_SVM-master\image\train_DJ_new_resize\14id.jpg'
savePath = r'C:\PLY\Graduation Design\HOG_SVM-master\image\train_DJ_new_resize\14trans.jpg'
img = cv2.imread(img_path)
h, w, _= img.shape

mat_shift = np.float32([[1,0,10], [0,1,20]])
img_1 = cv2.warpAffine(img, mat_shift, (h, w))
mat_shift = np.float32([[1, 0, -15], [0, 1, -15]])
img_2 = cv2.warpAffine(img, mat_shift, (h, w))

cv2.imwrite(savePath, img_2)