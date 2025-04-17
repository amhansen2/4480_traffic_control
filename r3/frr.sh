#!/bin/bash

# start FRR
/usr/lib/frr/frrinit.sh start

# keep container alive 
# src: https://medium.com/@haroldfinch01/how-to-keep-docker-container-running-after-starting-services-3111fbd702db
tail -f /dev/null