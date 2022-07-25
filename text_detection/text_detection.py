import torch, torchvision
import mmcv
import mmdet
import mmocr

from mmocr.utils.ocr import MMOCR


def main():
    img_file =""
    output_file = ""
    model_name = ""
    
    mmocr = MMOCR(det=model_name, recog=None)
    output = mmocr.readtext(img_file, print_result=True, output=output_file, export_format = "json")
    
    return output

if __name__ == '__main__':
    main()
