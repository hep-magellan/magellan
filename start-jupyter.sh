#!/usr/bin/env bash

# - This script sources the environment variables and starts up the jupyter notebook server

PORT=$1

if  [ -z "${PORT}" ]; then
	PORT=8890
	echo "PORT=${PORT}"
fi

source setup.sh
jupyter notebook --no-browser --port=${PORT}
