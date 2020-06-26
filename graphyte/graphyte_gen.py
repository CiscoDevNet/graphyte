#!/usr/bin/env python3
"""graphyte_gen.py

Builds an individual graphyte module within a model.

Takes as input a diagram, and optionally templates and a
variable list, together with information about other modules
within the model in order to build a navigation menu.

Generates a standalone HTML module with embedded SVG diagram and
textfiles accessible via an interactive viewer.

"""

# imports
import os
import sys
import shutil
import argparse
import re
import logging
utils_path = os.path.abspath("utils")
if utils_path not in sys.path:
    sys.path.insert(0, utils_path)
from template_utils import add_templates_to_script
from param_utils import process_param_sheet, add_params_to_script
from html_utils import uml_2_svg, yang_2_uml, build_menu, build_html, process_svg
import pprint

# info
__author__ = "Jorge Somavilla"

# initialize logger
logger = logging.getLogger('graphyte')

pp = pprint.PrettyPrinter(indent=4)

class GraphyteModule(object):
    """Stores the attributes of the graphyte module.

    Attributes:
        model (str): Name of global graphyte model
        module (str): Name of current module.
        version (str): Model version.
        title (str): Model title.
        out_dir (str): Output directory.
        in_diagram_path (str): Path to input diagram.
        work_dir (str): Directory for temp runtime files.
        run_dir (str): Execution directory.
        file_dir (str): Input files directory.
        in_xls_path (str): Path to input variable list.
        menu_items (str): User specified navigation menu items.

    """
    def __init__(
            self, model, module, version, title, out_dir, in_diagram_path,
            work_dir, run_dir, file_dir, in_xls_path, menu_items, uml_no,
            changes_file
    ):
        """Initializes graphyte module instance. Builds attributes
        not specified by user.

        """
        self.model = model
        self.module = module
        self.model_no_sp = re.sub(r'\s+', r'_', model)
        self.module_no_sp = re.sub(r'\s+', r'_', module)
        self.version = re.sub(r'\s+', r'', version)
        if title == "":
            title = model + " v" + version + " - " + module
        self.title = title
        # create output dir if doesn't exist
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        self.out_html_path = os.path.join(
            out_dir + "/", self.model_no_sp + "_" + self.module_no_sp
            + "_v" + self.version + ".html"
        )
        self.in_diagram_path = in_diagram_path
        self.in_diagram_name = os.path.basename(in_diagram_path)
        self.out_html_name_no_ext = os.path.basename(
            os.path.splitext(self.out_html_path)[0]
        )
        # define work_dir if not specified
        if not work_dir:
            self.input_work_dir = False
            work_dir = os.path.join(out_dir, "work")
        else:
            self.input_work_dir = True
        # create work dir if doesn't exist
        if not os.path.isdir(work_dir):
            os.makedirs(work_dir)
        self.work_dir = work_dir
        self.run_dir = run_dir
        self.in_xls_path = in_xls_path
        self.file_dir = file_dir
        self.menu_items = menu_items
        self.svg_links = []
        self.svg_path = ""
        self.template_param_list = []
        self.decision_param_list = []
        self.invalid_param_found_alert = ""
        self.allowed_parameters = []
        self.menu_tags = ""
        self.pyang_uml_no = uml_no
        if changes_file:
            self.changes_file = changes_file
            self.changes_fname = os.path.basename(changes_file)
            self.changes_tab = "<li id=\"changes\" style=\"float:right\">Changes</li><li id=\"separator\" style=\"float:right\">|</li>"
        else:
            self.changes_file = ""
            self.changes_fname = ""
            self.changes_tab = ""

    def diagram_is_yang(self):
        """Whether the diagram is of type YANG or not

        :return: True if YANG, False otherwise.

        """
        return os.path.splitext(self.in_diagram_path)[1] == ".yang"

    def diagram_is_uml(self):
        """Whether the diagram is of type UML or not

        :return: True if UML, False otherwise.

        """
        return os.path.splitext(self.in_diagram_path)[1] == ".uml"

    def push_link(self, link):
        """Adds new entry to list of SVG linked files

        :param link: name of file linked in the SVG.
        :return: Node
        """
        self.svg_links.append(link)

    def dirs_are_fine(self):
        """Performs sanity checks on input directories. 

        :return: True if pass, False if fail.
        
        """
        if not (os.path.exists(self.in_diagram_path)
                and os.path.isdir(self.file_dir)
                and os.path.isdir(self.out_dir)):
            #print (self.in_diagram_path + " exists: "
            #       + str(os.path.exists(self.in_diagram_path)))
            #print (self.file_dir + " exists: "
            #       + str(os.path.isdir(self.file_dir)))
            #print (self.out_dir + " exists: "
            #       + str(os.path.isdir(self.out_dir)))
            return False
        return True

    def get_menu_width(self):
        """Estimates dropdown menu width from longest content.

        Calculation is 9 times number of characters.

        :return: string with estimated width in px
        """
        menu_items = self.menu_items.split(",")
        return str(9*len(max(menu_items, key=len)))


