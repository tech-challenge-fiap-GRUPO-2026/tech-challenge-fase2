#!/bin/sh

xhost +local:docker

docker compose run --rm viewer

docker compose down 

xhost -local:docker