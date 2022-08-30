from os import environ as env
from typing import Dict, List

import cv2
import numpy as np
import pandas as pd
import requests
from classes import read_tables_from_list, read_texts_from_list
from dotenv import load_dotenv
from utility import dump_excel, get_random_color, merge_text_table

import streamlit as st

# load env var
load_dotenv()
TABLE_RECOGNITION_PORT = env["TABLE_RECOGNITION_PORT"]
TEXT_RECOGNITION_PORT = env["TEXT_RECOGNITION_PORT"]


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
            url = "http://table_recognition:80/ai/infer"
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
            url = "http://text_recognition:80/ai/infer"
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
                    xlsx_path = f"debug_{idx}.xlsx"
                    dump_excel([tables[idx]], xlsx_path)
                    with open(xlsx_path, "rb") as ref:
                        df = pd.read_excel(ref)
                        st.dataframe(df)
                        st.download_button(
                            "Download Excel File", ref, file_name=f"output_{idx}.xlsx"
                        )

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
        st.balloons()


if __name__ == "__main__":
    app()
