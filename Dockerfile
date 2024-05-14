# Use Java 8 slim JRE
FROM openjdk:23-slim-bullseye
LABEL org.opencontainers.image.authors="hoainamnv34"

# JMeter version
ARG JMETER_VERSION=5.6.3 

# Install some utilities
RUN apt-get clean && \
    apt-get update && \
    apt-get -qy install \
                wget \
                telnet \
                iputils-ping \
                unzip \
                python3 \
                python3-pip

# Install JMeter
RUN   mkdir /jmeter \
      && cd /jmeter/ \
      && wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-$JMETER_VERSION.tgz \
      && tar -xzf apache-jmeter-$JMETER_VERSION.tgz \
      && rm apache-jmeter-$JMETER_VERSION.tgz


RUN pip3 install requests

# Set JMeter Home
ENV JMETER_HOME /jmeter/apache-jmeter-$JMETER_VERSION/

# Add JMeter to the Path
ENV PATH $JMETER_HOME/bin:$PATH


COPY tests /root
WORKDIR	$JMETER_HOME


COPY endpoint.py /endpoint.py

ENTRYPOINT ["python3", "/endpoint.py"]


