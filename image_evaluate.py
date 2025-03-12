import cv2
import numpy as np
import math
from PIL import Image, ImageStat

#图像信息熵也是图像一维熵
tmp = []
for i in range(256):
    tmp.append(0)
val = 0
k = 0
res = 0
image = cv2.imread(r'C:\PLY\Graduation Design\test_1 _ori.jpg',0)
img = np.array(image)
for i in range(len(img)):
    for j in range(len(img[i])):
        val = img[i][j]
        tmp[val] = float(tmp[val] + 1)
        k = float(k + 1)
for i in range(len(tmp)):
    tmp[i] = float(tmp[i] / k)
for i in range(len(tmp)):
    if tmp[i] == 0:
        res = res
    else:
        res = float(res - tmp[i] * (math.log(tmp[i]) / math.log(2.0)))
print(res)

img = Image.open(r'C:\PLY\Graduation Design\test_1 _ori.jpg')
stat = ImageStat.Stat(img)
print(stat.extrema)  # 最大值与最小值[(0, 255)]
print(stat.mean)  # 均值
print(stat.stddev)  # 标准差




