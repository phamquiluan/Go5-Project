from http import HTTPStatus

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile

from text_recognition import TextRecognizer

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

        ocr_model: TextRecognizer = TextRecognizer.get_unique_instance()
        output: list = ocr_model.process(image, text_list=[])
        return output
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=e.__repr__()
        )
