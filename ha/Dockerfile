FROM ubuntu

RUN apt-get update
RUN apt-get -y install bash iproute2 net-tools tcpdump vim iputils-ping
RUN apt-get clean

COPY reset-defaults.sh /reset-defaults.sh
RUN chmod +x /reset-defaults.sh
CMD ["/reset-defaults.sh"]


