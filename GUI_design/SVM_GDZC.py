import glob
import platform
import time
from PIL import Image
from skimage.feature import hog
import numpy as np
import os
import joblib
from sklearn.svm import LinearSVC
import shutil
import sys

image_height = 320
image_width = 300

test_path = r''
savePath = r'C:\PLY\Graduation Design\GUI_design\feat\0'
model_path = r'C:\PLY\Graduation Design\HOG_SVM-master\model\model_oil_leak'
global flag

def rgb2gray(im):
    gray = im[:, :, 0] * 0.2989 + im[:, :, 1] * 0.5870 + im[:, :, 2] * 0.1140
    return gray

def get_feat(path):
    image = Image.open(path)
    image = image.resize((image_width, image_height), Image.ANTIALIAS)
    image = image.copy()
    image = np.reshape(image, (image_height, image_width, -1))
    gray = rgb2gray(image) / 255.0
    # 这句话根据你的尺寸改改
    fd = hog(gray, orientations=9, block_norm='L1', pixels_per_cell=[8, 8], cells_per_block=[4, 4], visualize=False,
             transform_sqrt=True)
    # 这句话根据你的尺寸改改
    image_name = (path.split('\\'))[-1]
    fd_name = image_name + '.feat'
    fd_path = os.path.join(savePath, fd_name)
    joblib.dump(fd, fd_path)
    return fd_path

def Predict(test_path):
    clf = joblib.load(model_path)
    data_test = joblib.load(get_feat(test_path))
    data_test_feat = data_test.reshape((1, -1)).astype(np.float64)
    result = clf.predict(data_test_feat)
    if int(result[0]) == 0:
        flag = 0
    else:
        flag = 1
    return flag

if __name__ == '__main__':
    Predict(test_path)
