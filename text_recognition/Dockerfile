# syntax=docker/dockerfile:1.0.0-experimental
FROM nvidia/cuda:11.6.2-devel-ubuntu20.04 as base
# FROM nvidia/cuda:11.6.0-cudnn8-runtime-ubuntu18.04 as base

RUN apt-get update -qqy && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
  build-essential \
  cmake \
  curl \
  g++ \
  git \
  libsm6 \
  libxext6 \
  ffmpeg \
  libxrender1 \
  locales \
  pkg-config \
  poppler-utils \
  # python3.7 python3.7-dev python3.7-distutils \
  python3.8 python3.8-dev \
  python3-pip \
  software-properties-common \
  unzip \
  wget \
  && \
  update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 \
  && \
  apt-get clean && \
  apt-get autoremove && \
  rm -rf /var/lib/apt/lists/*

# Set locale
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LANG C.UTF-8

# Configure Python buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

# Set default python version
RUN rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python
RUN rm -f /usr/bin/pip && ln -s /usr/bin/pip3 /usr/bin/pip
RUN --mount=type=cache,target=/root/.cache \
	pip install "pip==19.3.1"

WORKDIR /code

# install ML model requirements.txt
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache \
	pip install -r requirements.txt

FROM base AS serve
# install serving deps
RUN --mount=type=cache,target=/root/.cache \
	pip install fastapi pydantic python-multipart "uvicorn[standard]"

COPY . .
EXPOSE 80

# download weight
RUN python -c "from text_recognition import TextRecognizer; TextRecognizer.get_unique_instance()"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
