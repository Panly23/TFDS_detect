import cv2
import math
import numpy as np
import os
from PIL import Image

kernel = np.ones((5,5),np.uint8)

def Process(filePath, savePath):
    im = Image.open(filePath)
    img = np.copy(im)
    out = cv2.Canny(img, 30, 120)
    # out = cv2.dilate(imgCanny, kernel, iterations=1)
    cv2.imwrite(savePath, out)

def changeImage():
    filePath = r'C:\PLY\Graduation Design\HOG_SVM-master\image\train_SJB_gz_OSTU'
    destPath = r'C:\PLY\Graduation Design\HOG_SVM-master\image\train_SJB_gz_canny'
    if not os.path.exists(destPath):
        os.makedirs(destPath)
    for root, dirs, files in os.walk(filePath):
        for file in files:
            if file[-1]=='g':
                Process(os.path.join(filePath, file), os.path.join(destPath, file))
    print('Done')

if __name__ == '__main__':
    changeImage()



