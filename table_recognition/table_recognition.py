import os
from pathlib import Path
# import cv2

prj_root = Path(__file__).parent.parent.resolve()

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
