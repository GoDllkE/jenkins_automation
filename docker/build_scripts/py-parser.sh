#!/usr/bin/env bash
#
if [[ -d "$1" ]]; then
	ls "$1"
fi

# Capture from setup.py the required fields
MOD_NAME=$(grep 'name=' "$1" | cut -d '=' -f2 | sed "s/'//g;s/,//g" | tr -d [:space:])
MOD_VERS=$(grep 'version=' "$1" | cut -d '=' -f2 | sed "s/'//g;s/,//g" | tr -d [:space:])

# show captured content
echo "name: ${MOD_NAME}"
echo "version: ${MOD_VERS}"
