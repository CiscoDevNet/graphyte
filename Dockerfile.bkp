### 1. Get Linux
FROM alpine:3.7

### 2. Get Java via the package manager
RUN apk update \
&& apk upgrade \
&& apk add --no-cache bash \
&& apk add --no-cache --virtual=build-dependencies unzip \
&& apk add --no-cache curl \
&& apk add --no-cache openjdk8-jre \
&& apk add ttf-dejavu


### 3. Get Python, PIP
RUN apk add --no-cache python3 \
&& apk add python3-dev \
&& python3 -m ensurepip \
&& pip3 install --upgrade pip setuptools \
&& rm -r /usr/lib/python*/ensurepip && \
if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
rm -r /root/.cache

#### 4. SET JAVA_HOME environment variable
ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"

#### 5. System requirements via package manager
RUN apk add git \
&& apk add make \
&& apk --no-cache add gcc libc-dev libxml2-dev libxslt-dev \
&& apk add graphviz

#### 6. Install Graphyte
RUN cd /usr/local \
&& git clone https://github.com/CiscoDevNet/graphyte.git \
&& cd graphyte \
&& make all