### 1. Get Linux
FROM centos/python-36-centos7

USER root

### 2. Get Java via the package manager
RUN yum install -y epel-release && \
    yum update -y && \
    yum install -y \
    java-1.8.0-openjdk \
    make \
    git \
    gcc \
    libc-dev \
    libxml2-dev \
    libxslt-dev \
    graphviz \
    ttf-dejavu && \
    yum upgrade -y python-setuptools


#### 4. SET JAVA_HOME environment variable
ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"



#### 6. Install Graphyte
RUN cd /usr/local \
&& git clone https://github.com/CiscoDevNet/graphyte.git \
&& cd graphyte \
&& make all