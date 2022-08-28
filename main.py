import glob
import mimetypes
import os
from os import environ as env
from typing import List

import requests
import streamlit as st
from dotenv import load_dotenv
from tqdm import tqdm

from classes import Table, Text, read_tables_from_list, read_texts_from_list
from utility import dump_excel, load_json, merge_text_table, timeit

st.set_page_config(
    layout="centered", page_icon="🖱️", page_title="Interactive table app"
)
st.title("🖱️ Interactive table app")
st.write(
    """This app shows how you can use the [streamlit-aggrid](STREAMLIT_AGGRID_URL)
    Streamlit component in an interactive way so as to display additional content
    based on user click."""
)

# load env var
load_dotenv()
TABLE_DETECTION_PORT = env["TABLE_DETECTION_PORT"]
TABLE_RECOGNITION_PORT = env["TABLE_RECOGNITION_PORT"]
TEXT_DETECTION_PORT = env["TEXT_DETECTION_PORT"]
TEXT_RECOGNITION_PORT = env["TEXT_RECOGNITION_PORT"]


@timeit
def get_table(image_path):
    image_name = os.path.basename(image_path)
    url = f"http://localhost:{TABLE_RECOGNITION_PORT}/ai/infer"
    files = [
        (
            "file",
            (image_name, open(image_path, "rb"), mimetypes.guess_type(image_path)[0]),
        )
    ]
    response = requests.request("POST", url, files=files)
    return response.json()


@timeit
def get_ocr(image_path):
    image_name = os.path.basename(image_path)
    url = f"http://localhost:{TEXT_RECOGNITION_PORT}/ai/infer"
    files = [
        (
            "file",
            (image_name, open(image_path, "rb"), mimetypes.guess_type(image_path)[0]),
        )
    ]
    response = requests.request("POST", url, files=files)
    return response.json()


@timeit
def main():
    # image_path = "/home/luan/research/Go5-Project/sample.jpg"

    # # read table
    # output: List = get_table(image_path)
    # print(output)
    # tables: List[Table] = read_tables_from_list(output)

    # # read text
    # output: List = get_ocr(image_path)
    # texts: List[Text] = read_texts_from_list(output)

    # merge_text_table(tables, texts)

    # # indexing
    # for t in tables:
    #     t.indexing()

    # # image = cv2.imread(image_path)
    # # show(draw(image, tables))
    #
    # dump_excel(tables[1], "debug.xlsx")

    for image_path in tqdm(
        glob.glob("/home/luan/research/Go5-Project/data/images/*.jpg")
    ):
        if "eu-0050002" not in image_path:
            continue

        image_name = os.path.basename(image_path)
        file_name = os.path.splitext(image_name)[0]

        # read table
        output: List = load_json(
            f"/home/luan/research/Go5-Project/cache/table/{file_name}.json"
        )
        tables: List[Table] = read_tables_from_list(output)

        # read text
        output: List = load_json(
            f"/home/luan/research/Go5-Project/cache/ocr/{file_name}.json"
        )
        texts: List[Text] = read_texts_from_list(output)

        merge_text_table(tables, texts)

        # indexing
        for t in tables:
            t.indexing()

        dump_excel(tables, "debug.xlsx")
        # image = cv2.imread(image_path)
        # cv2.imwrite(f"debug/{image_name}", draw(image, tables))


if __name__ == "__main__":
    main()
