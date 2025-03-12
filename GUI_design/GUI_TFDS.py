import sys, math, sipbuild, os
import numpy as np      # 导入 numpy 并简写成 np
import shutil

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsWidget,QApplication, QFileDialog, QMainWindow, QMessageBox
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *

import image_process
import detect
import split
import SVM_GDZC
import SVM_SJB
import YOLO_DJ
import DJ_detect

import cv2

from ui_TFDS import Ui_MainWindow
import global_var

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类
        self.stackedWidget.setCurrentIndex(0)

    def click_pushButton_1(self):  # 打开图片
        global imgNamepath
        imgNamepath, imgType = QFileDialog.getOpenFileName(self, "+", "C:\\", "*.jpg;;*.png;;All Files(*)")
        img = QtGui.QPixmap(imgNamepath).scaled(self.label_2.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.stackedWidget.setCurrentIndex(1)  # 打开 stackedWidget > page_0
        self.label_2.setPixmap(img)
        global_var.set_value('target_path', imgNamepath)
        return

    def click_pushButton_2(self):  # 图像预处理
        image_new = image_process.Process(imgNamepath)
        image_src = cv2.cvtColor(image_new, cv2.COLOR_BGR2RGB)
        QtImg = QImage(image_src, image_src.shape[1], image_src.shape[0], image_src.shape[1] * 3, QImage.Format_RGB888)
        img_dis = QPixmap(QtImg).scaled(self.label_5.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.stackedWidget.setCurrentIndex(2)
        # 显示图片
        self.label_5.setPixmap(img_dis)
        img = QtGui.QPixmap(imgNamepath).scaled(self.label_6.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.label_6.setPixmap(img)
        return

    def click_pushButton_3(self):  # 保存
        img_dis = self.label_5.pixmap().toImage()
        fpath, ftype = QFileDialog.getSaveFileName(self, "保存", "C:\\", "*.jpg;;*.png;;All Files(*)")
        img_dis.save(fpath)
        global_var.set_value('target_path', fpath)
        return

    def click_pushButton_4(self):  #返回
        self.stackedWidget.setCurrentIndex(1)

    def click_pushButton_5(self):  #图片分类
        # 清空文件夹
        shutil.rmtree(r'C:\PLY\Graduation Design\GUI_design\exp')
        os.mkdir(r'C:\PLY\Graduation Design\GUI_design\exp')

        global img_0_path, img_1_path, img_3_path
        global flag_0 , flag_1, flag_3
        flag_0 = 0
        flag_1 = 0
        flag_3 = 0

        image_path = global_var.get_value('target_path')
        image_name = (image_path.split("/"))[-1]
        image_name_new = str(image_name).split(".")[0]

        detect.run_detect()

        file_dir = r'C:\PLY\Graduation Design\GUI_design\exp\labels'

        txt_name = image_name_new + '.txt'
        path_label = os.path.join(file_dir, txt_name)
        global_var.set_value('path_labels', path_label)

        if os.path.splitext(image_path)[1] == '.png':
            global_var.set_value('type_image', "png")
        if os.path.splitext(image_path)[1] == '.jpg':
            global_var.set_value('type_image', "jpg")

        split.main()

        self.stackedWidget.setCurrentIndex(3)
        image_split_path = r'C:\PLY\Graduation Design\GUI_design\exp'
        image_split_new = os.path.join(image_split_path, image_name)
        image_split = QtGui.QPixmap(image_split_new).scaled(self.label_28.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.label_28.setPixmap(image_split)

        data_dir = r'C:\PLY\Graduation Design\GUI_design\save'

        for root, dirs, files in os.walk(data_dir):
            for dir in dirs:
                if dir == '0':
                    dir_name_0 = os.path.join(root, dir)
                    if not os.listdir(dir_name_0):
                        flag_0 = 1
                        font = QtGui.QFont()
                        font.setFamily("Adobe 黑体 Std R")
                        font.setPointSize(16)
                        self.label_14.setFont(font)
                        self.label_13.setText("无图片")
                    else:
                        for root_0, dir_0s, file_0s in os.walk(dir_name_0):
                            for file_0 in file_0s:
                                img_0_path = os.path.join(root_0, file_0)
                                img_0 = QtGui.QPixmap(img_0_path).scaled(self.label_13.size(), aspectRatioMode=Qt.KeepAspectRatio)
                                self.label_13.setPixmap(img_0)
                if dir == '1':
                    dir_name_1 = os.path.join(root, dir)
                    if not os.listdir(dir_name_1):
                        flag_1 = 1
                        font = QtGui.QFont()
                        font.setFamily("Adobe 黑体 Std R")
                        font.setPointSize(16)
                        self.label_29.setFont(font)
                        self.label_29.setText("无图片")
                    else:
                        for root_1, dir_1s, file_1s in os.walk(dir_name_1):
                            for file_1 in file_1s:
                                img_1_path = os.path.join(root_1, file_1)
                                img_1 = QtGui.QPixmap(img_1_path).scaled(self.label_29.size(), aspectRatioMode=Qt.KeepAspectRatio)
                                self.label_29.setPixmap(img_1)
                if dir == '2':
                    dir_name_2 = os.path.join(root, dir)
                    if not os.listdir(dir_name_2):
                        font = QtGui.QFont()
                        font.setFamily("Adobe 黑体 Std R")
                        font.setPointSize(16)
                        self.label_31.setFont(font)
                        self.label_31.setText("无图片")
                    else:
                        for root_2, dir_2s, file_2s in os.walk(dir_name_2):
                            for file_2 in file_2s:
                                img_2_path = os.path.join(root_2, file_2)
                                img_2 = QtGui.QPixmap(img_2_path).scaled(self.label_31.size(), aspectRatioMode=Qt.KeepAspectRatio)
                                self.label_31.setPixmap(img_2)
                if dir == '3':
                    dir_name_3 = os.path.join(root, dir)
                    if not os.listdir(dir_name_3):
                        flag_3 = 1
                        font = QtGui.QFont()
                        font.setFamily("Adobe 黑体 Std R")
                        font.setPointSize(16)
                        self.label_33.setFont(font)
                        self.label_33.setText("无图片")
                    else:
                        for root_3, dir_3s, file_3s in os.walk(dir_name_3):
                            for file_3 in file_3s:
                                img_3_path = os.path.join(root_3, file_3)
                                img_3 = QtGui.QPixmap(img_3_path).scaled(self.label_33.size(),
                                                                         aspectRatioMode=Qt.KeepAspectRatio)
                                self.label_33.setPixmap(img_3)
                if dir == '4':
                    dir_name_4 = os.path.join(root, dir)
                    if not os.listdir(dir_name_4):
                        font = QtGui.QFont()
                        font.setFamily("Adobe 黑体 Std R")
                        font.setPointSize(16)
                        self.label_35.setFont(font)
                        self.label_35.setText("无图片")
                    else:
                        for root_4, dir_4s, file_4s in os.walk(dir_name_4):
                            for file_4 in file_4s:
                                img_4_path = os.path.join(root_4, file_4)
                                img_4 = QtGui.QPixmap(img_4_path).scaled(self.label_35.size(),
                                                                         aspectRatioMode=Qt.KeepAspectRatio)
                                self.label_35.setPixmap(img_4)
                if dir == '5':
                    dir_name_5 = os.path.join(root, dir)
                    if not os.listdir(dir_name_5):
                        font = QtGui.QFont()
                        font.setFamily("Adobe 黑体 Std R")
                        font.setPointSize(16)
                        self.label_37.setFont(font)
                        self.label_37.setText("无图片")
                    else:
                        for root_5, dir_5s, file_5s in os.walk(dir_name_5):
                            for file_5 in file_5s:
                                img_5_path = os.path.join(root_5, file_5)
                                img_5 = QtGui.QPixmap(img_5_path).scaled(self.label_37.size(), aspectRatioMode=Qt.KeepAspectRatio)
                                self.label_37.setPixmap(img_5)

    def click_pushButton_6(self):  # 故障识别
        # 清空文件夹
        shutil.rmtree(r'C:\PLY\Graduation Design\GUI_design\DJ_detect\exp')
        os.mkdir(r'C:\PLY\Graduation Design\GUI_design\DJ_detect\exp')

        self.stackedWidget.setCurrentIndex(4)
        # 判断轴承渗油
        if flag_0 == 1:
            font = QtGui.QFont()
            font.setFamily("Adobe 黑体 Std R")
            font.setPointSize(16)
            self.label_16.setFont(font)
            self.label_16.setText("无该部件图片")
            self.label_18.setText("无故障图片")
        else:
            GDZC_img = QtGui.QPixmap(img_0_path).scaled(self.label_16.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.label_16.setPixmap(GDZC_img)
            if SVM_GDZC.Predict(img_0_path) == 0:
                self.label_18.setText("无轴承渗油故障")
                self.label_18.adjustSize()
            if SVM_GDZC.Predict(img_0_path) == 1:
                self.label_18.setText("有轴承渗油故障")
                self.label_18.adjustSize()
        # 判断挡键螺栓松脱
        if flag_1 == 1:
            font = QtGui.QFont()
            font.setFamily("Adobe 黑体 Std R")
            font.setPointSize(16)
            self.label_19.setFont(font)
            self.label_19.setText("无该部件图片")
            self.label_21.setText("无故障图片")
        else:
            DJ_img = QtGui.QPixmap(img_1_path).scaled(self.label_19.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.label_19.setPixmap(DJ_img)
            global_var.set_value('DJ_path', img_1_path)
            print(global_var.get_value('DJ_path'))

            YOLO_DJ.run_detect()

            img_1_name = (img_1_path.split("\\"))[-1]
            txt_img_1_name = img_1_name.split(".")[0] + '.txt'

            file_dir = r'C:\PLY\Graduation Design\GUI_design\DJ_detect\exp\labels'
            label_path = os.path.join(file_dir, txt_img_1_name)
            global_var.set_value('DJ_label', label_path)

            flag = DJ_detect.main()

            if flag == 0:
                self.label_21.setText("无挡键螺栓松脱故障")
                self.label_21.adjustSize()
            if flag == 1:
                self.label_21.setText("有挡键螺栓松脱故障")
                self.label_21.adjustSize()
        # 判断锁紧板偏移
        if flag_3 == 1:
            font = QtGui.QFont()
            font.setFamily("Adobe 黑体 Std R")
            font.setPointSize(16)
            self.label_24.setFont(font)
            self.label_24.setText("无该部件图片")
            self.label_23.setText("无故障图片")
        else:
            SJB_img = QtGui.QPixmap(img_3_path).scaled(self.label_24.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.label_24.setPixmap(SJB_img)
            if SVM_SJB.Predict(img_3_path) == 0:
                self.label_23.setText("无锁紧板偏移故障")
                self.label_23.adjustSize()
            if SVM_SJB.Predict(img_3_path) == 1:
                self.label_23.setText("有锁紧板偏移故障")
                self.label_23.adjustSize()

    def click_pushButton_7(self):
        self.stackedWidget.setCurrentIndex(0)

    def trigger_actHelp(self):  # 动作 actHelp 触发
        QMessageBox.about(self, "About",
                          """使用说明 \n1.点击退出，可以退出本系统\n2.图像分类对未处理和处理后的图片均接受\n
                          """)
        return


if __name__ == '__main__':
    global_var._init()  # 初始化
    global_var.set_value('target_path', " ")  # 定义
    global_var.set_value('path_labels', " ")
    global_var.set_value('path_imgs', " ")
    global_var.set_value('type_image', " ")
    global_var.set_value('DJ_path', " ")
    global_var.set_value('DJ_label', " ")
    app = QApplication(sys.argv)  # 在 QApplication 方法中使用，创建应用程序对象
    myWin = MyMainWindow()  # 实例化 MyMainWindow 类，创建主窗口
    myWin.show()  # 在桌面显示控件 myWin
    sys.exit(app.exec_())  # 结束进程，退出程序



