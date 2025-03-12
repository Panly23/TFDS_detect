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

## Installation 
```bash
conda create -n tfds python=3.9
conda activate tfds
pip install torch==1.13.1 torchvision
pip install pyqt5 labelme scikit-learn opencv-python
```
## Usage
###1. **Clone repositoryn:**
- Store TFDS images in `data/raw_images`
- Annotate components using Labelme, save annotations to `data/annotations`

### **Model Training:**
```bash
# Object detection (YOLOv5)
python train.py --data data.yaml --cfg yolov5s.yaml --weights yolov5s.pt --epochs 100

# Fault classification (SVM)
python train_svm.py --dataset data/processed --class bearing
```
### Launch GUI
```bash
python src/GUI_software.py
```
## Project Structure
```bash
├── data/                 # Datasets
│   ├── raw_images/       # Raw TFDS images
│   ├── processed/        # Preprocessed images
│   └── annotations/      # Labelme annotations
├── models/               # Pretrained models
│   ├── yolov5s.pt
│   └── svm_classifier.pkl
├── src/                  # Source code
│   ├── preprocessing.py  # Image enhancement
│   ├── detection.py      # Object detection
│   └── GUI_software.py   # System GUI
└── docs/                 # Documentation
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
