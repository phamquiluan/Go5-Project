import glob
import os

import cv2
import numpy as np
import requests

for image_path in glob.glob("../data/images/*.jpg"):
    image_name = os.path.basename(image_path)

    # predict
    with open(image_path, "rb") as ref:
        output = requests.request(
            method="POST"
            url="http://127.0.0.1:8080/predictions/dbnet",
            headers={},
            data={},
            files=
            data={
            "data": ref
        })
        print(output)

        print(output.text)


    # visualize
    # image = cv2.imread(image_path)
