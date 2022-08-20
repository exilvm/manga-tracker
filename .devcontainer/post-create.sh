#!/usr/bin/env bash

# Update OS Packages
sudo apt update && sudo apt -y upgrade

# Install Dev Container CLI
npm i @devcontainers/cli --global
