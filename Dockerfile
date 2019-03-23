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
RUN apt-get install curl -y
RUN apt-get install python-dev -y
RUN apt-get install python3-dev -y
RUN apt-get install libpq-dev -y


#nginx setup
RUN mkdir -p /home/ubuntu/devops && mkdir -p /mnt/logs && chown -R ubuntu:ubuntu /home/ubuntu && chown -R ubuntu:ubuntu /mnt/logs

#django setup
RUN  apt-get update -y
RUN  apt-get install python-pip -y

RUN  pip install virtualenv
RUN virtualenv -p /usr/bin/python3 /home/ubuntu/ver3.4
RUN  chown -R ubuntu /home/ubuntu/ver3.4
RUN /home/ubuntu/ver3.4/bin/pip install autoenv

RUN echo "export PYTHONIOENCODING=utf-8" >> /home/ubuntu/.bashrc
RUN echo "export PYTHONPATH=/home/ubuntu/devops/" >> /home/ubuntu/.bashrc
RUN echo "source /home/ubuntu/ver3.4/bin/activate" >> /home/ubuntu/.bashrc
RUN /bin/bash -c "export PYTHONPATH=/home/ubuntu/devops/"
RUN /bin/bash -c "source /home/ubuntu/ver3.4/bin/activate"
ENV BRANCH_NAME master

# Install base dependencies
RUN apt-get update && apt-get install -y -q --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        libssl-dev \
        supervisor \
        vim \
        wget \
    && rm -rf /var/lib/apt/lists/*

RUN cd /home/ubuntu && git clone https://3a1305696a02c640d882cec27edb4d3857f9d641@github.com/messX/devops.git
RUN /home/ubuntu/ver3.4/bin/pip install -r /home/ubuntu/devops/requirements.txt
VOLUME /mnt/logs
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod 775 usr/local/bin/docker-entrypoint.sh
RUN ln -s usr/local/bin/docker-entrypoint.sh / # backwards compat
ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
