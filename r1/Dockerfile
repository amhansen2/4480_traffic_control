FROM ubuntu

RUN apt-get update && apt-get -y install \
    bash iproute2 net-tools tcpdump vim iputils-ping curl gnupg lsb-release frr frr-pythontools && \
    apt-get clean

RUN curl -s https://deb.frrouting.org/frr/keys.gpg | tee /usr/share/keyrings/frrouting.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/frrouting.gpg] https://deb.frrouting.org/frr $(lsb_release -s -c) frr-stable" | \
    tee -a /etc/apt/sources.list.d/frr.list && \
    apt-get update && \
    apt-get -y install frr frr-pythontools

RUN echo "zebra=yes" >> /etc/frr/daemons && \
    echo "ospfd=yes" >> /etc/frr/daemons
RUN sed -i 's/ospfd=no/ospfd=yes/' /etc/frr/daemons

COPY frr.conf /etc/frr/frr.conf
COPY frr.sh /frr.sh
RUN chmod +x /frr.sh
ENTRYPOINT ["/frr.sh"]


