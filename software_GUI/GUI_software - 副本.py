# GUIdemo11.py
# Demo11 of GUI by PyQt5
# Copyright 2021 youcans, XUPT
# Crated：2021-10-20

# 初始化全局变量
GDZC_path = r'C:\PLY\Graduation Design\software_GUI\save\0'
DJ_path = r'C:\PLY\Graduation Design\software_GUI\save\1'
SJB_path = r'C:\PLY\Graduation Design\software_GUI\save\3'

pic, pic_GDZC, pic_DJ, pic_SJB = 0, 0, 0, 0
i, j, k, m, n = 0, 0, 0, 0, 0

import sys, os, math, shutil

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsWidget,QApplication, QFileDialog, QMainWindow, QMessageBox
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *

from ui_software import Ui_MainWindow  # 导入 uiDemo9.py 中的 Ui_MainWindow 界面类

import image_retinex
import detect
import split
import global_var
import image_show
import SVM_GDZC
import SVM_SJB
import YOLO_DJ
import DJ_detect

class MyMainWindow(QMainWindow, Ui_MainWindow):  # 继承 QMainWindow 类和 Ui_MainWindow 界面类
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类
        self.label_5.setText(" ")
        self.label_7.setText(" ")
        self.label_8.setText(" ")
        self.label_9.setText(" ")
        self.label_10.setText(" ")

    def click_pushButton_1(self):  # 选择文件夹
        directory = QFileDialog.getExistingDirectory(self, "选择文件夹", "C:\\")  # 起始路径
        self.lineEdit.setText(directory)
        global_var.set_value('filePath', directory)  # 定义
        # 清空文件夹
        shutil.rmtree(r'C:\PLY\Graduation Design\software_GUI\exp')
        os.mkdir(r'C:\PLY\Graduation Design\software_GUI\exp')
        # 清空文件夹
        shutil.rmtree('C:/PLY/Graduation Design/software_GUI/save')
        os.mkdir('C:/PLY/Graduation Design/software_GUI/save')
        os.mkdir('C:/PLY/Graduation Design/software_GUI/save/0')
        os.mkdir('C:/PLY/Graduation Design/software_GUI/save/1')
        os.mkdir('C:/PLY/Graduation Design/software_GUI/save/2')
        os.mkdir('C:/PLY/Graduation Design/software_GUI/save/3')
        os.mkdir('C:/PLY/Graduation Design/software_GUI/save/4')
        os.mkdir('C:/PLY/Graduation Design/software_GUI/save/5')

        shutil.rmtree('C:/PLY/Graduation Design/software_GUI/DJ_detect/exp')
        os.mkdir('C:/PLY/Graduation Design/software_GUI/DJ_detect/exp')


    def click_pushButton_2(self):
        global i, j, k, m, n
        global pic, pic_GDZC, pic_DJ, pic_SJB

        font = QtGui.QFont()
        font.setFamily("Adobe 宋体 Std L")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        image_retinex.changeImage()
        detect.run_detect()
        split.main()

        i = image_show.image_show(pic)
        # 显示第一张图片
        image_path = global_var.get_value('image_path')
        image = QtGui.QPixmap(image_path).scaled(self.label_7.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.label_7.setPixmap(image)

        # 显示图片名称
        image_id = (str(image_path).split("/"))[-1]
        self.label_5.setText(image_id)

        # 显示滚动轴承
        image_show.GDZC_show(pic, pic_GDZC)
        if global_var.get_value('flag_GDZC') == "0":
            GDZC_image_path = global_var.get_value('GDZC_image_path')
            GDZC_image = QtGui.QPixmap(GDZC_image_path).scaled(self.label_8.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.label_8.setPixmap(GDZC_image)
        if global_var.get_value('flag_GDZC') == "1":
            self.label_8.setText("无图片")
            self.label_8.setFont(font)

        # 显示挡键
        image_show.DJ_show(pic, pic_DJ)
        if global_var.get_value('flag_DJ') == "0":
            DJ_image_path = global_var.get_value('DJ_image_path')
            DJ_image = QtGui.QPixmap(DJ_image_path).scaled(self.label_9.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.label_9.setPixmap(DJ_image)
        if global_var.get_value('flag_DJ') == "1":
            self.label_9.setText("无图片")
            self.label_9.setFont(font)

        # 显示锁紧板
        image_show.SJB_show(pic, pic_SJB)
        if global_var.get_value('flag_SJB') == "0":
            SJB_image_path = global_var.get_value('SJB_image_path')
            SJB_image = QtGui.QPixmap(SJB_image_path).scaled(self.label_10.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.label_10.setPixmap(SJB_image)
        if global_var.get_value('flag_SJB') == "1":
            self.label_10.setText("无图片")
            self.label_10.setFont(font)

        # 表格显示数据
        self.setWindowTitle('TFDS图像故障情况表')
        file_path = global_var.get_value('filePath')
        image_list = list(x for x in os.listdir(file_path))
        self.tableWidget.setRowCount(len(image_list))

        image_name_path = global_var.get_value('filePath')
        image_name = []
        for root, dirs, files in os.walk(image_name_path):
            for file in files:
                image_name.append(str(file))

        GDZC_list_path = r'C:\PLY\Graduation Design\software_GUI\save\0'
        GDZC_problem_list = []
        GDZC_list = []
        for root, dirs, files in os.walk(GDZC_list_path):
            for file in files:
                GDZC_list.append(file)
                if SVM_GDZC.Predict(os.path.join(GDZC_list_path, file)) == 0:
                    GDZC_problem_list.append('无故障')
                if SVM_GDZC.Predict(os.path.join(GDZC_list_path, file)) == 1:
                    GDZC_problem_list.append('有故障')

        DJ_list_path = r'C:\PLY\Graduation Design\software_GUI\save\1'
        global_var.set_value('DJ_path', DJ_list_path)
        YOLO_DJ.run_detect()
        DJ_problem_list = []
        DJ_list = []
        for root, dirs, files in os.walk(DJ_list_path):
            for file in files:
                DJ_list.append(file)
                txt_file = (file.split("\\"))[-1]
                txt_file = os.path.splitext(txt_file)[0] + '.txt'
                file_dir = os.path.join(r'C:\PLY\Graduation Design\software_GUI\DJ_detect\exp\labels', txt_file)
                global_var.set_value('DJ_label', file_dir)
                if DJ_detect.main() == 0:
                    DJ_problem_list.append("无故障")
                if DJ_detect.main() == 1:
                    DJ_problem_list.append("有故障")

        SJB_list_path = r'C:\PLY\Graduation Design\software_GUI\save\3'
        SJB_problem_list = []
        SJB_list = []
        for root, dirs, files in os.walk(SJB_list_path):
            for file in files:
                SJB_list.append(file)
                if SVM_SJB.Predict(os.path.join(SJB_list_path, file)) == 0:
                    SJB_problem_list.append('无故障')
                if SVM_SJB.Predict(os.path.join(SJB_list_path, file)) == 1:
                    SJB_problem_list.append('有故障')

        for j in range(len(image_name)):
            item = QTableWidgetItem(str(image_name[j]))
            self.tableWidget.setItem(j, 0, item)
            if (image_name[j].split("."))[0] == (GDZC_list[k].split("."))[0]:
                item = QTableWidgetItem(str(GDZC_problem_list[k]))
                self.tableWidget.setItem(j, 1, item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                k += 1
            else:
                item = QTableWidgetItem("无图片")
                self.tableWidget.setItem(j, 1, item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)

            if (image_name[j].split("."))[0] == (DJ_list[m].split("."))[0]:
                item = QTableWidgetItem(str(DJ_problem_list[m]))
                self.tableWidget.setItem(j, 2, item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                m += 1
            else:
                item = QTableWidgetItem("无图片")
                self.tableWidget.setItem(j, 2, item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)

            if (image_name[j].split("."))[0] == (SJB_list[n].split("."))[0]:
                item = QTableWidgetItem(str(SJB_problem_list[n]))
                self.tableWidget.setItem(j, 3, item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                n += 1
            else:
                item = QTableWidgetItem("无图片")
                self.tableWidget.setItem(j, 3, item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)

    def click_pushButton_3(self):
        global pic, pic_GDZC, pic_DJ, pic_SJB
        global i

        pic += 1
        i = image_show.image_show(pic)

        font = QtGui.QFont()
        font.setFamily("Adobe 宋体 Std L")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        if i != -1:
            # 显示图片
            image_path = global_var.get_value('image_path')
            image = QtGui.QPixmap(image_path).scaled(self.label_7.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.label_7.setPixmap(image)

            # 显示名字
            image_id = (str(image_path).split("/"))[-1]
            self.label_5.setText(image_id)

            # 显示滚动轴承
            if global_var.get_value('flag_GDZC') == "0":
                pic_GDZC += 1
            image_show.GDZC_show(pic, pic_GDZC)
            if global_var.get_value('flag_GDZC') == "0":
                GDZC_image_path = global_var.get_value('GDZC_image_path')
                GDZC_image = QtGui.QPixmap(GDZC_image_path).scaled(self.label_8.size(),
                                                                   aspectRatioMode=Qt.KeepAspectRatio)
                self.label_8.setPixmap(GDZC_image)
            if global_var.get_value('flag_GDZC') == "1":
                image_show.GDZC_show(pic, pic_GDZC)
                self.label_8.setText("无图片")
                self.label_8.setFont(font)

            # 显示挡键
            if global_var.get_value('flag_DJ') == "0":
                pic_DJ += 1
            image_show.DJ_show(pic, pic_DJ)
            if global_var.get_value('flag_DJ') == "0":
                DJ_image_path = global_var.get_value('DJ_image_path')
                DJ_image = QtGui.QPixmap(DJ_image_path).scaled(self.label_9.size(), aspectRatioMode=Qt.KeepAspectRatio)
                self.label_9.setPixmap(DJ_image)
            if global_var.get_value('flag_DJ') == "1":
                self.label_9.setText("无图片")
                self.label_9.setFont(font)

            # 显示锁紧板
            if global_var.get_value('flag_SJB') == "0":
                pic_SJB += 1
            image_show.SJB_show(pic, pic_SJB)
            if global_var.get_value('flag_SJB') == "0":
                SJB_image_path = global_var.get_value('SJB_image_path')
                SJB_image = QtGui.QPixmap(SJB_image_path).scaled(self.label_10.size(),
                                                                 aspectRatioMode=Qt.KeepAspectRatio)
                self.label_10.setPixmap(SJB_image)
            if global_var.get_value('flag_SJB') == "1":
                self.label_10.setText("无图片")
                self.label_10.setFont(font)
        else:
            self.label_7.setText("已加载完\n全部图片")
            self.label_7.setFont(font)
            self.label_8.setText("已加载完\n全部图片")
            self.label_8.setFont(font)
            self.label_9.setText("已加载完\n全部图片")
            self.label_9.setFont(font)
            self.label_10.setText("已加载完\n全部图片")
            self.label_10.setFont(font)
            self.label_5.setText(" ")


    def trigger_actHelp(self):  # 动作 actHelp 触发
        QMessageBox.about(self, "About",
                            """使用说明:\n1.待检测图片请全部放入文件夹中\n2.选择图片所在的文件夹，系统将依次完成图像预处理、图像分割、图像分类和故障判断\n3.点击退出，可以退出本系统""")
        return


if __name__ == '__main__':  #
    global_var._init()  # 初始化
    global_var.set_value('filePath', " ")  # 定义
    global_var.set_value('image_path', " ")
    global_var.set_value('GDZC_image_path', " ")
    global_var.set_value('SJB_image_path', " ")
    global_var.set_value('flag_GDZC', " ")
    global_var.set_value('flag_DJ', " ")
    global_var.set_value('flag_SJB', " ")
    global_var.set_value('DJ_path', " ")
    global_var.set_value('DJ_label', " ")
    app = QApplication(sys.argv)  # 在 QApplication 方法中使用，创建应用程序对象
    myWin = MyMainWindow()  # 实例化 MyMainWindow 类，创建主窗口
    myWin.show()  # 在桌面显示控件 myWin
    sys.exit(app.exec_())  # 结束进程，退出程序
