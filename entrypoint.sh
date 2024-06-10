#!/bin/bash

# # Remove existing security results directory
# rm -rf /results/jmeter/security > /dev/null 2>&1
echo "[INFO] Start Running Jmeter"

# Extracting the first parameter for wait-for-it.sh
target=$1
shift  # Remove the first parameter from the arguments list
echo "[INFO] Target: $target"

# Execute wait-for-it.sh with the first parameter
./wait-for-it.sh $target -t 60 -- echo "[INFO] Target is up"



# Run JMeter with the remaining parameters
echo "[INFO] jmeter args: $@"
jmeter "$@"
echo "[INFO] Running Jmeter"

# # Create directories for results
# mkdir -p /results/zap/html
# mkdir -p /results/zap/json

# Sleep for 10 seconds & then retrieve results from ZAP
sleep 10

download_file 

# Remove site in zap
