import xml.etree.ElementTree as ET
import os

classes = ['GDZC','DJ','CZA','SJB','JCG','YZTH']  # 写自己的分类名
pre_dir = r'C:\PLY\毕设\yolov5-master\own_datas\labels\xml-test'  # xml文件所在文件夹
target_dir = r'C:\PLY\毕设\yolov5-master\own_datas\labels\txt-test'  # 想要存储txt文件的文件夹
path = os.listdir(pre_dir)

for path1 in path:
    tree = ET.parse(os.path.join(pre_dir, path1))
    root = tree.getroot()
    oo = []
    for child in root:
        if child.tag == 'filename':
            oo.append(child.text)  # 获得xml文件的名
            # print(child.text)
        for i in child:

            if i.tag == 'width':  # 获得图片的w
                oo.append(i.text)
                # print(i.text)
            if i.tag == 'height':  # 获得图片的h
                oo.append(i.text)
                # print(i.text)
            if i.tag == 'name':  # 获得当前框的class
                oo.append(i.text)
                # print(i.text)

            for j in i:
                if j.tag == 'xmin':  # 获得当前框的两个对角线上的点的两组坐标
                    oo.append(j.text)
                    # print(j.text)
                if j.tag == 'ymin':
                    oo.append(j.text)
                    # print(j.text)
                if j.tag == 'xmax':
                    oo.append(j.text)
                    # print(j.text)
                if j.tag == 'ymax':
                    oo.append(j.text)
                    # print(j.text)
    print(oo)
    filename = oo[0]  # 读取图片的名和宽高
    filename = os.path.split(filename)
    # print(filename)
    name, extension = os.path.splitext(filename[1])  # 获取xml名和后缀
    width = oo[1]
    dw = 1 / int(width)
    height = oo[2]
    dh = 1 / int(height)
    oo.pop(0)
    oo.pop(0)
    oo.pop(0)  # 删除三次oolist的0号元素

    back = []
    # print((len(oo))%5)
    for i in range(len(oo) // 5):
        for p in range(len(classes)):  # 划定class的序号
            if classes[p] == oo[5 * i]:  # str == str
                cl = p
                back.append(cl)
        x = (int(oo[5 * i + 1]) + int(oo[5 * i + 3])) / 2  # oo里的所有元素都是str，数字也是
        y = (int(oo[5 * i + 2]) + int(oo[5 * i + 4])) / 2  # 计算标注框的中心点的xy坐标
        w = int(oo[5 * i + 3]) - int(oo[5 * i + 1])
        h = int(oo[5 * i + 4]) - int(oo[5 * i + 2])  # 计算标注框的宽高
        back.append('{:.4f}'.format(x * dw))
        back.append('{:.4f}'.format(y * dh))
        back.append('{:.4f}'.format(w * dw))
        back.append('{:.4f}'.format(h * dh))
        # back.append(y*dh)
        # back.append(w*dw)
        # back.append(h*dh)#转换到0-1区间
    print(back)
    # dir=r'C:\Users\loadlicb\Desktop'#label文件夹名
    file = open(os.path.join(target_dir, name + '.txt'), 'w')
    for i in range(len(back)):
        l = ' '
        if (i + 1) % 5 == 0:
            l = '\n'
        file.writelines(str(back[i]) + l)  # over
