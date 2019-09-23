## YANG Diagrams

Graphyte can render diagrams and add as modules with the help of [Pyang tool](https://pypi.org/project/pyang/).

Simply include your .yang modules as input files and Graphyte will process them into html modules with rendered UML style diagrams.

There are some options available for the model owner in the file graphyte.conf regarding YANG files:

- **diagram_ignore_list**: Use to provide a comma separated list of files that Graphyte should skip and not consider as modules.
- **pyang_uml_no**: Used to fine tune the conversion from YANG to UML. Multiple options are available in Pyang that allow the model owner to customize which YANG model constructs and elements to hide in the rendered diagram. Available options are:
    - uses
    - leafref
    - identity
    - identityref
    - typedef
    - annotation
    - import
    - circles
    - stereotypes
    
  For example, if we wish to remove from the diagram the YANG annotations and the imported modules, we will add the following to the graphyte.conf file:
  
```
  [layout]
  ...
  pyang_uml_no = annotation,import
```

Default value if no pyang_uml_no option is provided will be empty (include all yang artifacts in the representation).

Linking templates to YANG modules/diagrams is not supported.