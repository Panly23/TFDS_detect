# TFDS_detect（Railway Freight Car Fault Detection System Based on Deep Learning）

## Project Overview
This project aims to develop a computer vision-based automated fault detection system for railway freight cars, addressing inefficiencies and high missed detection rates in traditional manual inspections. The system utilizes the YOLOv5 object detection network to locate critical components, combines SVM and deep learning algorithms for fault classification, and features a PyQt5 GUI for real-time TFDS image processing and fault feedback. Experimental results show the system achieves <2% false detection rate and <3% missed detection rate, meeting railway industry requirements.

## Key Features
- **Critical Component Detection**: Locates core components (bearings, retaining keys, locking plates) with mAP@0.5 ≥ 0.99
- **Multi-type Fault Recognition**:
  - Bearing oil leakage (SVM classifier: 1% false detection, 0% missed detection)
  - Retaining key bolt loosening (YOLOv5 detection: 2.9% missed detection)
  - Locking plate displacement (SVM classifier: 1.67% false detection)
- **Batch Processing & Visualization**: Supports batch image import with tabular results and per-image inspection
## System functions
- **Image preprocessing**：Enhance the original image using Laplace, histogram equalization, Log transform, and Retinex algorithm to improve uneven lighting.
- **Target area segmentation**: Using YOLOv5 network to locate and segment key components in TFDS images, reducing background interference.
- **Fault diagnosis**: SVM or deep learning methods were used for binary classification of different components to determine whether there is a "fault" or "no fault", and high accuracy (mAP ≈ 0.995) was obtained through experimental verification.
- **System interface**: Design a graphical interface using PyQt5 to achieve functions such as batch processing of images, viewing each image individually, and displaying fault detection results.
## Tech Stack
- **Algorithms**: YOLOv5 (object detection), SVM (fault classification)
- **Language**: Python 3.9
- **Libraries**: PyTorch 1.13.1, OpenCV, Scikit-learn, PyQt5
- **Annotation Tool**: Labelme
- **Preprocessing**: Retinex algorithm (illumination compensation)

## Installation & Usage
**1. Clone repository:**
```bash
git clone  https://github.com/YourUsername/TFDS_detect.git
cd TFDS_detect
```
**2. Create a virtual environment and install dependencies:**
```bash
conda create -n tfds_env python=3.9
conda activate tfds_env
pip install -r requirements.txt
```
For the YOLOv5 module, please refer to yolov5-master/requestations.txt.<br>

**3. data preparation:**
- **Image data**: Store the raw images collected by the TFDS system in `data/raw_images` (to be created by oneself)
- **Labeling data**: Use Labelme to label key components, and store the labeling results in `data/annotations`<br>

**4. model training:**
- **Object Detection (YOLOv5)**:<br> 
Run in the `yolov5 master` directory:
```bash
python train.py --data data.yaml --cfg yolov5s.yaml --weights yolov5s.pt --epochs 100
```
- **Fault classification (SVM/YOLOv5)**:<br> 
Select the corresponding classifier based on the actual components and run the training script (such as `HOG_SVM` master or custom SVM training script) under the corresponding module

## Launch GUI
Run in the `software_GUI` directory:
```bash
python GUI_software.py
```
The system interface supports batch processing of images, viewing each image individually, and displaying fault detection results.

## Project Structure
```bash
├── GUI_design/                # GUI 设计相关代码及配置
├── HOG_SVM-master/            # HOG+SVM 故障检测模块（含独立 README）
├── break_image/               # 原始故障图片
├── break_image_retinex/       # 经 Retinex 处理后的图片
├── gitbook/                   # 项目文档（GitBook 格式）
├── image_evaluate.py          # 图像评估脚本
├── software_GUI/              # 主系统 GUI 软件及相关代码
├── test/                      # 测试图片
├── test-1/                    # 其他测试图片及子目录
├── README.md                  # 本文档
└── yolov5-master/             # YOLOv5 模块（含多种配置及说明文件）
```
## Performance
| Component      | Precision (P) | Recall (R) | mAP@0.5 |
|--------------|--------------|------------|--------|
| Bearing       | 0.997        | 1.000      | 0.995  |
| Retaining Key | 0.999        | 1.000      | 0.995  |
| Locking Plate | 0.999        | 1.000      | 0.995  |

## Notes
- Adjust YOLOv5 training parameters (e.g., batch_size) based on hardware

- Custom dataset expansion requires `data.yaml` format configuration

- GUI interaction logic details in `src/GUI_software.py`
