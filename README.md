# 4480_traffic_control

## Setup once on POWDER

### 1. Clone the assignment helper files:
```
git clone https://gitlab.flux.utah.edu/teach-studentview/cs4480-2025-s.git
```

### 2. Install docker:
```
cd cs4480-2025-s/pa3/part1/
./dockersetup
```

### 3. Instantiate your three node network: HostA < − > R1 < − > HostB
```
# need to run docker commands as root
sudo bash
# start up Docker containers as specified by config files
docker compose up -d
```

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
