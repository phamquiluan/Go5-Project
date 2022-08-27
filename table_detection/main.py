import os
from http import HTTPStatus
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile

from table_detection import TableDetector

app = FastAPI()


@app.get("/health/live", response_model=None)
def get_health_live() -> bool:
    return True


def isImageFile(file: UploadFile = File(...)):
    return file.content_type in ["image/png", "image/jpeg"]


@app.post("/ai/infer")
async def process(file: UploadFile = File(...)):
    try:
        image = None
        if isImageFile(file):
            image = await file.read()
            image = np.fromstring(image, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            await file.close()
        else:
            raise HTTPException(
                status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value,
                detail="Do not support this file format",
            )
        assert image is not None

        table_detector: TableDetector = TableDetector.get_unique_instance()
        output: list = table_detector.process(image)
        return output
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=e.__repr__()
        )


if __name__ == "__main__":
    prj_root = Path(__file__).parent.parent.resolve()
    input_image = cv2.imread(os.path.join(prj_root, "sample.jpg"))

    table_detector: TableDetector = TableDetector.get_unique_instance()
    print(table_detector.process(input_image))
