#!/bin/bash

# Start FRR daemons
/usr/lib/frr/frrinit.sh start

# Drop into shell so the container stays alive
exec bash
