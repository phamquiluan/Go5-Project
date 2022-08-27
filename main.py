import mimetypes
import os
import time
from functools import wraps
from os import environ as env
from typing import Dict, List

import cv2
import numpy as np
import requests
from dotenv import load_dotenv
from pydantic import BaseModel


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

# load env var
load_dotenv()
TABLE_DETECTION_PORT=env["TABLE_DETECTION_PORT"]
TABLE_RECOGNITION_PORT=env["TABLE_RECOGNITION_PORT"]
TEXT_DETECTION_PORT=env["TEXT_DETECTION_PORT"]
TEXT_RECOGNITION_PORT=env["TEXT_RECOGNITION_PORT"]


class Box(BaseModel):
    name : str = "box"
    xmin : int
    xmax : int
    ymin : int
    ymax : int

    @property
    def width(self):
        return max(self.xmax - self.xmin, 0)

    @property
    def height(self):
        return max(self.ymax - self.ymin, 0)

    @property
    def area(self):
        return self.width * self.height

    def get_intersection(self, box):
        xmin = max(self.xmin, box.xmin)
        ymin = max(self.ymin, box.ymin)

        xmax = min(self.xmax, box.xmax)
        ymax = min(self.ymax, box.ymax)

        if xmin < xmax and ymin < ymax:
            return (xmax - xmin) * (ymax - ymin)
        return 0

class Text(Box):
    name : str = "text"
    ocr : str = ""

class Cell(Box):
    name : str = "cell"
    texts : List[Text] = []

    def is_valid(self):
        return self.width > CELL_MIN_WIDTH and self.height > CELL_MIN_HEIGHT


class Table(Box):
    name : str = "table"
    cells : List[Cell] = []

def read_tables_from_list(input_list : List[Dict]) -> List[Table]:
    tables = []
    for item in input_list:
        if item["name"] != "table":
            continue
        new_table = Table(
            xmin=item["xmin"],
            ymin=item["ymin"],
            xmax=item["xmax"],
            ymax=item["ymax"]
        )
        new_table.cells = [Cell(xmin=i["xmin"], ymin=i["ymin"], xmax=i["xmax"], ymax=i["ymax"]) for i in item["cells"]]
        tables.append(new_table)
    return tables

def read_texts_from_list(input_list : List[Dict]) -> List[Text]:
    texts = []
    for item in input_list:
        if item["name"] != "text":
            continue
        texts.append(
            Text(
                xmin=item["xmin"],
                ymin=item["ymin"],
                xmax=item["xmax"],
                ymax=item["ymax"],
                ocr=item["ocr"]
            )
        )
    return texts

@timeit
def get_table(image_path):
    image_name = os.path.basename(image_path)
    url = f"http://localhost:{TABLE_RECOGNITION_PORT}/ai/infer"
    files=[
      ('file',(image_name,open(image_path,'rb'), mimetypes.guess_type(image_path)[0]))
    ]
    response = requests.request("POST", url, files=files)
    return response.json()

@timeit
def get_ocr(image_path):
    image_name = os.path.basename(image_path)
    url = f"http://localhost:{TEXT_RECOGNITION_PORT}/ai/infer"
    files=[
      ('file',(image_name,open(image_path,'rb'), mimetypes.guess_type(image_path)[0]))
    ]
    response = requests.request("POST", url, files=files)
    return response.json()

def get_random_color():
    return tuple((np.random.random(3) * 153 + 102).astype(np.uint8).tolist())

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


def draw(image, table_list : List[Table]):
    vis_image = image.copy()

    # draw cell
    for table in table_list:
        for cell in table.cells:
            cv2.rectangle(vis_image, (cell.xmin, cell.ymin), (cell.xmax, cell.ymax), get_random_color(), -1)

    vis_image = vis_image // 2 + image // 2

    # draw table
    for table in table_list:
        cv2.rectangle(vis_image, (table.xmin, table.ymin), (table.xmax, table.ymax), (0, 0, 255), 4)

    # draw text
    for table in table_list:
        for cell in table.cells:
            for text in cell.texts:
                cv2.rectangle(vis_image, (text.xmin, text.ymin), (text.xmax, text.ymax), (255, 0, 0), 2)

    # put text
    for table in table_list:
        for cell in table.cells:
            for text in cell.texts:
                cv2.putText(
                    vis_image,
                    text.ocr,
                    (text.xmin, text.ymin),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 1)
    return vis_image


def draw_text(image, text_list : List[Text]):
    for text in text_list:
        cv2.rectangle(image, (text.xmin, text.ymin), (text.xmax, text.ymax), (255, 0, 0), 2)
    return image


def merge_text_table(tables : List[Table], texts : List[Text]):
    for table in tables:
        in_table_texts = [t for t in texts if t.get_intersection(table) > 0]

        for cell in table.cells:
            cell.texts = [t for t in in_table_texts if t.get_intersection(cell) / t.area > 0.4]

@timeit
def main():
    image_path = '/home/luan/research/Go5-Project/sample.jpg'

    # read table
    output : List = get_table(image_path)
    tables : List[Table] = read_tables_from_list(output)

    # read text
    output : List = get_ocr(image_path)
    texts : List[Text] = read_texts_from_list(output)

    merge_text_table(tables, texts)

    image = cv2.imread(image_path)
    show(draw(image, tables))





if __name__ == "__main__":
    main()
