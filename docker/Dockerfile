FROM alpine as builder
RUN apk --no-cache add git

RUN git clone https://github.com/heywoodlh/urlscan-py /opt/urlscan-py

FROM alpine:latest
LABEL maintainer=heywoodlh

# Copy cloned dir from builder
COPY --from=builder /opt/urlscan-py /opt/urlscan-py

# Install Python3 and urlscan-py.
RUN apk --no-cache add python3 py3-pip &&\ 
  pip3 install -r /opt/urlscan-py/requirements.txt

RUN mkdir /data
RUN mkdir -p /root/.urlscan/

ENTRYPOINT ["/opt/urlscan-py/bin/urlscan"]
