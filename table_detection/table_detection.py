import os
from pathlib import Path
import cv2
from mmdet.apis import init_detector, inference_detector, show_result_pyplot, show_result
import mmcv
import numpy as np
import math
from numpy import array, float32, size
from PIL import Image
def return_table(table_coordinates):

    tables_dict = []

    for table_data in table_coordinates:
        table_dict = {
            "name" : "table",
            "xmin" : table_data[0],
            "ymin" : table_data[1],
            "xmax" : table_data[2],
            "ymax" : table_data[3]
        }

        tables_dict.append(table_dict)
  
    return tables_dict

class TableDetector:
    instance = None

    def __init__(self, weights_path = None):
        # init your model here
        if weights_path is None:
            weights_path = os.path.join(
                os.path.dirname(__file__),
                "weight.pth"
            ) 
            assert os.path.exists(weights_path), weights_path
        
        # TODO: change this
        self.model = lambda x: [{
            "name": "table",
            "xmin": 100,
            "ymin": 100,
            "xmax": 200,
            "ymax": 200,
        }]

    def process(self, image):
        output = self.model(image)
        return output

    @classmethod
    def get_unique_instance(cls):
        if cls.instance is None:
            # initialize instance
            cls.instance = cls()
        return cls.instance

=======

def return_table(table_coordinates):

    tables_dict = []

    for table_data in table_coordinates:
        table_dict = {
            "name" : "table",
            "xmin" : table_data[0],
            "ymin" : table_data[1],
            "xmax" : table_data[2],
            "ymax" : table_data[3]
        }

        tables_dict.append(table_dict)
  
    return tables_dict
>>>>>>> a4b8a67 (add Install.md for model installation, code completed for table_detection)

def main():
    # Load model
    config_file = "/home/toan/Go5-Project/table_detection/CascadeTabNet/Config/cascade_mask_rcnn_hrnetv2p_w32_20e.py"
    checkpoint_file = "/home/toan/Go5-Project/table_detection/checkpoints/epoch_36.pth"
    
    model = init_detector(config_file, checkpoint_file, device='cuda:0')

    img = "/home/toan/Go5-Project/sample.jpg"
    
    # Run Inference
    result = inference_detector(model, img)

    table_coordinates = []

    ## extracting bordered tables
    for bordered_tables in result[0][0]:
	    table_coordinates.append(bordered_tables[:4].astype(int))

    ## extracting borderless tables
    for borderless_tables in result[0][2]:
	    table_coordinates.append(borderless_tables[:4].astype(int))
    
    table_data = return_table(table_coordinates)

    if len(table_data) != 0:
        # visualize the results in a new window
        show_result_pyplot(img, result,('Bordered', 'Cell', 'Borderless'), score_thr=0.5)
        
        # or save the visualization results to image files
        show_result(img, result, ('Bordered', 'Cell', 'Borderless'), out_file = "out_file.jpg")
    else:
        im1 = Image.open(img) 
  
        im1 = im1.save("out_file.jpg")

    for i in table_data:
        print(i)




if __name__ == "__main__":
    main()



