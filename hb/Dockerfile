# ha/hb/Dockerfile
FROM ubuntu

RUN apt-get update && apt-get -y install \
    bash iproute2 net-tools tcpdump vim iputils-ping && \
    apt-get clean

CMD ["bash"]