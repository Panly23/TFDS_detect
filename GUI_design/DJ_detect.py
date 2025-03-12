import os
import cv2
import global_var

flag = -1


def main():
    global flag
    # yolo标签目录
    path_label = global_var.get_value('DJ_label')
    # 需要提取的类的编号
    cls_idx = ['0', '1']

    if os.path.exists(path_label) == True:
        f = open(path_label, 'r+', encoding='utf-8')
        while True:
            line = f.readline()
            if line:
                msg = line.split(" ")
                cls = msg[0]
                flag = 0
                for idx in cls_idx:
                    if idx == cls:
                        flag = 1
                        if idx == '0':
                            flag = 0
                            # global_var.set_value('flag_DJ', "0")
                        if idx == '1':
                            flag = 1
                            # global_var.set_value('flag_DJ', "1")
                if flag == 0:
                    continue
            else:
                break
    return flag


if __name__ == '__main__':
    main()

