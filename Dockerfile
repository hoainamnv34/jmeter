# Use Java 8 slim JRE
FROM openjdk:23-slim-bullseye
LABEL org.opencontainers.image.authors="hoainamnv34"

# JMeter version
ARG JMETER_VERSION=5.6.3 

# Install few utilities
RUN apt-get clean && \
    apt-get update && \
    apt-get -qy install \
                wget \
                telnet \
                iputils-ping \
                unzip

# Install JMeter
RUN   mkdir /jmeter \
      && cd /jmeter/ \
      && wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-$JMETER_VERSION.tgz \
      && tar -xzf apache-jmeter-$JMETER_VERSION.tgz \
      && rm apache-jmeter-$JMETER_VERSION.tgz

      
# # ADD all the plugins
# ADD jmeter-plugins/lib /jmeter/apache-jmeter-$JMETER_VERSION/lib

# # ADD the sample test
# ADD sample-test sample-test

# Set JMeter Home
ENV JMETER_HOME /jmeter/apache-jmeter-$JMETER_VERSION/

# Add JMeter to the Path
ENV PATH $JMETER_HOME/bin:$PATH

