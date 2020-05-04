# <{graphyte}>
Webdoc automation tool.

## System requirements

Graphyte requires Python >3.6.

System requirements for UML support:
- JAVA runtime environment >1.8.
- Graphviz.

## Files

**graphyte_gen.py**: Graphyte core, generates one graphyte module per run.

**graphyte.py**: Graphyte wrapper, handles the execution of graphyte_gen.py for a set of modules belonging to the same model, in a simplified way.


## Installation

- Install [system requirements](##-Pre-requirements)

- Install graphyte
``` bash
git clone...
cd graphyte
make all
```

## Execution

``` bash
python graphyte.py -d /path/to/input/dir/
```

## Running Graphyte as container

Build docker image and execute command in ephemeral container.

```bash
docker build . -t graphyte-image
docker run --rm -t --name graphyte-container -v /path/to/local/inputs/dir:/inputs graphyte-image /bin/bash -c "cd /usr/local/graphyte/graphyte; python graphyte.py -d /inputs"
```

Or build image, run the container in daemon mode, execute any number of commands on it and then manually destroy the container after you are done.

```bash
docker build . -t graphyte-image
docker run --rm -dt --name graphyte-container -v /path/to/local/inputs/dir:/inputs graphyte-image
docker exec -w "/usr/local/graphyte/graphyte" graphyte-container /bin/bash -c "python graphyte.py -d /inputs"
(...)
docker kill graphyte-container
```

Or if you want to use Confluence upload feature, then log into the container and execute the commands from there (you need an interactive shell).

```bash
docker build . -t graphyte-image
docker run --rm -it --name graphyte-container -v /path/to/local/inputs/dir:/inputs graphyte-image /bin/bash
cd /usr/local/graphyte/graphyte
python graphyte.py -d /inputs
(...)
exit
docker kill graphyte-container
```

In all cases replace **/path/to/local/inputs/dir** with your inputs local file path (as per [graphyte documentation](https://ciscodevnet.github.io/graphyte/usage/)).

Finally remove your docker image.

``` bash
docker image rm graphyte-image
```

Note: you can adjust the timezone in your container OS like so:

```bash
docker exec -it graphyte-container /bin/bash
cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime
```

## Author
Jorge Somavilla (@cisco.com) ([contact](https://www.linkedin.com/in/jsomav/))