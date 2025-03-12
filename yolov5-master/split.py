import os
import cv2
output_path = r'C:\PLY\Graduation Design\yolov5-master\own_datas\images\save_YZTH_broke'

def main():
    # yolo标签目录
    path_root_labels = r'C:\PLY\Graduation Design\yolov5-master\runs\detect\exp9\labels'
    # 图像目录
    path_root_imgs = r'C:\PLY\Graduation Design\yolov5-master\own_datas\images\YZTH_broke'
    #标签文件类型
    type_object = '.txt'
    # 图像文件类型
    type_img = 'png'
    # 需要提取的类的编号
    cls_idx = ['0', '1', '2', '3', '4', '5']
    global output_path


    for ii in os.walk(path_root_imgs):
        for j in ii[2]:
            type = j.split(".")[1]
            if type != type_img:
                continue
            path_img = os.path.join(path_root_imgs, j)
            print(path_img)
            label_name = j[:-4]+type_object
            path_label = os.path.join(path_root_labels, label_name)
            # print(path_label)
            if os.path.exists(path_label) == True:
                f = open(path_label, 'r+', encoding='utf-8')
                img = cv2.imread(path_img)
                w = img.shape[1]
                h = img.shape[0]
                new_lines = []
                count = 0
                while True:
                    line = f.readline()
                    if line:
                        img_tmp = img.copy()
                        msg = line.split(" ")
                        cls = msg[0]
                        flag = 0
                        for idx in cls_idx:
                            if idx == cls:
                                flag = 1
                                if idx == 0:
                                    output_path = r'C:\PLY\Graduation Design\yolov5-master\own_datas\images\save\0'
                                if idx == 1:
                                    output_path = r'C:\PLY\Graduation Design\yolov5-master\own_datas\images\save\1'
                                if idx == 2:
                                    output_path = r'C:\PLY\Graduation Design\yolov5-master\own_datas\images\save\2'
                                if idx == 3:
                                    output_path = r'C:\PLY\Graduation Design\yolov5-master\own_datas\images\save\3'
                                if idx == 4:
                                    output_path = r'C:\PLY\Graduation Design\yolov5-master\own_datas\images\save\4'
                                if idx == 5:
                                    output_path = r'C:\PLY\Graduation Design\yolov5-master\own_datas\images\save\5'
                        if flag == 0:
                            continue
                        # print(x_center,",",y_center,",",width,",",height)
                        x1 = int((float(msg[1]) - float(msg[3]) / 2) * w)  # x_center - width/2
                        y1 = int((float(msg[2]) - float(msg[4]) / 2) * h)  # y_center - height/2
                        x2 = int((float(msg[1]) + float(msg[3]) / 2) * w)  # x_center + width/2
                        y2 = int((float(msg[2]) + float(msg[4]) / 2) * h)  # y_center + height/2
                        print(x1,",",y1,",",x2,",",y2)
                        # cv2.rectangle(img_tmp,(x1,y1),(x2,y2),(0,0,255),5)
                        img_roi = img_tmp[y1:y2,x1:x2]
                        # cv2.imshow("show", img_roi)
                        # c = cv2.waitKey(0)
                        if os.path.exists(output_path) == False:
                            os.mkdir(output_path)
                        save_path = os.path.join(output_path, cls)
                        if os.path.exists(save_path) == False:
                            os.mkdir(save_path)
                        count +=1
                        rot_name = j + '_' + str(count) + '.png'
                        save_roi = os.path.join(save_path, rot_name)
                        cv2.imwrite(save_roi,img_roi)
                    else :
                        break
            # cv2.imshow("show", img_tmp)
            # c = cv2.waitKey(0)



if __name__ == '__main__':
    main()

