FROM ubuntu

# Install basic networking and debugging tools
RUN apt-get update && apt-get -y install \
    bash iproute2 net-tools tcpdump vim iputils-ping curl gnupg lsb-release frr frr-pythontools && \
    apt-get clean

# Add FRR repo and install FRR and OSPF tools
RUN curl -s https://deb.frrouting.org/frr/keys.gpg | tee /usr/share/keyrings/frrouting.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/frrouting.gpg] https://deb.frrouting.org/frr $(lsb_release -s -c) frr-stable" | \
    tee -a /etc/apt/sources.list.d/frr.list && \
    apt-get update && \
    apt-get -y install frr frr-pythontools

# Add zebra=yes and ospfd=yes in /etc/frr/daemons file
RUN echo "zebra=yes" >> /etc/frr/daemons && \
    echo "ospfd=yes" >> /etc/frr/daemons

# Enable OSPF daemon
RUN sed -i 's/ospfd=no/ospfd=yes/' /etc/frr/daemons

# Copy initial FRR config (optional, could be per-router config)
COPY frr.conf /etc/frr/frr.conf

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

