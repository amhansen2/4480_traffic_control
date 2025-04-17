FROM ubuntu

RUN apt-get update
RUN apt-get -y install bash iproute2 net-tools tcpdump vim iputils-ping
RUN apt-get clean

# add frr and ospf
RUN curl -s https://deb.frrouting.org/frr/keys.gpg | tee /usr/share/keyrings/frrouting.gpg > /dev/null
RUN echo "deb [signed-by=/usr/share/keyrings/frrouting.gpg] https://deb.frrouting.org/frr $(lsb_release -s -c) frr-stable" | tee -a /etc/apt/sources.list.d/frr.list
RUN apt-get update
RUN apt-get -y install frr frr-pythontools


# add zebra=yes and ospfd=yes in /etc/frr/daemons file 
#(don't know why zebra isn't automatically showing up but I keep getting this error)
RUN echo "zebra=yes" >> /etc/frr/daemons 
RUN sed -i 's/ospfd=no/ospfd=yes/' /etc/frr/daemons

# setup frr with my conf files
COPY frr.conf /etc/frr/frr.conf
COPY frr.sh /frr.sh
RUN chmod +x /frr.sh
ENTRYPOINT ["/frr.sh"]


