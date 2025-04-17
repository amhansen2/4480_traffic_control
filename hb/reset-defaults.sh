#!/bin/bash
ip route del default
ip route add default via 10.0.15.4 dev eth0
exec bash
