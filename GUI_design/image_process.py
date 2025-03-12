import numpy as np
from PIL import Image
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import sys
import os



def Process(filePath):
    img = cv2.imread(filePath)
    img_amsrcr = automatedMSRCR(img, [15, 80, 200])
    return img_amsrcr

# ------------------------------------------------------------#
# SSR
# retinex SSR
# # 用data数组里的最小数替代0
# np.nonzero(a) 取出a里面非零的数
# -----------------------------------------------------------#
def replaceZeroes(data):
    min_nonzero = min(data[np.nonzero(data)])  # 取data数组里除0外最小的数
    data[data == 0] = min_nonzero  # 把data数组里的0的数用 min_nonzero 替换掉
    return data


def SSR(src_img, size):
    L_blur = cv2.GaussianBlur(src_img, (size, size), 0)  # 高斯函数
    img = replaceZeroes(src_img)  # 去除0  这里为什么要去0 呢  我个人认为是后面有log运算 0不能运算
    L_blur = replaceZeroes(L_blur)  # 去除0

    dst_Img = cv2.log(img / 255.0)  # 归一化取log
    dst_Lblur = cv2.log(L_blur / 255.0)  # 归一化取log
    dst_IxL = cv2.multiply(dst_Img, dst_Lblur)  # 乘  L(x,y)=S(x,y)*G(x,y)
    log_R = cv2.subtract(dst_Img, dst_IxL)  # 减  log(R(x,y))=log(S(x,y))-log(L(x,y))

    dst_R = cv2.normalize(log_R, None, 0, 255, cv2.NORM_MINMAX)  # 放缩到0-255
    log_uint8 = cv2.convertScaleAbs(dst_R)  # 取整
    return log_uint8


def SSR_image(image):
    size = 3
    b_gray, g_gray, r_gray = cv2.split(image)  # 拆分三个通道
    # 分别对每一个通道进行 SSR
    b_gray = SSR(b_gray, size)
    g_gray = SSR(g_gray, size)
    r_gray = SSR(r_gray, size)
    result = cv2.merge([b_gray, g_gray, r_gray])  # 通道合并。
    return result


# ------------------------------------------------------#

# ------------------------------------------------------#
# MSR
# retinex MSR
# ------------------------------------------------------#
def MSR(img, scales):
    weight = 1 / 3.0  # 不同ssr的权重
    scales_size = len(scales)  # 做多少次ssr
    h, w = img.shape[:2]  # 宽高
    log_R = np.zeros((h, w), dtype=np.float32)  # 创建0数组

    for i in range(scales_size):  #
        img = replaceZeroes(img)  # 去0值
        L_blur = cv2.GaussianBlur(img, (scales[i], scales[i]), 0)  # 高斯函数
        L_blur = replaceZeroes(L_blur)  # 去0值
        dst_Img = cv2.log(img / 255.0)  # 归一化取log
        dst_Lblur = cv2.log(L_blur / 255.0)  # 归一化取log
        dst_Ixl = cv2.multiply(dst_Img, dst_Lblur)  # 乘  L(x,y)=S(x,y)*G(x,y)
        # 公式如下  也就是求三次 ssr  结果乘权重然后相加在一起。
        # log(R(x,y))=log(S(x,y))-log(L(x,y))
        #  log(R(x,y))=Weight1⋅log(Rσ1(x,y))+Weight2⋅log(Rσ2(x,y))+Weight3⋅log(Rσ3(x,y))
        log_R += weight * cv2.subtract(dst_Img, dst_Ixl)

    dst_R = cv2.normalize(log_R, None, 0, 255, cv2.NORM_MINMAX)  # 0-1 缩放到0-255
    log_uint8 = cv2.convertScaleAbs(dst_R)  # 取整
    return log_uint8


def MSR_image(image):
    scales = [15, 101, 301]  # 卷积核大小
    b_gray, g_gray, r_gray = cv2.split(image)  # 拆分通道 r g b
    b_gray = MSR(b_gray, scales)
    g_gray = MSR(g_gray, scales)
    r_gray = MSR(r_gray, scales)
    result = cv2.merge([b_gray, g_gray, r_gray])
    return result


