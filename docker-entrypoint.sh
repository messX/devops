#!/usr/bin/env bash
cd /home/ubuntu/devops
git reset --hard
git clean -f
git fetch --all
git checkout $BRANCH_NAME
git pull
/home/ubuntu/ver3.4/bin/python3 collector.py