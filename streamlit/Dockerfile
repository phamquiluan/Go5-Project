FROM python:3.7

WORKDIR /code

COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY streamlit_app.py classes.py utility.py /code/

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
