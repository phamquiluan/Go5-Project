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


class TableRecognizer:
    instance = None

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

        return tables

    @classmethod
    def get_unique_instance(cls):
        if cls.instance is None:
            # initialize instance
            cls.instance = cls()
        return cls.instance
    
    def __non_oversegment(self, grid_cells, func_cells, intersect_ratio = 0.98):
        for func_cell in func_cells:
            fxmin, fymin, fxmax, fymax = func_cell
            
            idx = 0
            while idx < len(grid_cells):
                gxmin, gymin, gxmax, gymax = grid_cells[idx]
                grid_area = abs(gxmin - gxmax) * abs(gymin - gymax)
                
                w_intersect = min(gxmax, fxmax) - max(gxmin, fxmin)
                h_intersect = min(gymax, fymax) - max(gymin, fymin)
                intersect_area = 0 if (w_intersect < 0) or (h_intersect < 0) else w_intersect * h_intersect
                
                # delete grid_cell that has a large intersect area with one func_cell
                if (intersect_area / grid_area) > intersect_ratio:
                    del grid_cells[idx]
                    continue
                idx += 1        

    def __deduce_grid_cells(self, results, oversegment=True):
        tables = []
        func_cells = []
        rows = []
        cols = []
        grid_cells = []

        # classify the bboxes from raw output of model
        for idx, score in enumerate(results["scores"].tolist()):
            if score < self.__thresh:
                continue
            bbox = results["boxes"][idx].tolist() # xmin, ymin, xmax, ymax
            if results["labels"][idx] == 1:
                cols.append(bbox)
            elif results["labels"][idx] == 2:
                rows.append(bbox)
            elif results["labels"][idx] in (5,): # span cell only
                func_cells.append(bbox)
        
        # extract all grid cells from intersection between a row and a column 
        for row in rows:
            for col in cols:
                xmin, ymin, xmax, ymax = col[0], row[1], col[2], row[3]
                grid_cells.append([xmin, ymin, xmax, ymax])
        
        # eliminate oversegmentation on grid_cells
        if (not oversegment) or (0 <= oversegment <= 1):
            self.__non_oversegment(grid_cells, func_cells, intersect_ratio = oversegment)

        return grid_cells + func_cells

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __ge__(self, other):
        return (self.x >= other.x) and (self.y >= other.y)
    def __le__(self, other):
        return (self.x <= other.x) and (self.y <= other.y)
    def __gt__(self, other):
        return (self.x > other.x) and (self.y > other.y)
    def __lt__(self, other):
        return (self.x < other.x) and (self.y < other.y)
