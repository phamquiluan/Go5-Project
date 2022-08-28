from math import floor
from math import ceil
def list_process(element):
    element.pop()
    x = element[0::2]
    y = element[1::2]
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    element = dict()
    element["xmin"]=floor(x_min)
    element["ymin"]=floor(y_min)
    element["xmax"]=ceil(x_max)
    element["ymax"]=ceil(y_max)
    return element
def run_inference(img_path, output_dir):
    from mmocr.utils.ocr import MMOCR
    import cv2
    # import os
    offset = 1
    
    mmocr = MMOCR(det='MaskRCNN_IC17', recog=None)

    results = mmocr.readtext(img_path, output='outputs/demo_text_det_pred.jpg')

    
    # print(results)
    results = results[0]["boundary_result"]
    results = list(map(list_process,results))
    # print(results)
    
    img = cv2.imread(img_path)
    

    for index, rec in enumerate(results):
        file_name = output_dir + "image" + str(index) + ".png"
        cropped_img = img[rec["ymin"]-offset:rec["ymax"]+offset, rec["xmin"]-offset:rec["xmax"]+offset]
        cv2.imwrite(file_name,cropped_img)
