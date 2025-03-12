"""
#-*-coding:utf-8-*-
"""
import os

# 文件夹路径
img_path = r'C:\PLY\Graduation Design\HOG_SVM-master\image\test_DJ_new'
# txt 保存路径
save_txt_path = r'C:\PLY\Graduation Design\HOG_SVM-master\label\test_DJ.txt'

# 读取文件夹中的所有文件
imgs = os.listdir(img_path)

# 图片名列表
names = []

# 过滤：只保留jpg结尾的图片
for img in imgs:
    if img.endswith(".jpg"):
        names.append(img)

txt = open(save_txt_path,'w')

for name in names:
    # name = name[:-4]    # 去掉后缀名.png
    if name[0] == "0":
        txt.write(name + ' ' + '0' + '\n')  # 逐行写入图片名，'\n'表示换行
    if name[0] == "1":
        txt.write(name + ' ' + '1' + '\n')  # 逐行写入图片名，'\n'表示换行
txt.close()
