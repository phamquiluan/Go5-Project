from os import environ as env
from typing import Dict, List

import cv2
import numpy as np
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

from classes import read_tables_from_list, read_texts_from_list
from utility import dump_excel, get_random_color, merge_text_table

# load env var
load_dotenv()
TABLE_DETECTION_PORT = env["TABLE_DETECTION_PORT"]
TABLE_RECOGNITION_PORT = env["TABLE_RECOGNITION_PORT"]
TEXT_DETECTION_PORT = env["TEXT_DETECTION_PORT"]
TEXT_RECOGNITION_PORT = env["TEXT_RECOGNITION_PORT"]


# def get_ocr(image_path):
#     image_name = os.path.basename(image_path)
#     url = f"http://localhost:{TEXT_RECOGNITION_PORT}/ai/infer"
#     files = [
#         (
#             "file",
#             (image_name, open(image_path, "rb"), mimetypes.guess_type(image_path)[0]),
#         )
#     ]
#     response = requests.request("POST", url, files=files)
#     return response.json()


st.set_page_config(layout="wide", page_icon="🖱️", page_title="Interactive table app")
st.title("👨‍💻 Table Extraction App")


def app():
    upload_file = st.file_uploader(label="Pick a file", type=["png", "jpg", "jpeg"])
    image = None
    if upload_file is not None:
        filename = upload_file.name
        filetype = upload_file.type
        filebyte = bytearray(upload_file.read())

        # cvt byte to image
        image = np.asarray(filebyte, dtype=np.uint8)
        image = cv2.imdecode(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        tables = []
        with st.spinner("🤖 Extracting Table Structure! "):
            url = f"http://localhost:{TABLE_RECOGNITION_PORT}/ai/infer"
            files = [
                (
                    "file",
                    (filename, filebyte, filetype),
                )
            ]
            response = requests.request("POST", url, files=files)
            response: List[Dict] = response.json()

            tables = read_tables_from_list(response)

        texts = []
        with st.spinner("🤖 Extracting Text Regions and OCR! "):
            url = f"http://localhost:{TEXT_RECOGNITION_PORT}/ai/infer"
            files = [
                (
                    "file",
                    (filename, filebyte, filetype),
                )
            ]
            response = requests.request("POST", url, files=files)
            response: List[Dict] = response.json()

            texts = read_texts_from_list(response)

        merge_text_table(tables, texts)
        tables.sort(key=lambda t: t.ymin)

        # image = draw(image, tables)
        tab1, tab2, tab3 = st.tabs(
            ["Tabular Data", "Table Visualization", "OCR Visualization"]
        )

        with tab1:
            st.header("Tabular Information")

            for idx, col in enumerate(st.columns(len(tables))):
                with col:
                    if len(tables) > 1:
                        st.header(f"Table {idx + 1}")

                    df = None
                    xslx_path = "debug.xlsx"
                    dump_excel([tables[idx]], xslx_path)
                    with open(xslx_path, "rb") as ref:
                        df = pd.read_excel(ref)
                    st.dataframe(df)

        with tab2:
            st.header("Table Detection & Recognition")
            for idx, col in enumerate(st.columns(len(tables) + 1)):
                with col:
                    if idx == 0:  # detection
                        vimage = image.copy()
                        for table in tables:
                            cv2.rectangle(
                                vimage,
                                (table.xmin, table.ymin),
                                (table.xmax, table.ymax),
                                (0, 0, 255),
                                4,
                            )
                        st.image(vimage)
                    else:  # recognition
                        vimage = image.copy()
                        for cell in tables[idx - 1].cells:
                            cv2.rectangle(
                                vimage,
                                (cell.xmin, cell.ymin),
                                (cell.xmax, cell.ymax),
                                get_random_color(),
                                -1,
                            )
                        st.image(vimage // 2 + image // 2)
        with tab3:
            st.header("OCR")
            vimage = image.copy()
            for table in tables:
                for cell in table.cells:
                    for text in cell.texts:
                        cv2.rectangle(
                            vimage,
                            (text.xmin, text.ymin),
                            (text.xmax, text.ymax),
                            (0, 0, 255),
                            2,
                        )

            for table in tables:
                for cell in table.cells:
                    for text in cell.texts:
                        cv2.putText(
                            vimage,
                            text.ocr,
                            (text.xmin, text.ymin),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 0, 0),
                            1,
                        )

            st.image(vimage)
        # for table in tables:
        #     df = None
        #     xslx_path = "debug.xlsx"
        #     dump_excel([table], xslx_path)
        #     with open(xslx_path, "rb") as ref:
        #         df = pd.read_excel(ref)
        #     st.dataframe(df)
        # placeholder.empty()
        # st.image(image, caption=["output"], width=1000)
        #     st.json(json.dumps(output))

        st.balloons()


if __name__ == "__main__":
    app()
