## Linking input diagrams and templates

If everything goes as planned, graphyte will produce a series of web documents embedding both diagrams and templates. When the user selects active shapes of the diagram, the corresponding templates will be triggered and loaded into the viewer.

For this to be possible, there must be some association between a particular element in a diagram and one of the multiple input templates. Graphyte uses the **Hyperlink** field on diagram shapes to establish that association between shape and template. The model owner is required to add a hyperlink to each shape with the name of the target template to be loaded on a mouse-click event.

## Supported Link Types

Graphyte supports 3 types of links in diagrams:

- Links to templates

Used to show the contents of a template in the viewer when clicking on a particular shape. In order to achieve this, in your diagram, add a link to the shape. Add the name of the template in the href field (the path is not required). No additional tags are required.

    E.g.: href="my_template.txt"

 
- Links to other modules in the model

This allows the user to, by clicking on a shape in one module, load another one of the modules in the same model. In order to define this type of link, we must use the tag "mod:".

E.g.: Consider the following graphyte model called "Project ACME", which has 3 diagrams, that will generate 3 modules:

    Model = "Project ACME"

    Module 1 = foo.svg

    Module 2 = bar.svg

    Module 3 = baz.uml

In order to go from Module 1 to Module 2, the user could rely on the embedded navigation menu that graphyte adds to the model. But it is also possible to add a link to a shape in foo.svg, that will take the user directly to Module 2. In order to achieve this, the model owner can add a link to a shape in foo.svg with the content:

    href="mod:bar.svg"

(It is also possible to leave the extension out, as in **href="mod:bar"**).

The same applies for uml diagrams. However there is one thing the model owner needs to take care of. Plantuml syntax for hyperlinks does not allow spaces, while graphyte does allow spaces in diagram filenames. So in graphyte we could have a diagram file called "foo bar.uml". In order to link to that module from a plantuml diagram, model owner must remember to replace spaces (" ") by their percent encoding ("%20") sign: "foo%20bar.uml". This is not required for SVG diagrams.

- Links to any external URL

In order for graphyte not to interpret href field contents, the model owner must add it as a literal hyperlink with the tag "lit:".

This will be useful to link to URLs that graphyte should not process further.

    E.g.: href="lit:https://www.cisco.com/"

When clicking on the shape it will load the URL [https://www.cisco.com](https://www.cisco.com) in the browser.

## Link in YANG modules

It is not supported to link templates in YANG modules, only on UML and SVG modules.