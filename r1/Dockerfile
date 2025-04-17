FROM ubuntu

RUN apt-get update
RUN apt-get -y install bash iproute2 net-tools tcpdump vim iputils-ping traceroute
RUN apt-get clean

RUN apt-get install -y curl gnupg 
RUN curl -s https://deb.frrouting.org/frr/keys.gpg | tee /usr/share/keyrings/frrouting.gpg > /dev/null
RUN apt-get install -y lsb-release

ENV FRRVER=frr-stable
RUN echo "deb [signed-by=/usr/share/keyrings/frrouting.gpg] https://deb.frrouting.org/frr $(lsb_release -s -c) ${FRRVER}" | tee /etc/apt/sources.list.d/frr.list
RUN apt-get update
RUN apt-get install -y frr frr-pythontools

# add zebra=yes and ospfd=yes in /etc/frr/daemons file 
#(don't know why zebra isn't automatically showing up but I keep getting this error)
RUN echo "zebra=yes" >> /etc/frr/daemons 
RUN sed -i 's/ospfd=no/ospfd=yes/' /etc/frr/daemons

# setup frr with my conf files
COPY frr.conf /etc/frr/frr.conf
COPY frr.sh /frr.sh
RUN chmod +x /frr.sh


CMD ["tail", "-f", "/dev/null"]



