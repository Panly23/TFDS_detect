# GUIdemo2.py
# Demo2 of GUI by PqYt5
# Copyright 2021 Youcans, XUPT
# Crated：2021-10-06

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import Demo1

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    MainWindow = QMainWindow()  # 创建主窗口
    ui = Demo1.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()  # 显示主窗口
    sys.exit(app.exec_())  # 在主线程中退出
