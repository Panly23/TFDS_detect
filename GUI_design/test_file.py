import os
import sys
import cv2


def walk_dir(filePath, topdown=True):
    for root, dirs, files in os.walk(filePath, topdown):
        # for file in files:
        #     dir_name = os.path.join(root, file)
        #     # print(os.path.join(root, file))
        #     if os.path.isfile(full_name):
        for dir in dirs:
            if dir == '0':
                dir_name_0 = os.path.join(root, dir)
                for root_0, dir_0s, file_0s in os.walk(dir_name_0):
                    for file_0 in file_0s:
                        img = cv2.imread(os.path.join(root_0, file_0))
                        print(os.path.join(root_0, file_0))
                        cv2.imshow('',img)
                        cv2.waitKey(0)

        #
        #         # for file in files:
        #         print("yes")
        #         img_path = os.path.join(root, name)
        #         cv2.imshow(img_path)
        #         cv2.waitKey(0)
        #     if name == '1':
        #         print(os.path.join(name))
        #         print("no")

if __name__ == '__main__':
    walk_dir("save")
