import json
import time
from functools import wraps
from typing import Dict, List

import cv2
import numpy as np

from classes import Table, Text


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


def draw(image, table_list: List[Table]):
    vis_image = image.copy()

    # draw cell
    for table in table_list:
        for cell in table.cells:
            cv2.rectangle(
                vis_image,
                (cell.xmin, cell.ymin),
                (cell.xmax, cell.ymax),
                get_random_color(),
                -1,
            )

    vis_image = vis_image // 2 + image // 2

    # draw table
    for table in table_list:
        cv2.rectangle(
            vis_image,
            (table.xmin, table.ymin),
            (table.xmax, table.ymax),
            (0, 0, 255),
            4,
        )

    # draw text
    for table in table_list:
        for cell in table.cells:
            for text in cell.texts:
                cv2.rectangle(
                    vis_image,
                    (text.xmin, text.ymin),
                    (text.xmax, text.ymax),
                    (255, 0, 0),
                    2,
                )

    # put text
    for table in table_list:
        for cell in table.cells:
            # for text in cell.texts:
            cv2.putText(
                vis_image,
                cell.ocr,
                (cell.xmin, cell.ymin),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1,
            )
    return vis_image


def load_json(json_path: str) -> List[Dict]:
    data = None
    with open(json_path) as ref:
        data = json.load(ref)
    assert data is not None, json_path
    return data


def draw_text(image, text_list: List[Text]):
    for text in text_list:
        cv2.rectangle(
            image, (text.xmin, text.ymin), (text.xmax, text.ymax), (255, 0, 0), 2
        )
    return image


def merge_text_table(tables: List[Table], texts: List[Text]):
    for table in tables:
        in_table_texts = [t for t in texts if t.get_intersection(table) > 0]

        for cell in table.cells:
            cell.texts = [
                t for t in in_table_texts if t.get_intersection(cell) / t.area > 0.4
            ]


def dump_excel(tables: List[Table], file_path):
    import xlsxwriter

    tables.sort(key=lambda x: x.ymin)

    workbook = xlsxwriter.Workbook(file_path)

    cell_format = workbook.add_format(
        {
            "align": "center",
            "valign": "vcenter",
        }
    )

    # creawte work sheet
    worksheet = workbook.add_worksheet(name="Table")

    table_start_index = 0
    for table in tables:
        for cell in table.cells:
            if cell.start_row == cell.end_row and cell.start_col == cell.end_col:
                worksheet.write(
                    table_start_index + cell.start_row,
                    cell.start_col,
                    cell.ocr,
                    cell_format,
                )
            else:
                worksheet.merge_range(
                    cell.get_excel_index(table_start_index), cell.ocr, cell_format
                )
        table_start_index = table_start_index + max(c.end_row for c in table.cells) + 2

    workbook.close()


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper
