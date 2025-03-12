# TFDS_detect
## Project introduction
The purpose of this project is to develop a set of automatic fault identification system for railway freight cars based on computer vision to solve the problems of low efficiency and high omission rate of traditional manual detection. The system locates the key parts through the yolov5 target detection network, realizes fault classification by combining SVM and deep learning algorithm, and is equipped with pyqt5 interactive interface, which can process TFDs images in real time and feed back fault information. The experiment shows that the false detection rate of the system is less than 2%, and the missing detection rate is less than 3%

## Functional characteristics
-* * inspection of key parts * *: positioning core components such as rolling bearings, gear keys and locking plates（ mAP@0.5 ≥ 0.99).
-* * multi type fault identification * *:
-Bearing oil leakage (SVM classification, false detection rate 1%, missing detection rate 0%)
-The retaining key bolt is loose (yolov5 detection, missed detection rate is 2.9%)
-Locking plate offset (SVM classification, false detection rate 1.67%)
-* * batch processing and visualization interface * *: supports batch import of image sets, and provides the function of fault result table and view one by one.
