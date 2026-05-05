#!/bin/bash

# Get the first non-loopback IPv4 address
ip_address=$(ip -4 addr show scope global | awk '/inet/ {print $2}' | cut -d/ -f1 | head -n 1)

echo "$ip_address"

