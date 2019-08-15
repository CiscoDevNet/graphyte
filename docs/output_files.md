## Output Files

As a result of running graphyte successfully, graphyte will generate the **model** consisting of one **.html module** for each diagram input file. Additionally, it will create the **graphyte.log** file containing execution information.

The output files will be placed in a **/www** directory below the directory passed with -d option.

### HTML Modules

Graphyte will generate an HTML file for each of the modules that form the model. Apart from the diagram and the viewer area, the following fields are found on each module:

- **Title**: Composed by the name and version of the model (specified in graphyte.conf file), and the module name (extracted from the diagram file).
- **Zoom tool**: Allows zooming the diagram in and out for better visualization.
- **Module Parameters**: if the parameter analysis was performed as part of graphyte's execution, the results will show up here.
- **Navigation menu**, displaying all the available modules (HTML pages) and providing a way to jump from one to the other from within the browser. Navigation links are relative, so the HTML files must be in the same folder for them to work.
- **Text editor**: Templates can be edited from within the viewer using the integrated editor. After making the changes on the plain text document, the reviewer can download the modified file to his system. The template embedded in the current model will not be updated, the model is frozen on a fixed version. In order to incorporate the revised template, a new model version will need to be generated.


### Log file

The log file contains execution details useful for troubleshooting.