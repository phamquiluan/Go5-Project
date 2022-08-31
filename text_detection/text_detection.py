import os
from pathlib import Path

import easyocr

prj_root = Path(__file__).parent.parent.resolve()


class TextDetector:
    instance = None

    def __init__(self, weights_path=None):
        self.reader = easyocr.Reader(["en"])

        if weights_path is None:
            weights_path = os.path.join(os.path.dirname(__file__), "weight.pth")
            assert os.path.exists(weights_path), weights_path

    def process(self, image):
        outputs = []
        output = self.reader.readtext(image)

        for id, row in enumerate(output):
            box = {}
            box["name"] = str(id)
            box["xmin"] = row[0][0][0]
            box["xmax"] = row[0][2][0]
            box["ymin"] = row[0][0][1]
            box["ymax"] = row[0][2][1]

            outputs.append(box)

        return outputs

    @classmethod
    def get_unique_instance(cls):
        if cls.instance is None:
            # initialize instance
            cls.instance = cls()
        return cls.instance
