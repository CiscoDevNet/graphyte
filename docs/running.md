## Running Graphyte

Once the model owner has created the templates and diagrams, linked them together, created the graphyte.conf file and optionally the variable worksheet, everything is ready to generate the graphyte model.

Place all the input files under the same directory. The directory path containing all the input files will be passed as argument to graphyte with -d option.

```
python3 graphyte.py -d /path/to/inputs/directory/
```

Note that there are no restrictions as to how input files should be organized below the directory specified with -d option. Graphyte will scan all subdirectories and fetch the relevant files required by the model.
