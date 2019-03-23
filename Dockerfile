# OS
FROM ubuntu:xenial

###
MAINTAINER manu "manu@metripping.com"
###

ENV container docker

# User setup
RUN mkdir /home/ubuntu
RUN groupadd -r ubuntu
RUN useradd -u 1000 --no-log-init -r -g ubuntu -d /home/ubuntu ubuntu
RUN chown ubuntu:ubuntu /home/ubuntu


# Core components
RUN apt-get update
RUN apt-get install python-dev -y
RUN apt-get install python3-dev -y

#nginx setup
RUN mkdir -p /home/ubuntu/prometheus-custom-exporter && mkdir -p /mnt/logs && chown -R ubuntu:ubuntu /home/ubuntu && chown -R ubuntu:ubuntu /mnt/logs

#django setup
RUN  apt-get install software-properties-common -y
RUN  apt-add-repository universe -y
RUN  apt-get update -y
RUN  apt-get install python-pip -y

RUN  pip install virtualenv
RUN virtualenv -p /usr/bin/python3 /home/ubuntu/ver3.4
RUN  chown -R ubuntu /home/ubuntu/ver3.4
RUN /home/ubuntu/ver3.4/bin/pip install autoenv

RUN echo "export PYTHONIOENCODING=utf-8" >> /home/ubuntu/.bashrc
RUN echo "export PYTHONPATH=/home/ubuntu/prometheus-custom-exporter/" >> /home/ubuntu/.bashrc
RUN echo "source /home/ubuntu/ver3.4/bin/activate" >> /home/ubuntu/.bashrc
RUN /bin/bash -c "export PYTHONPATH=/home/ubuntu/prometheus-custom-exporter/"
RUN /bin/bash -c "source /home/ubuntu/ver3.4/bin/activate"
ENV BRANCH_NAME master
RUN cd /home/ubuntu && git clone https://66b7e54aec473b7a52b48c57dec3e6fc8a5c4831@github.com/VG13/NginxExporter.git
RUN /home/ubuntu/ver3.4/bin/pip install -r /home/ubuntu/prometheus-custom-exporter/requirements.txt
VOLUME /mnt/logs
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod 775 usr/local/bin/docker-entrypoint.sh
RUN ln -s usr/local/bin/docker-entrypoint.sh / # backwards compat
ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
