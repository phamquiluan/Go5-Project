import os
from pathlib import Path

import easyocr
import cv2

prj_root = Path(__file__).parent.parent.resolve()


class TextDetector:
    instance = None

    def __init__(self, weights_path=None):
        # init your model here

        self.reader = easyocr.Reader(['en'])

        if weights_path is None:
            weights_path = os.path.join(os.path.dirname(__file__), "weight.pth")
            assert os.path.exists(weights_path), weights_path

        # TODO: change this
        # self.model = lambda x: [
        #     {
        #         "name": "text",
        #         "xmin": 100,
        #         "ymin": 100,
        #         "xmax": 200,
        #         "ymax": 200,
        #     }
        # ]



    def process(self, image):
        outputs = []

        output = self.reader.readtext(image)
        
        for id, row in enumerate(output):
            box = {}
            box['name'] = str(id)
            box['xmin'] = row[0][0][0]
            box['xmax'] = row[0][2][0]
            box['ymin'] = row[0][0][1]
            box['ymax'] = row[0][2][1]

            outputs.append(box)

        return outputs

    @classmethod
    def get_unique_instance(cls):
        if cls.instance is None:
            # initialize instance
            cls.instance = cls()
        return cls.instance


def main():
    cv2.imread(os.path.join(prj_root, "sample.jpg"))

    # TODO: code here

    return [
        {
            "name": "table",
            "xmin": 100,
            "ymin": 100,
            "xmax": 200,
            "ymax": 200,
        }
    ]


if __name__ == "__main__":
    main()
