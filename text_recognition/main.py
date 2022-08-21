from typing import Union
from pathlib import Path
import os
import cv2
from http import HTTPStatus
import numpy as np

from fastapi import FastAPI, UploadFile, File, HTTPException
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

        text_detector : TextDetector = TextDetector.get_unique_instance()
        output : list = text_detector.process(image)
        return output
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail=e.__repr__()
        )
