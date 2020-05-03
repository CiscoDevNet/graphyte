all: plantuml setup install

install:
	chmod +x graphyte/graphyte.py graphyte/graphyte_gen.py

plantuml:
	curl -L https://sourceforge.net/projects/plantuml/files/1.2017.16/plantuml.1.2017.16.jar/download > graphyte/utils/plantuml.jar

setup:
	pip3 install -U .