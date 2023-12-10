FROM python:3.10

WORKDIR /code

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY streamlit_app.py classes.py utility.py /code/

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
