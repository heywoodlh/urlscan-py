FROM ubuntu:14.04
# Install Python.
RUN \
  apt-get update && \
  apt-get install -y python curl wget cron jq python-dev python-pip python-virtualenv python3 python3-pip && \
  pip3 install urlscan-py && \
  pip install csvkit && \
  rm -rf /var/lib/apt/lists/*

ADD crontab /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
#RUN touch /var/log/cron.log

COPY urlscanio.sh /
RUN chmod u+x /urlscanio.sh

# Define working directory.
WORKDIR /data

# Define default command.
#CMD ["bash"]
CMD touch /var/log/cron.log && cron && tail -f /var/log/cron.log
