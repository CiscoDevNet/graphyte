# Graphyte Step-by-Step Guide

In order to generate a new model from scratch follow steps 1 to 6.

For subsequent model revisions, update your source files and re-run graphyte (step 6). 

|Step | Chapter(s) |
|:--- |:--- |
| 1. Create your **template files** (.txt, .csv, .xml). | [Creating Templates](templates.md) |
| 2. Create your **diagrams** (.svg, .uml). | [Creating SVG diagrams with Microsoft Visio](diagrams_visio.md) |
|  | [Creating SVG diagrams with Draw.io](diagrams_drawio.md) |
|  | [Creating SVG diagrams with Inkscape](diagrams_inkscape.md) |
|  | [Creating UML diagrams for Graphyte](diagrams_uml.md) |
| 3. **Link** diagram elements to their corresponding template. | [Linking Input Diagrams and Templates](linking.md) |
| 4. (Optional) If parameter validation is desired, create your list of **authorized parameters** (.xls/.xlsx). | [Creating a Variable List](variables.md) |
| 5. Create your **graphyte.conf** file. | [Graphyte Configuration File](configfile.md) |
| 6. Run graphyte. | [Running Graphyte](running.md) |

Your model is now generated. For model revision/troubleshooting:

|Step |
|:--- |
| 7. Verify execution log on graphyte.log file.|
| 8. Review your generated model. Update desired templates using the text editor integrated in the viewer. |
| 9. Update the version number in the graphyte.conf file. |
| 10. Run graphyte. A new revision of the model is generated. |


![graphyte_io.png](img/graphyte_io.png)
