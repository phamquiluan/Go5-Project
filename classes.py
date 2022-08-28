from typing import Dict, List

from pydantic import BaseModel


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
    name: str = "text"
    ocr: str = ""


def int2xlsx(i):
    if i < 26:
        return chr(i + 65)
    return f"{chr(i // 26 + 64)}{chr(i % 26 + 65)}"


class Cell(Box):
    name: str = "cell"
    texts: List[Text] = []

    start_col: int = -1
    end_col: int = -1
    start_row: int = -1
    end_row: int = -1

    def get_excel_index(self, table_start_index=None):
        if table_start_index is None:
            table_start_index = 0
        if self.start_col == self.end_col and self.start_row == self.end_row:
            return f"{int2xlsx(table_start_index + self.start_col)}{table_start_index + self.start_row + 1}"
        return f"{int2xlsx(table_start_index + self.start_col)}{table_start_index + self.start_row + 1}:{int2xlsx(table_start_index + self.end_col)}{table_start_index + self.end_row + 1}"

    @property
    def ocr(self):
        return " ".join(t.ocr for t in self.texts)


class Table(Box):
    name: str = "table"
    cells: List[Cell] = []

    def indexing(self):
        CELL_INDEXING_TOLERANT = 10

        """Calc index for cells."""
        for cell_indexing_tolerant in range(CELL_INDEXING_TOLERANT, -1, -1):
            project_x = [c.xmin for c in self.cells] + [c.xmax for c in self.cells]
            project_x.sort()

            x_indexed_gaps = []  # idx, xmin, xmax
            idx = 0
            for i, x in enumerate(project_x[:-1]):
                if abs(x - project_x[i + 1]) > cell_indexing_tolerant:
                    x_indexed_gaps.append((idx, x, project_x[i + 1]))
                    idx += 1

            project_y = [c.ymin for c in self.cells] + [c.ymax for c in self.cells]
            project_y.sort()

            y_indexed_gaps = []  # idx, xmin, xmax
            idx = 0
            for i, y in enumerate(project_y[:-1]):
                if abs(y - project_y[i + 1]) > cell_indexing_tolerant:
                    y_indexed_gaps.append((idx, y, project_y[i + 1]))
                    idx += 1

            # start indexing
            for cell in self.cells:
                for idx, xmin, xmax in x_indexed_gaps:
                    if cell.xmin <= xmin:
                        cell.start_col = idx
                        break

                for idx, xmin, xmax in x_indexed_gaps:
                    if cell.xmax >= xmax:
                        cell.end_col = idx

            for cell in self.cells:
                for idx, ymin, ymax in y_indexed_gaps:
                    if cell.ymin <= ymin:
                        cell.start_row = idx
                        break

                for idx, ymin, ymax in y_indexed_gaps:
                    if cell.ymax >= ymax:
                        cell.end_row = idx

            # checking steps
            is_valid = True
            for cell in self.cells:
                if (
                    cell.start_row is None
                    or cell.end_row is None
                    or cell.start_col is None
                    or cell.end_col is None
                ):
                    is_valid = False
                    break

                if cell.start_row > cell.end_row or cell.start_col > cell.end_col:
                    is_valid = False
                    break

            if is_valid is True:
                break


def read_tables_from_list(input_list: List[Dict]) -> List[Table]:
    tables = []
    for item in input_list:
        if item["name"] != "table":
            continue
        new_table = Table(
            xmin=item["xmin"], ymin=item["ymin"], xmax=item["xmax"], ymax=item["ymax"]
        )
        new_table.cells = [
            Cell(xmin=i["xmin"], ymin=i["ymin"], xmax=i["xmax"], ymax=i["ymax"])
            for i in item["cells"]
        ]
        tables.append(new_table)
    return tables


def read_texts_from_list(input_list: List[Dict]) -> List[Text]:
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
                ocr=item["ocr"],
            )
        )
    return texts