# -----------------------------------------------------------#
# 这个求出来数据没有转换不能直接显示  MSRCR MSRCP调用
# -----------------------------------------------------------#
# SSR
def singleScaleRetinex(img, sigma):  # SSR
    # L(x,y)=S(x,y)*G(x,y)
    # log(R(x,y))=log(S(x,y))-log(L(x,y))
    retinex = np.log10(img) - np.log10(cv2.GaussianBlur(img, (0, 0), sigma))

    return retinex


# -----------------------------------------------------------#
# MSR  MSRCR MSRCP调用
def multiScaleRetinex(img, sigma_list):
    retinex = np.zeros_like(img)  # 创建0数组
    for sigma in sigma_list:  # 循环
        retinex += singleScaleRetinex(img, sigma)  # 高斯模糊
    #  log(R(x,y))=Weight1⋅log(Rσ1(x,y))+Weight2⋅log(Rσ2(x,y))+Weight3⋅log(Rσ3(x,y))
    # 加权求均值
    retinex = retinex / len(sigma_list)

    return retinex


# -----------------------------------------------------------#
# 这个函数求的是 色彩恢复因子Ci
def colorRestoration(img, alpha, beta):
    img_sum = np.sum(img, axis=2, keepdims=True)  # 按通道求和

    color_restoration = beta * (np.log10(alpha * img) - np.log10(img_sum))

    return color_restoration


# Simplest Color Balance  自动色阶平衡
# 按照一定的百分比去除最小和最大的部分，然后中间的部分重新线性量化到0和255之间。
def simplestColorBalance(img, low_clip, high_clip):
    # 这里 low_clip和high_clip 是经验值为认为设定的   0.01、0.99
    total = img.shape[0] * img.shape[1]  # 多少个像素点
    for i in range(img.shape[2]):  # 维度
        # np.unique对数据去重后从小到大排序
        # unique为从小到大排序的数组
        # counts不同元素的个数
        unique, counts = np.unique(img[:, :, i], return_counts=True)
        current = 0
        # 这个for循环 求出 下限 low_val 和 上限 high_val
        # 具体的原理我也不清楚
        # 从输出来讲缩小了像素值的范围  ，防止出现两极化现象。
        for u, c in zip(unique, counts):
            if float(current) / total < low_clip:
                low_val = u
            if float(current) / total < high_clip:
                high_val = u
            current += c  # 累加

        img[:, :, i] = np.maximum(np.minimum(img[:, :, i], high_val), low_val)  # 限定范围

    return img


# ----------------------------------------------------#
# “sigma_list”: [15, 80, 200],多尺度高斯模糊sigma值
# “G” : 5.0,增益
# “b” : 25.0,偏差
# “alpha” : 125.0,
# “beta” : 46.0,
# “low_clip” : 0.01,
# “high_clip” : 0.99
# ---------------------------------------------------#

def MSRCR(img, sigma_list, G, b, alpha, beta, low_clip, high_clip):
    # 这里加1 我个人认为是  图片数组里最小值为0  后面会有log计算  0值不能计算 所以加了1
    img = np.float64(img) + 1.0

    img_retinex = multiScaleRetinex(img, sigma_list)  # 求 MSR

    img_color = colorRestoration(img, alpha, beta)  # 色彩恢复因子Ci
    img_msrcr = G * (img_retinex * img_color + b)  # 加增益和偏差  求MSRCR

    # 直接线性量化
    for i in range(img_msrcr.shape[2]):
        img_msrcr[:, :, i] = (img_msrcr[:, :, i] - np.min(img_msrcr[:, :, i])) / \
                             (np.max(img_msrcr[:, :, i]) - np.min(img_msrcr[:, :, i])) * \
                             255
    # np.maximum(array1, array2)：逐位比较array1和array2，并输出两者的最大值。
    img_msrcr = np.uint8(np.minimum(np.maximum(img_msrcr, 0), 255))  # 限定范围  取整   小于0的都换成0
    img_msrcr = simplestColorBalance(img_msrcr, low_clip, high_clip)  # 自动色阶平衡

    return img_msrcr


# -------------------------------------------------------------------------#
# MSRCP
def MSRCP(img, sigma_list, low_clip, high_clip):
    img = np.float64(img) + 1.0

    intensity = np.sum(img, axis=2) / img.shape[2]  # 求三通道像素点平均值  二维

    retinex = multiScaleRetinex(intensity, sigma_list)  # 求 MSR

    intensity = np.expand_dims(intensity, 2)  # 扩展维度 3维
    retinex = np.expand_dims(retinex, 2)  # 扩展维度 3维

    intensity1 = simplestColorBalance(retinex, low_clip, high_clip)  # 自动色阶平衡
    # 直接线性量化
    intensity1 = (intensity1 - np.min(intensity1)) / \
                 (np.max(intensity1) - np.min(intensity1)) * \
                 255.0 + 1.0

    img_msrcp = np.zeros_like(img)

    # 根据原始的RGB的比例映射到每个通道
    for y in range(img_msrcp.shape[0]):
        for x in range(img_msrcp.shape[1]):
            B = np.max(img[y, x])  # 最大值
            A = np.minimum(256.0 / B, intensity1[y, x, 0] / intensity[y, x, 0])
            img_msrcp[y, x, 0] = A * img[y, x, 0]
            img_msrcp[y, x, 1] = A * img[y, x, 1]
            img_msrcp[y, x, 2] = A * img[y, x, 2]

    img_msrcp = np.uint8(img_msrcp - 1.0)  # 取整

    return img_msrcp


# ---------------------------------------------------------------------------------#
# automatedMSRCR
def automatedMSRCR(img, sigma_list):
    img = np.float64(img) + 1.0

    img_retinex = multiScaleRetinex(img, sigma_list)  # 求 MSR
    for i in range(img_retinex.shape[2]):  # 维度循环
        # unique()：返回参数数组中所有不同的值，并按照从小到大排序
        # unique 去重后重新排序的数组，count去重后 不同数据的个数
        unique, count = np.unique(np.int32(img_retinex[:, :, i] * 100), return_counts=True)  # 这里*了100 数据放大100倍

        for u, c in zip(unique, count):
            if u == 0:
                zero_count = c  # 数组中0的个数
                break
        #  下面数据/100 都是为了还原数据 因为上面*了100
        low_val = unique[0] / 100.0  # MSR 结果 img_retinex中的最小值
        high_val = unique[-1] / 100.0  # MSR 结果 img_retinex中的最大值

        # 下面这几行的原理我不是很清楚，我也没找到文献说明，
        # 看代码的输出 上面求得low_val = -2.13 ，high_val = 0.46
        # 经过for循环后 low_val = -0.47 ，high_val = 0.22
        # 我认为他是把最大值和最小值给收缩了，防止两极化现象
        for u, c in zip(unique, count):
            if u < 0 and c < zero_count * 0.1:
                low_val = u / 100.0
            if u > 0 and c < zero_count * 0.1:
                high_val = u / 100.0
                break

        # 限定范围  把高于high_val 和低于low_val 用 high_val、low_val代替 。
        img_retinex[:, :, i] = np.maximum(np.minimum(img_retinex[:, :, i], high_val), low_val)
        # 直接线性量化  0-255
        img_retinex[:, :, i] = (img_retinex[:, :, i] - np.min(img_retinex[:, :, i])) / \
                               (np.max(img_retinex[:, :, i]) - np.min(img_retinex[:, :, i])) \
                               * 255

    img_retinex = np.uint8(img_retinex)

    return img_retinex

# def changeImage(filePath):
#     image = Process(filePath)
#     return image

if __name__ == '__main__':
    Process()


