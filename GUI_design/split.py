import os
import cv2
import global_var
import shutil

output_path = r'C:\PLY\Graduation Design\GUI_design\save'

def main():
    # 清空文件夹
    shutil.rmtree('C:/PLY/Graduation Design/GUI_design/save')
    os.mkdir('C:/PLY/Graduation Design/GUI_design/save')
    os.mkdir('C:/PLY/Graduation Design/GUI_design/save/0')
    os.mkdir('C:/PLY/Graduation Design/GUI_design/save/1')
    os.mkdir('C:/PLY/Graduation Design/GUI_design/save/2')
    os.mkdir('C:/PLY/Graduation Design/GUI_design/save/3')
    os.mkdir('C:/PLY/Graduation Design/GUI_design/save/4')
    os.mkdir('C:/PLY/Graduation Design/GUI_design/save/5')
    # yolo标签目录
    path_root_labels = global_var.get_value('path_labels')
    # 图像目录
    path_root_imgs = global_var.get_value('target_path')
    # 图像文件类型
    type_img = global_var.get_value('type_image')
    # 需要提取的类的编号
    cls_idx = ['0', '1', '2', '3', '4', '5']
    global output_path

    type = path_root_imgs.split(".")[1]
    if type != type_img:
        print("wrong file")
    if os.path.exists(path_root_labels) == True:
        f = open(path_root_labels, 'r+', encoding='utf-8')
        img = cv2.imread(path_root_imgs)
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
                            output_path = r'C:\PLY\Graduation Design\GUI_design\save\0'
                        if idx == 1:
                            output_path = r'C:\PLY\Graduation Design\GUI_design\save\1'
                        if idx == 2:
                            output_path = r'C:\PLY\Graduation Design\GUI_design\save\2'
                        if idx == 3:
                            output_path = r'C:\PLY\Graduation Design\GUI_design\save\3'
                        if idx == 4:
                            output_path = r'C:\PLY\Graduation Design\GUI_design\save\4'
                        if idx == 5:
                            output_path = r'C:\PLY\Graduation Design\GUI_design\save\5'
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
                # rot_name = path_root_imgs + '_' + str(count) + '.png'
                image_id = path_root_imgs.split("/")[-1]
                image_id = str(image_id).split(".")[0]
                rot_name = image_id + '_' + str(count) + '.png'
                save_roi = os.path.join(save_path, rot_name)
                cv2.imwrite(save_roi,img_roi)
            else :
                break
            # cv2.imshow("show", img_tmp)
            # c = cv2.waitKey(0)



if __name__ == '__main__':
    main()

