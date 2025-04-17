# 4480_traffic_control
---
## Setup once on POWDER

---
### 1. Clone the repo
```
git clone https://github.com/amhansen2/4480_traffic_control.git
```
---
### 2. Create 4 node topology
```
cd 4480_traffic_control
python3 orchestrator.py create
```

---
### Test
Jump onto router/host
```
docker exec -it 4480_traffic_control-r1-1 bash
```

test frr stuff
```
vtysh
```

ping (from ha)
```
ping 10.0.15.3
```

install and use traceroute to see different paths (from ha)
```
apt install -y traceroute
traceroute 10.0.15.3
```

---
### Other useful Docker commands:
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
