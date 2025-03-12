
GDZC_path = r'C:\PLY\Graduation Design\software_GUI\save\0'
DJ_path = r'C:\PLY\Graduation Design\software_GUI\save\1'
SJB_path = r'C:\PLY\Graduation Design\software_GUI\save\3'

import sys, os
import global_var

i = 0
flag = 0
image_list = list()

def image_show(pic):
    global flag
    global image_list
    global i
    file_path = global_var.get_value('filePath')
    if file_path:
        image_list = list(x for x in os.listdir(file_path))
    num = len(image_list)
    if flag == 0:
        flag = 1
    if flag == 1:
        if pic < num:
            image_path = str(file_path + '/' + image_list[pic])
            global_var.set_value('image_path', image_path)
        else:
            i = -1
    return i

def GDZC_show(pic, pic_GDZC):
    GDZC_image_list = list(x for x in os.listdir(GDZC_path))
    if (GDZC_image_list[pic_GDZC].split("."))[0] == (image_list[pic].split("."))[0]:
        GDZC_image_path = str(GDZC_path + '/' + GDZC_image_list[pic_GDZC])
        global_var.set_value('GDZC_image_path', GDZC_image_path)
        global_var.set_value('flag_GDZC', "0")
    else:
        global_var.set_value('flag_GDZC', "1")

def DJ_show(pic, pic_DJ):
    DJ_image_list = list(x for x in os.listdir(DJ_path))
    if (DJ_image_list[pic_DJ].split("."))[0] == (image_list[pic].split("."))[0]:
        DJ_image_path = str(DJ_path + '/' + DJ_image_list[pic_DJ])
        global_var.set_value('DJ_image_path', DJ_image_path)
        global_var.set_value('flag_DJ', "0")
    else:
        global_var.set_value('flag_DJ', "1")

def SJB_show(pic, pic_SJB):
    SJB_image_list = list(x for x in os.listdir(SJB_path))
    if (SJB_image_list[pic_SJB].split("."))[0] == (image_list[pic].split("."))[0]:
        SJB_image_path = str(SJB_path + '/' + SJB_image_list[pic_SJB])
        global_var.set_value('SJB_image_path', SJB_image_path)
        global_var.set_value('flag_SJB', "0")
    else:
        global_var.set_value('flag_SJB', "1")