FROM ubuntu

# Install basic networking and debugging tools
RUN apt-get update && apt-get -y install \
    bash iproute2 net-tools tcpdump vim iputils-ping curl gnupg lsb-release && \
    apt-get clean

# Add FRR repo and install FRR and OSPF tools
RUN curl -s https://deb.frrouting.org/frr/keys.gpg | tee /usr/share/keyrings/frrouting.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/frrouting.gpg] https://deb.frrouting.org/frr $(lsb_release -s -c) frr-stable" | \
    tee -a /etc/apt/sources.list.d/frr.list && \
    apt-get update && \
    apt-get -y install frr frr-pythontools

# Enable OSPF daemon
RUN sed -i 's/ospfd=no/ospfd=yes/' /etc/frr/daemons

# Optional: copy initial FRR config (or handle via startup script instead)
COPY frr.conf /etc/frr/frr.conf

# Default to bash shell
CMD ["bash"]
