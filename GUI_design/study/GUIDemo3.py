# GUIdemo3.py
# Demo3 of GUI by PyQt5
# Copyright 2021 youcans, XUPT
# Crated：2021-10-08

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import uiDemo3  # 导入图像界面设计文件

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    MainWindow = QMainWindow()  # 创建主窗口
    ui = uiDemo3.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()  # 显示主窗口
    sys.exit(app.exec_())  # 在主线程中退出
