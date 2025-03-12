# GUIdemo11.py
# Demo11 of GUI by PyQt5
# Copyright 2021 youcans, XUPT
# Crated：2021-10-20

import sys, math, sip

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from uiDemo11 import Ui_MainWindow  # 导入 uiDemo9.py 中的 Ui_MainWindow 界面类

class MyMainWindow(QMainWindow, Ui_MainWindow):  # 继承 QMainWindow 类和 Ui_MainWindow 界面类
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类

    def click_pushButton_1(self):  # 点击 pushButton_1 触发
        self.textEdit.append("当前动作：click_pushButton_1")
        self.textEdit.append("选择堆叠布局页面：page_0")
        self.stackedWidget.setCurrentIndex(0)  # 打开 stackedWidget > page_0
        self.label_1.setPixmap(QtGui.QPixmap("../image/fractal01.png"))
        return


if __name__ == '__main__':  # youcans, XUPT 2021

    app = QApplication(sys.argv)  # 在 QApplication 方法中使用，创建应用程序对象
    myWin = MyMainWindow()  # 实例化 MyMainWindow 类，创建主窗口
    myWin.show()  # 在桌面显示控件 myWin
    sys.exit(app.exec_())  # 结束进程，退出程序
