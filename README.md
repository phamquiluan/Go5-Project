# The Go5-Project

![](https://user-images.githubusercontent.com/24642166/115177933-6ca5b780-a0fa-11eb-810d-3a5daba2ef6e.gif)


# how to start

1. clone 
```bash
git@github.com:phamquiluan/Go5-Project.git
```
2. pin up services
```bash
cd Go5-Project
docker compose up
```
3. run stream lit app
```bash
streamlit run streamlit_app.py
```

![](https://user-images.githubusercontent.com/24642166/187080608-fbd3ae88-48fe-4a6d-bbe5-1a704098fcae.png)

![](https://user-images.githubusercontent.com/24642166/187080611-1c8b44b3-3332-48df-a7d2-8274d0e427da.png)


Project Board: https://github.com/users/phamquiluan/projects/3/views/1

# Prepare data

1. Download data from here and put to `data` dir: https://drive.google.com/drive/folders/1J_z-laBlG14Fps81FVrUJUjesdND_JTx?usp=sharing
2. The image dir path `$PWD/data/images`



# Dev guide

1. cd into your dir

```bash
# for example
cd text_detection
```

2. create venv

```bash
python3.9 -m venv env
. env/bin/activate
```

3. install requirements

```bash
pip install -r requirements.txt
```

4. dev

on your Python file.

# Docker guide

```
export DOCKER_BUILDKIT=1
export BUILDKIT_PROGRESS=plain
```

1. build single service

```
docker build -t table_detection -f table_detection/Dockerfile table_detection/
```

2. compose up

```
docker compose up --build
```
