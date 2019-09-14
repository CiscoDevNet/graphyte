# Configuration File

Graphyte requires a configuration file where the model owner will add some mandatory settings and others that are optional:

| Section | Setting | Mandatory/Optional | Example | Description |
|:------- |:------- |:------- |:------- |:------- |
| **[main]** | model | mandatory | model = HLD Customer ACME | Global name of the model. It will appear in all modules. |
| **[main]** | version | mandatory | version = 1.0 | Version of the model. |
| **[parameters]** | auth_params | optional | auth_params = ACME_params.xls | Worksheet with the list of authorised parameters for template validation. |
| **[layout]** | diagram_order | optional | diagram_order = Overview.svg,Sequence.uml,Architecture Components.uml,Service.yang | Desired order for the modules in the navigation menu. Use exact diagram filenames (spaces allowed). Comma separated. |
| **[layout]** | diagram_ignore_list | optional | diagram_ignore_list = topology.svg,l3vpn.yang | List of diagram files to skip processing into modules. Use exact diagram filenames (spaces allowed). Comma separated. |
| **[layout]** | pyang_uml_no | optional | pyang_uml_no = annotation,import,typedef | PYANG options to skip when converting YANG into UML. (Allowed values: uses,leafref,identity,identityref,typedef,annotation,import,circles,stereotypes. Default:annotation) |

![configfile.jpg](img/configfile.jpg)

