#!/usr/bin/env bash

sudo apt update && sudo apt -y upgrade

pip install --user -r requirements.txt

npm i npm@latest @devcontainers/cli --global

npm i

npm run migrate:up 

cd web

npm i

