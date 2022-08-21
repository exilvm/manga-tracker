#!/usr/bin/env bash

sudo apt update && sudo apt -y upgrade

export DB_HOST=localhost DB_NAME=postgres DB_NAME_TEST=postgres DB_USER=postgres DB_PASSWORD=postgres PGPASSWORD=postgres DB_PORT=5432 DEBUG=manga-tracker:* TS_NODE_PROJECT=tsconfig.server.json TS_NODE_FILES=true ELASTIC_NODE=http://localhost:9200 BASE_URL=http://localhost:3000/api

pip install --user -r requirements.txt

npm i npm@latest @devcontainers/cli --global

npm i

npm run migrate:up 

cd web

npm i

