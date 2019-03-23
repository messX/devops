cd /home/ubuntu/devops
git fetch --all
git clean -f
git checkout master
git pull origin master
sudo docker build -t metrippingnginxexporter .
sudo docker rm -f metrippingnginxexporter
sh docker-cmd.sh