# 4480_traffic_control

## Setup once on POWDER

### 1. Clone the repo
```
git clone https://github.com/amhansen2/4480_traffic_control.git
```

### 2. Install docker:
```
cd 4480_traffic_control
./dockersetup
```

### 3. Instantiate the network by composing the containers
```
# need to run docker commands as root
sudo bash
# start up Docker containers as specified by config files
docker compose up -d
```



## Test FRR
docker exec -it 4480_traffic_control-r1-1 bash
 
then 
vtysh




#### Other useful Docker commands:
- see all containers and status
```
docker ps
```
- see all networks and status
```
docker network ls
```
- see more details of specific network
```
docker network inspect <network name>
```
- to attach to a running container, e.g., to execute commands in container
```
docker attach <container name>
```
- to detach from container and leave it running
```
Ctrl+P Ctrl+Q
```
- to take down all containers
```
docker compose down
```
