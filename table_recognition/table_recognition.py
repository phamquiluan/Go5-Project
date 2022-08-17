<<<<<<< HEAD
import glob
import os
from pathlib import Path
from typing import List

import cv2
import numpy as np
from pydantic import BaseModel
from tqdm import tqdm

CELL_MIN_WIDTH = 10
CELL_MIN_HEIGHT = 10
MIN_CELL_NUM_INSIDE_TABLE = 4


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


class Cell(Box):
    name: str = "cell"

    def is_valid(self):
        return self.width > CELL_MIN_WIDTH and self.height > CELL_MIN_HEIGHT


class Table(Box):
    name: str = "table"
    cells: List[Cell] = []


def get_random_color():
    return tuple((np.random.random(3) * 153 + 102).astype(np.uint8).tolist())


def draw(image, table_list: List[Table]):
    vis_image = image.copy()
    # for table in table_list:
    #     cv2.rectangle(image, (table.xmin, table.ymin), (table.xmax, table.ymax), (255, 0 ,0), 4)

    for table in table_list:
        for cell in table.cells:
            cv2.rectangle(
                vis_image,
                (cell.xmin, cell.ymin),
                (cell.xmax, cell.ymax),
                get_random_color(),
                -1,
            )

    return image // 2 + vis_image // 2


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

def ensure_gray(image):
    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except Exception:
        pass
    return image
=======
import os, sys
from pathlib import Path
import cv2
import math
from PIL import Image
>>>>>>> 6be06ee (Update driver code for module table_recognition)


lib_dir = os.path.join(Path(__file__).parent.resolve(), "table-transformer")
sys.path.append(lib_dir)
import core

class TableRecognizer:
    instance = None

<<<<<<< HEAD
    def __init__(self, weights_path=None):
        pass

    def process(self, image, table_list: list) -> List[Table]:
        # bin
        gray_image = ensure_gray(image)
        bin_image = cv2.adaptiveThreshold(
            ~gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10
        )
        vline = cv2.morphologyEx(
            bin_image, cv2.MORPH_OPEN, np.ones((image.shape[1] // 100, 1))
        )
        hline = cv2.morphologyEx(
            bin_image, cv2.MORPH_OPEN, np.ones((1, image.shape[1] // 100))
        )

        mask = cv2.bitwise_or(vline, hline)
        mask = cv2.dilate(mask, np.ones((3, 3)))

        # get hv table from mask
        cnts = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        cnts, hiers = cnts if len(cnts) == 2 else cnts[1:]
        if hiers is None:
            # TODO: there is no table
            pass
        else:
            hiers = hiers[0]

            tables = []
            for idx, cnt in enumerate(cnts):
                points = cnt[:, 0, :].tolist()
                xmin = min(p[0] for p in points)
                xmax = max(p[0] for p in points)
                ymin = min(p[1] for p in points)
                ymax = max(p[1] for p in points)

                new_table = Table(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

                child_idx = hiers[idx][2]
                while child_idx != -1:
                    points = cnts[child_idx][:, 0, :].tolist()
                    xmin = min(p[0] for p in points)
                    xmax = max(p[0] for p in points)
                    ymin = min(p[1] for p in points)
                    ymax = max(p[1] for p in points)
                    new_cell = Cell(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
                    if new_cell.is_valid():
                        new_table.cells.append(new_cell)
                    child_idx = hiers[child_idx][0]

                if len(new_table.cells) >= MIN_CELL_NUM_INSIDE_TABLE:
                    # new_table.indexing()
                    tables.append(new_table)
                else:  # this is frame
                    pass

        # show(draw(image, tables))
        # output = self.model(image)
        return tables
=======
    def __init__(self, weights_path = None):
        # init model
        if weights_path is None:
            weights_path = os.path.join(
                os.path.dirname(__file__),
                "weight.pth"
            ) 
            assert os.path.exists(weights_path), weights_path
        m = core.TableRecognizer(weights_path)
        
        self.__thresh = 0.95
        self.model = lambda x: m.predict(x, thresh=self.__thresh)

    def process(self, image, table_list : list):
        output = []
        for table in table_list:
            table["cell_list"] = []
            crop_tab = image[math.floor(table["ymin"]) - 15 : math.ceil(table["ymax"]) + 15, 
                             math.floor(table["xmin"]) - 15 : math.ceil(table["xmax"]) + 15]
            crop_tab = cv2.cvtColor(crop_tab, cv2.COLOR_BGR2RGB)
            crop_tab = Image.fromarray(crop_tab).convert("RGB")

            results = self.model(crop_tab)
            for idx, score in enumerate(results["scores"].tolist()):
                if score < self.__thresh:
                    continue
                if results["labels"][idx] not in [0, 6]:
                    xmin, ymin, xmax, ymax = list(map(int, results["boxes"][idx]))
                    table["cell_list"].append({
                        "name": "cell",
                        "xmin": xmin,
                        "ymin": ymin,
                        "xmax": xmax,
                        "ymax": ymax
                    })

            output.append(table)
        
        return output
>>>>>>> 6be06ee (Update driver code for module table_recognition)

    @classmethod
    def get_unique_instance(cls):
        if cls.instance is None:
            # initialize instance
            cls.instance = cls()
        return cls.instance
<<<<<<< HEAD
=======
import extract_table
import math

prj_root = Path(__file__).parent.parent.resolve()
=======
        
>>>>>>> 6be06ee (Update driver code for module table_recognition)

def main(show=False):
    input_image = cv2.imread(os.path.join(prj_root, "sample.jpg"))
    input_table_list = [{
        "name": "table",
        "xmin": 2.7792429e+02,
        "ymin": 2.6385663e+02,
        "xmax": 1.3853302e+03,
        "ymax": 9.6729169e+02,
    }]

<<<<<<< HEAD
    pos = []
    for tab in input_table_list:
        crop_img = input_image[math.floor(tab["ymin"])-15:math.ceil(tab["ymax"])+15, 
                               math.floor(tab["xmin"])-15:math.ceil(tab["xmax"])+15]
        #cv2.imshow('image',crop_img)
        #cv2.waitKey(0)

        # [...., [[x_max, y_max], [x_min, y_min]], ....]
        cell_boxes = extract_table.process_single_image(crop_img, show=show, save=False)
        
        pos.append(tab)
        tab["cell_list"] = []
        for cell in cell_boxes:
            tab["cell_list"].append({
                "name": "cell",
                "xmin": cell[1][0],
                "ymin": cell[1][1],
                "xmax": cell[0][0],
                "ymax": cell[0][1]
            })

    return pos

if __name__ == "__main__":
    print(main())
>>>>>>> c2458a5 (Table Cell implementation & show-off notebook)
=======
    table_recognizer = TableRecognizer(weights_path = os.path.join(lib_dir, "output", "pubtables1m_structure_detr_r18.pth"))
    output = table_recognizer.process(input_image, input_table_list)

    return output

if __name__ == "__main__":
    print(main())
>>>>>>> 6be06ee (Update driver code for module table_recognition)
