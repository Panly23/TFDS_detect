import os
import YOLO_DJ
import global_var
import DJ_detect

def main():
    # YOLO_DJ.run_detect()
    file_path = []
    file_dir = r'C:\PLY\Graduation Design\GUI_design\DJ_detect\exp\labels\_4.txt'
    file_1 = (file_dir.split("\\"))[-1]
    print(file_1)
    file_2 = (file_1.split("."))[0]
    print(file_2)
    # for root, dirs, files in os.walk(file_dir):
    #     for file in files:
    #         if os.path.splitext(file)[1] == '.txt':
    #             file_path.append(os.path.join(root, file))
    # label_path = " ".join(file_path)
    # global_var.set_value('DJ_label', str(label_path))
    # DJ_detect.main()
    # if global_var.get_value('flag_DJ') == '0':
    #     print("无挡键螺栓松脱故障")
    # #     # self.label_21.setText("无挡键螺栓松脱故障")
    # if global_var.get_value('flag_DJ') == '1':
    #     print("有挡键螺栓松脱故障")
    # #     # self.label_21.setText("有挡键螺栓松脱故障")

if __name__ == '__main__':
    global_var._init()  # 初始化
    global_var.set_value('DJ_label', " ")  # 定义
    main()
