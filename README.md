# <{graphyte}>
Webdoc automation tool.

## Prerequisites

Graphyte requires Python 3.

Graphyte UML support requires:
- JAVA runtime environment.
- PlantUML version 1.2017.16, automatically installed by makefile.

## Files

```
graphyte/
├── CHANGES
├── graphyte.py
├── graphyte_gen.py
└── utils
    ├── html_utils.py
    ├── mod_template
    ├── param_utils.py
    ├── plantuml.jar
    └── template_utils.py
```

**graphyte_gen.py**: Graphyte core, generates one graphyte module per run.

**graphyte.py**: Graphyte wrapper, handles the execution of graphyte_gen.py for a set of modules belonging to the same model, in a simplified way.

**Important: Both files must be in the same folder.**

## Installation
Just do
``` bash
git clone...
cd graphyte
make all
```

## Execution

``` bash
python3 graphyte.py -d /path/to/input/dir/
```

## Author
Jorge Somavilla ([on LinkedIn](https://www.linkedin.com/in/jsomav/))