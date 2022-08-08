Run these commands to install the model

```
pip install torch==1.4.0+cu100 torchvision==0.5.0+cu100 -f https://download.pytorch.org/whl/torch_stable.html
pip install -q mmcv terminaltables
git clone --branch v1.2.0 'https://github.com/open-mmlab/mmdetection.git'
cd "mmdetection"
pip install -r "/content/mmdetection/requirements/optional.txt"
python setup.py install
python setup.py develop
pip install -r {"requirements.txt"}
pip install pillow==6.2.1 
pip install mmcv==0.4.3
```

Clone the repo
```
git clone https://github.com/DevashishPrasad/CascadeTabNet.git
```

Download the Pretrained Model
```
gdown "https://drive.google.com/u/0/uc?id=1-QieHkR1Q7CXuBu4fp3rYrvDG9j26eFT"
```

Then run the code in table_detection.py


