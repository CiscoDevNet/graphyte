# Graphyte Documentation

Graphyte is a general-purpose webdoc automation engine that supports the full project lifecycle (requirement capture, revision, design, development, Q&A, documentation).

## Introduction

Graphyte helps automate the creation of interactive, portable web documents that massively reduce the size and complexity of traditional documentation.

Features:

- Generation of dynamic web documentation.
- Interactive visualization of configuration and text files.
- Markup syntax for highlighting parameters in TXT, XML files.
- Support for diagrams in SVG format and in UML language.
- Version control.
- Integrated text editor for template review.
- Parameter extraction and validation.

As a general purpose documentation tool, the range of possible applications is unlimited:

- Cisco NSO project requirements / versioning / validation / design / reference.
- Network designs/LLD documents with device configurations.
- Interactive presentations
- Flow/Sequence/Component diagrams with supporting documents.
- Review of design specifications maintaining version control.
- etc

## How does it work

Graphyte requires a set of input files from the user. In turn, it generates and validates a standalone web based set of documents known as the graphyte "model".

![graphyte_components.png](img/graphyte_components.png)

A model is a set of web documents that are related to each other, and combined create the full representation of the target design the user is trying to build. It could be a series of network schematics with device configurations, a sequence diagram with extended information, a logic workflow and parametrized templates for an automation project, or your new flat's blueprints and notes.

Each of the HTML web documents that assemble the model is called a "module". A model may consist of one or more modules. The web page layout of a module has the following structure:

![model_areas.png](img/model_areas.png)


## Using graphyte step-by-step

1. Create your template files (.txt, .csv, .xml).
2. Create your diagrams (.svg, .uml).
3. Link diagram elements to their corresponding template.
4. (Optional) If parameter validation is desired, create your list of authorized parameters (.xls/.xlsx).
5. Create your graphyte.conf file.
6. Run graphyte
7. Verify execution log on graphyte.log file.
8. Review your generated model. Modify any templates using the text editor integrated in the viewer.
9. Generate new revisions of the model by updating the version number in the graphyte.conf file.

![graphyte_io.png](img/graphyte_io.png)

## Input Files

To generate a model, the user is required to provide a series of input files:

- Templates: These are basically text files with content that will show up in the viewer when triggered by mouse clicks on the diagram. The currently supported formats are Plain Text files (.txt), eXtensible Markup Language XML files (.xml) and Comma Separated Values files (.csv).
- Diagrams: The diagram files used with graphyte are also text-based. Currently supported formats are Unified Modeling Language UML (.uml) and Scalable Vector Graphics files (.svg). UML file support is achieved by graphyte via integration with the PlantUML tool. SVG is an XML-based image format for two-dimensional graphics. A variety of applications allow creating or exporting to SVG files, including Inkscape or Microsoft Visio.
- Variable list: Optionally, depending on which graphyte features the user is aiming for, additional input files may be needed. This is the case for example for input files with parameters, that graphyte can automatically validate against a user defined list of "allowed model parameters".
- graphyte.conf file: The user is required to include a small configuration file where a series of options can be set, including the name and version of the model.

### Templates

The ultimate objective of a model is to represent relevant information in the viewer area responding to user events (mouse clicks) on the different parts of the diagram.

This relevant information is provided to graphyte in the form of text files called "templates".

Templates may optionally include parameters. Graphyte provides syntax capabilities to support up to 4 types of parameters that will be recognized, processed and highlighted as such.

Take a look at the [Templates section](templates.md) for details on how to create graphyte templates.

### Diagrams

Graphyte diagrams allow the model designer to represent large amounts of information in a user-friendly and condensed way.

Graphyte diagrams are embedded into the HTML modules as SVG objects. Graphyte accepts as inputs either SVG diagrams, or UML diagrams that it will convert to SVG during execution.

Within the diagram, the model designer will link shapes or elements to target templates. By doing this, the shape becomes responsive to mouse clicks that will load the target template into the viewer.

The Diagrams Section provides more details on how to create graphyte-ready diagrams using several widely available tools.

### Variable list

blah

### Configuration file

## Output Files
### HTML Modules
### Log file

