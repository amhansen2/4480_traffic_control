# ha/hb/Dockerfile
FROM ubuntu

RUN apt-get update && apt-get -y install \
    bash iproute2 net-tools tcpdump vim iputils-ping && \
    apt-get clean

COPY reset-defaults.sh /reset-defaults.sh
RUN chmod +x /reset-defaults.sh
CMD ["/reset-defaults.sh"]
