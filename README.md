# TFDS_detect
# Railway Freight Car Fault Detection System Based on Deep Learning

## Project Overview
This project aims to develop a computer vision-based automated fault detection system for railway freight cars, addressing inefficiencies and high missed detection rates in traditional manual inspections. The system utilizes the YOLOv5 object detection network to locate critical components, combines SVM and deep learning algorithms for fault classification, and features a PyQt5 GUI for real-time TFDS image processing and fault feedback. Experimental results show the system achieves <2% false detection rate and <3% missed detection rate, meeting railway industry requirements.

## Key Features
- **Critical Component Detection**: Locates core components (bearings, retaining keys, locking plates) with mAP@0.5 ≥ 0.99
- **Multi-type Fault Recognition**:
  - Bearing oil leakage (SVM classifier: 1% false detection, 0% missed detection)
  - Retaining key bolt loosening (YOLOv5 detection: 2.9% missed detection)
  - Locking plate displacement (SVM classifier: 1.67% false detection)
- **Batch Processing & Visualization**: Supports batch image import with tabular results and per-image inspection

## Tech Stack
- **Algorithms**: YOLOv5 (object detection), SVM (fault classification)
- **Language**: Python 3.9
- **Libraries**: PyTorch 1.13.1, OpenCV, Scikit-learn, PyQt5
- **Annotation Tool**: Labelme
- **Preprocessing**: Retinex algorithm (illumination compensation)

## Installation & Usage
### Environment Setup
```bash
conda create -n tfds python=3.9
conda activate tfds
pip install torch==1.13.1 torchvision
pip install pyqt5 labelme scikit-learn opencv-python

## **Workflow**

### **Data Preparation:**
- Store TFDS images in `data/raw_images`
- Annotate components using Labelme, save annotations to `data/annotations`

### **Model Training:**

### **Object detection (YOLOv5)**
```bash
python train.py --data data.yaml --cfg yolov5s.yaml --weights yolov5s.pt --epochs 100
