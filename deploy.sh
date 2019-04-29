#!/usr/bin/env bash
cd /home/ubuntu/devops
git fetch --all
git clean -f
git checkout master
git pull origin master
sudo docker rm -f metrippingnginxexporter
sh docker-cmd.sh
DOCKER_REGISTRY='eu.gcr.io/metripping-149707'
SERVICE='mt-nginx-monitor'
RELEASE_VERSION='0.1'
RELEASE_TAG=`date`
PROJECT_ID="metripping-149707"
image_name="mt-nginx-monitor"
image_tag="${RELEASE_TAG}:${RELEASE_VERSION}"
