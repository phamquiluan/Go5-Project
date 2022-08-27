import os
from pathlib import Path

import cv2

prj_root = Path(__file__).parent.parent.resolve()


class TextDetector:
    instance = None

    def __init__(self, weights_path=None):
        # init your model here
        if weights_path is None:
            weights_path = os.path.join(os.path.dirname(__file__), "weight.pth")
            assert os.path.exists(weights_path), weights_path

        # TODO: change this
        self.model = lambda x: [
            {
                "name": "text",
                "xmin": 100,
                "ymin": 100,
                "xmax": 200,
                "ymax": 200,
            }
        ]

    def process(self, image):
        output = self.model(image)
        return output

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
