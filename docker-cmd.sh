#!/usr/bin/env bash
sudo docker run -p 8080:8080 -v /home/ubuntu/logs:/mnt/logs --name metrippingnginxexporter metrippingnginxexporter