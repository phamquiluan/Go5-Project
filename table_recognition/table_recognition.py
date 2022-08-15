import os
from pathlib import Path
# import cv2

prj_root = Path(__file__).parent.parent.resolve()

class TableRecognizer:
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
            "cell_list": [
                {
                    "name": "cell",
                    "xmin": 100,
                    "ymin": 100,
                    "xmax": 200,
                    "ymax": 200
                }
            ]
        }]

    def process(self, image, table_list : list):
        # TODO: do something here 
        output = self.model(image)
        return output

    @classmethod
    def get_unique_instance(cls):
        if cls.instance is None:
            # initialize instance
            cls.instance = cls()
        return cls.instance


def main():
    input_image = cv2.imread(os.path.join(prj_root, "sample.jpg"))
    input_table_list = [{
        "name": "table",
        "xmin": 100,  # TODO: update?
        "ymin": 100,
        "xmax": 200,
        "ymax": 200,
    }]

    # TODO: code here

    return [{
        "name": "table",
        "xmin": 100,
        "ymin": 100,
        "xmax": 200,
        "ymax": 200,
        "cell_list": [
            {
                "name": "cell",
                "xmin": "...",
                "ymin": "...",
                "xmax": "...",
                "ymax": "..."
            }
        ]
    }]

if __name__ == "__main__":
    main()
