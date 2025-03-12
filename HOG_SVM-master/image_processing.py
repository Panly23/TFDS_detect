import cv2
import numpy as np
import os
from PIL import Image

def Process(filePath, savePath):
    im = Image.open(filePath)
    img = np.copy(im)
    out = equalizationByNumpy(img)
    cv2.imwrite(savePath, out)


def equalizationByNumpy(image):
    hist, bins = np.histogram(image.flatten(), 256, [0, 256])
    # hist是亮度值出现次数的统计
    cdf = hist.cumsum()
    # cdf是出现次数的累积分布函数
    # 如果高灰度值没有次数，但累计分布函数会把它加入。但最后在索引生成新图像时舍去

    # 均衡化处理
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')

    # 生成新图像
    img2 = cdf[image]

    return img2

def changeImage():
    filePath = r'C:\PLY\Graduation Design\yolov5-master\own_datas\images\save\1'
    destPath = r'C:\PLY\Graduation Design\yolov5-master\own_datas\images\save\1_hist'
    if not os.path.exists(destPath):
        os.makedirs(destPath)
    for root, dirs, files in os.walk(filePath):
        for file in files:
            if file[-1]=='g':
                Process(os.path.join(filePath, file), os.path.join(destPath, file))
    print('Done')

if __name__ == '__main__':
    changeImage()


