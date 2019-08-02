FROM alpine:latest

# Install Python3 and urlscan-py.
RUN \
  apk update && \
  apk add python3 && \
  pip3 install urlscan-py

RUN mkdir /data
RUN mkdir -p /root/.urlscan/

CMD '/bin/ash'
