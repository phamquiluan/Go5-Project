import os
from typing import List
import sys

import yaml
sys.path.append('/home/daitama/Desktop/Go5/Go5-Project')

import cv2
from pydantic import BaseModel
from ABINet.demo import get_model, load, readtext
from text_detection.text_detection import TextDetector
from ABINet.configs import *
from ABINet.utils import Config

print("hello")



def show(img, name="disp", width=1000):
    """
    name: name of window, should be name of img
    img: source of img, should in type ndarray
    """
    cv2.namedWindow(name, cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow(name, width, 1000)
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


class Box(BaseModel):
    name: str = "box"
    xmin: int
    xmax: int
    ymin: int
    ymax: int

    @property
    def width(self):
        return max(self.xmax - self.xmin, 0)

    @property
    def height(self):
        return max(self.ymax - self.ymin, 0)


class Text(Box):
    name: str = "text"
    ocr: str = ""


class TextRecognizer:
    instance = None

    def __init__(self):
        import easyocr
        self.reader: easyocr.Reader = easyocr.Reader(["en"])

    def process(self, image, text_list: list):
        texts = self.reader.readtext(image, min_size=1, text_threshold=0.3)

        output = []
        for (location, ocr) in texts:
            xmin = int(location[0])
            xmax = int(location[2])
            ymin = int(location[1])
            ymax = int(location[3])

            new_text = Text(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, ocr=ocr)
            output.append(new_text)

        return output

    @classmethod
    def get_unique_instance(cls):
        if cls.instance is None:
            # initialize instance
            cls.instance = cls()
        return cls.instance


def draw(image, text_list: List[Text]):
    for text in text_list:
        cv2.rectangle(
            image, (text.xmin, text.ymin), (text.xmax, text.ymax), (255, 0, 0), 4
        )
    return image


def main():
    # image = cv2.imread("/home/luan/research/Go5-Project/sample.jpg")

    import glob

    from tqdm import tqdm

    for image_path in tqdm(
        glob.glob("/home/luan/research/Go5-Project/data/images/*.jpg")
    ):
        image_name = os.path.basename(image_path)
        file_name = os.path.splitext(image_name)[0]

        image = cv2.imread(image_path)

        model = TextRecognizer.get_unique_instance()
        texts = model.process(image, text_list=[])
        # cv2.imwrite(
        #     f"/home/luan/research/Go5-Project/debug/{image_name}",
        #     draw(image, texts)
        # )
        output = [t.dict() for t in texts]

        import json

        with open(
            f"/home/luan/research/Go5-Project/cache/ocr/{file_name}.json", "w"
        ) as ref:
            json.dump(output, ref)


if __name__ == "__main__":
    main()