def build_module(args):
    """Process user inputs and build graphyte module.

    :param args: Input arguments list.
    :return: None
    """
    run_dir = os.path.dirname(os.path.realpath(__file__))

    usage = """
     Name:
     ----
       graphyte_gen.py - script to generate interactive HTML module from \
SVG/UML and text files.

     Usage:
     -----
       python3 C:\path\\to\graphyte_gen.py \
-i "input diagram file" \
-o "output directory" \
-M "model name" \
-V "model version" \
-m "module name" \
-d "linked files directory" \
[-w "work directory"] \
[-l "log file"] \
[-s "parameters worksheet"] \
[-n "navigation items"] \
[-t "web page title"] \
[-c "changes file"]

     Options:
     -------
       -i|--input     "input SVG/UML file":     Path to SVG or UML file used \
as diagram.
       -o|--output    "output dir":             Path to output directory.
       -M|--model     "global model name"       Global name of the model, \
common for all modules, e.g.: "L3VPN".
       -V|--version   "version":                Version of the model, e.g.: \
"1.0".
       -m|--module    "module name"             Name of the service \
module/component, e.g.: "Routing".
       -d|--filesdir  "linked files dir":       Path to directory containing \
all source text.
       -w|--workdir   "work dir":               Path to directory used by \
the tool to store in-flight, auxiliary files.
       -l|--logfile   "log file":               Path to log file.
       -s|--sheet     "input XLS file":         Parameters XLS file.
       -n|--nav       "navigation menu items":  Comma separated navigation \
menu items.
       -t|--title     "web page title":         Optional. Will show in the \
output web page.
       -c|--changes   "changes file":           Optional. Changes file.

    """

    in_diagram_path = ""
    out_dir = ""
    out_html_path = ""
    title = ""
    file_dir = ""
    menu_items = ""
    version = ""
    model = ""
    module = ""
    in_xls_path = ""
    work_dir = ""
    log_file = ""
    uml_no = ""
    changes_file = ""

    class MyParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            print (usage)
            sys.exit(2)

    parser = MyParser()
    parser.add_argument('-i', '--input', required=True,
                        help='Path to SVG/UML file.')
    parser.add_argument('-o', '--output', required=True,
                        help='Absolute path to output directory.')
    parser.add_argument('-M', '--model', required=True,
                        help='Global name of the model (i.e. name of '
                             'Service), common for all modules, e.g.: "L3VPN".')
    parser.add_argument('-V', '--version', required=True,
                        help='Version of the model, e.g.: "1.0".')
    parser.add_argument('-m', '--module', required=True,
                        help='Name of the model\'s module/component, '
                             'e.g.: "Routing".')
    parser.add_argument('-t', '--title', required=False,
                        help='Title that will show in the output web page.')
    parser.add_argument('-d', '--filesdir', required=True,
                        help='Path to directory containing all the files '
                             'linked form the web page.')
    parser.add_argument('-n', '--nav', required=False,
                        help='Comma separated list of navigation menu items.')
    parser.add_argument('-s', '--sheet', required=False,
                        help='Input XLS file.')
    parser.add_argument('-w', '--workdir', required=False,
                        help='Path to directory used by the tool to store '
                             'in-flight, auxiliary files.')
    parser.add_argument('-l', '--logfile', required=False,
                        help='Path to log file.')
    parser.add_argument('-u', '--uml-no', required=False, dest="umlno",
                        help='pyang --uml-no option.')
    parser.add_argument('-c', '--changes', required=False, dest="changes",
                        help='changes file.')
    args = parser.parse_args(args)



    # input diagram
    if args.input == '':
        sys.exit(usage)
    else:
        in_diagram_path = args.input.strip()
    # output directory
    if args.output == '':
        sys.exit(usage)
    else:
        out_dir = args.output.strip()
    # model
    if args.model == "":
        sys.exit(usage)
    else:
        model = args.model.strip()
    # version
    if args.version == '':
        sys.exit(usage)
    else:
        version = args.version.strip()
    # module
    if args.module == '':
        sys.exit(usage)
    else:
        module = args.module.strip()
    # title
    if args.title:
        title = args.title.strip()
    # files directory
    if args.filesdir == '':
        sys.exit(usage)
    else:
        file_dir = args.filesdir.strip()
    # navigation menu
    if args.nav:
        menu_items = args.nav
    # parameter worksheet
    if args.sheet:
        in_xls_path = args.sheet.strip()
    # work directory
    if args.workdir:
        work_dir = args.workdir.strip()
    # log file
    if args.logfile:
        log_file = args.logfile.strip()
    else:
        log_file = out_dir + "/graphyte.log"
    # pyang uml-no options
    if args.umlno:
        if not os.path.splitext(in_diagram_path)[1] == ".yang":
            # --uml-no option only valid for .yang diagram
            sys.exit(usage)
        else:
            uml_no = re.sub(r'\s+', '', args.umlno)
    else:
        pass
    # changes file
    if args.changes:
        changes_file = re.sub(r'\s+', '', args.changes)
    else:
        pass

    print ("\nRunning <{graphyte}> with arguments:\n\
              -i , Diagram file:      " + in_diagram_path + "\n\
              -o , Output directory:  " + out_dir + "\n\
              -M , Model name:        " + model + "\n\
              -V , Model version:     " + version + "\n\
              -m , Module name:       " + module + "\n\
              -t , Title:             " + title + "\n\
              -d , Files Dir:         " + file_dir + "\n\
              -s , Parameter sheet:   " + in_xls_path + "\n\
              -w , Work Dir:          " + work_dir + "\n\
              -l , Log file:          " + log_file + "\n\
              -n , Menu items:        " + menu_items + "\n\
              -u , pyang uml-no:      " + uml_no)


    # Initialize graphyte module object
    gm = GraphyteModule(
        model, module, version, title, out_dir, in_diagram_path, work_dir,
        run_dir, file_dir, in_xls_path, menu_items, uml_no, changes_file
    )

    # Sanity checks for dirs
    if not gm.dirs_are_fine:
        sys.exit(usage)

    # target string to be added to the html
    xls_to_script = ""

    # list of allowed parameters (extracted from input xls)
    # allowed_parameters = []

    # process authorized parameter list
    if in_xls_path:
        xls_to_script = process_param_sheet(gm)

    # if diagram is yang, convert to uml
    if gm.diagram_is_yang():
        logger.info('         Processing YANG file...' + '\r\n')
        success = yang_2_uml(gm)
        if success:
            logger.info('         ...ok' + '\r\n')
        else:
            logger.info('         ...failed' + '\r\n')
            print ("\n...aborted.")
            return False

    # if diagram is uml, convert to svg
    module_diagram = dict()
    if gm.diagram_is_uml():
        module_diagram = uml_2_svg(gm)
    else:
        # diagram was already SVG
        gm.svg_path = gm.in_diagram_path

    # process svg diagram
    processed_svg = process_svg(gm)

    # if work_dir was not user specified, clean up work_dir after svg creation
    if gm.diagram_is_uml() and not gm.input_work_dir:
        shutil.rmtree(os.path.join(out_dir, "work"))

    # process templates and detect parameters
    file_script,module_templates = add_templates_to_script(gm)

    # add detected parameters
    file_script = add_params_to_script(gm, file_script)

    # create navigation menu
    build_menu(gm)

    # create html file
    build_html(gm, processed_svg, file_script, xls_to_script)

    # merge return dictionary with all used files
    module_files = {**module_diagram,**module_templates}

    print ("\n...done.")
    return True,module_files

    # remove comment below to display module on browser after creation
    # webbrowser.open(out_html_path, new=0, autoraise=True)

    exit(0)


if __name__ == "__main__":
    # run when not called via 'import'
    import sys
    build_module(sys.argv[1:])
