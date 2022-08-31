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

export DOCKER_BUILDKIT=1
docker compose up
```

3. (optional) port forwarding if your app is running on a server

```bash
ssh -L 8501:localhost:8501 <username>@<server_ip_address>
```

![](https://user-images.githubusercontent.com/24642166/187080608-fbd3ae88-48fe-4a6d-bbe5-1a704098fcae.png)

![](https://user-images.githubusercontent.com/24642166/187080611-1c8b44b3-3332-48df-a7d2-8274d0e427da.png)
