#Run these commands to install the model and run the table detection module

##Go into your prefer directory and Clone the repo

```
mkdir Project
cd Project/
git clone https://github.com/phamquiluan/Go5-Project.git

cd Project/Go5-Project/table_detection
```

##Install the dependencies inside the table_detection directory

```
pip install torch==1.4.0+cu100 torchvision==0.5.0+cu100 -f https://download.pytorch.org/whl/torch_stable.html
pip install -q mmcv terminaltables

git clone --branch v1.2.0 'https://github.com/open-mmlab/mmdetection.git'
cd mmdetection/requirements
pip install -r optional.txt
python setup.py install
python setup.py develop

cd Project/Go5-Project/table_detection/mmdetection/
pip install -r requirements.txt
pip install pillow==6.2.1
pip install mmcv==0.4.3
```

##Clone the repo

```
cd Project/Go5-Project/table_detection
git clone https://github.com/DevashishPrasad/CascadeTabNet.git
```

##Download the Pretrained Model

```
gdown "https://drive.google.com/u/0/uc?id=1-mVr4UBicFk3mjUz5tsVPjQ4jzRtiT7V&export=download"
```

##Then run the code in table_detection.py
