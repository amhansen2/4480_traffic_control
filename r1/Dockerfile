FROM ubuntu

# Install base networking/debug tools
RUN apt-get update && apt-get -y install \
    bash iproute2 net-tools tcpdump vim iputils-ping curl gnupg lsb-release && \
    apt-get clean

# Add FRR repository and install FRR and Python tools
RUN curl -s https://deb.frrouting.org/frr/keys.gpg | tee /usr/share/keyrings/frrouting.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/frrouting.gpg] https://deb.frrouting.org/frr $(lsb_release -s -c) frr-stable" | \
    tee -a /etc/apt/sources.list.d/frr.list && \
    apt-get update && \
    apt-get -y install frr frr-pythontools



# Enable OSPF daemon
RUN sed -i 's/ospfd=no/ospfd=yes/' /etc/frr/daemons
# Append Zebra and OSPF daemon enable configurations to /etc/frr/daemons
RUN echo -e "zebra=yes\nospfd=yes" >> /etc/frr/daemons

# Copy the router-specific FRR config
COPY frr.conf /etc/frr/frr.conf

# Default shell
CMD ["bash"]
