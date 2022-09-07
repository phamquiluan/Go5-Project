# The Go5-Project: Extract Table from Image to Excel 
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/phamquiluan/Go5-Project/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/phamquiluan/Go5-Project/tree/main)
[![Docker Image CI](https://github.com/phamquiluan/Go5-Project/actions/workflows/docker-image.yml/badge.svg)](https://github.com/phamquiluan/Go5-Project/actions/workflows/docker-image.yml)


![](https://user-images.githubusercontent.com/24642166/115177933-6ca5b780-a0fa-11eb-810d-3a5daba2ef6e.gif)


# How to start

## Prerequisite
- GPU available (if not, remove the `runtime:nvidia` line in `docker-compose.yaml` file)
- docker-compose


## 1. Clone
```bash
git@github.com:phamquiluan/Go5-Project.git
```

## 2. Start up services
```bash
cd Go5-Project

COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose up --build
```

## 3. Open browser with url

```bash
localhost:8501  # you can update the port the .env file
```

![](https://user-images.githubusercontent.com/24642166/187752094-8af74653-77c7-4c27-8999-4198c988e42f.gif)
