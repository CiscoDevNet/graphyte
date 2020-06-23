#!/usr/bin/env python3
"""html_utils.py

Tools to assist with graphyte HTML creation and other XML-related tasks.

"""

# imports
import logging
import os
import re
from subprocess import Popen, PIPE
from tempfile import mkstemp
from os import fdopen
from shutil import move, copy
import pprint
# import webbrowser

# info
__author__ = "Jorge Somavilla"

# initialize logger
logger = logging.getLogger('graphyte')

pp = pprint.PrettyPrinter(indent=4)

def yang_2_uml(gm):
    """Convert YANG module into UML format and store in
    graphyte module object (in_diagram_path attribute).

    :param gm: the graphyte module object
    :return: boolean result
    """
    yang_fname = os.path.basename(gm.in_diagram_path)
    work_yang_path = gm.work_dir + "/" + gm.in_diagram_name
    yang_fname_no_ext = os.path.splitext(yang_fname)[0]
    work_uml_path = gm.work_dir + "/" + yang_fname_no_ext + ".uml"
    copy(gm.in_diagram_path,work_yang_path)
    uml_no_option = "--uml-no=" + gm.pyang_uml_no
    #print ("\npyang --ignore-errors " + uml_no_option + " -f uml " + work_yang_path + " -o " + work_uml_path)
    p1 = Popen(["pyang", "--ignore-errors", uml_no_option, "-f", "uml", work_yang_path,
                "-o", work_uml_path], cwd=gm.run_dir, stdout=PIPE, stderr=PIPE)
    p1.communicate()  # wait for pyang execution
    result = False
    if p1.returncode == 0:
        if os.path.exists(work_uml_path):
            logger.info('         Successfully converted YANG to UML.' + '\r\n')
            result = True
        else:
            logger.info('         Failed to convert YANG to UML. Is pyang installed?' + '\r\n')
            result = True
    else:
        logger.error('              Couldn´t convert YANG to UML. Check ' + yang_fname + ' syntax?\r\n')
        result = False
        return result
    # remove pyang-generated title and footer
    remove_patterns = ['center footer', ' <size:20> UML Generated :', ' endfooter', 'Title ' + yang_fname_no_ext]
    tmp_fh, tmp_uml_path = mkstemp()  # temp file
    with fdopen(tmp_fh, 'w') as new_uml:
        with open(work_uml_path) as old_uml:
            for line in old_uml:
                if not any(p in line for p in remove_patterns):
                    new_uml.write(line)
    if os.path.exists(work_uml_path):
        os.remove(work_uml_path)
    copy(tmp_uml_path, work_uml_path)
    # store as reference diagram
    gm.in_diagram_path = work_uml_path
    return result




def uml_2_svg(gm):
    """Convert UML diagram into SVG format and store in
    graphyte module object (svg_path attribute).

    :param gm: the graphyte module object
    :return: None
    """
    # For pyang generated UML files:
    # Try to remove relative output path from UML file
    # '@startuml' line should be left without additional arguments
    logger.info('         Processing UML file...' + '\r\n')
    uml_fname = os.path.basename(gm.in_diagram_path)
    logger.info('             ' + uml_fname + '\r\n')
    tmp_fh, tmp_uml_path = mkstemp()  # temp file

    with fdopen(tmp_fh, 'w') as new_uml:
        with open(gm.in_diagram_path) as old_uml:
            for line in old_uml:
                new_uml.write(re.sub(r'@startuml.*', r'@startuml', line))
    work_uml_path = gm.work_dir + "/" + gm.in_diagram_name

    if os.path.exists(work_uml_path):
        os.remove(work_uml_path)
    copy(tmp_uml_path, work_uml_path)
    plantuml_out_file = gm.work_dir + "/" + os.path.splitext(gm.in_diagram_name)[0] + ".svg"

    # TODO: cath exception if plantuml not in place
    #print ("java -Xmx1024m -jar utils/plantuml.jar -v -tsvg " + work_uml_path + " -o " + gm.work_dir)
    p1 = Popen(["java","-Xmx1024m", "-jar", "utils/plantuml.jar", "-v", "-tsvg", work_uml_path,
                "-o", gm.work_dir], cwd=gm.run_dir, stdout=PIPE, stderr=PIPE)
    p1.communicate()  # wait for plantuml execution
    gm.svg_path = plantuml_out_file
    d = dict()
    d['modsvgpath'] = { os.path.basename(plantuml_out_file) : plantuml_out_file }
    #pp.pprint(d)
    logger.info('         ...done' + '\r\n')
    return d


def atag_2_gtag(svg_lines, i):
    """Figures out if <a tag should be replaced by <g tag
    in SVG link group, depending on link label used:

    <a ... xlink:href="mod:module.svg" -> do not replace by <g
    <a ... xlink:href="lit:http://cisco.com" -> do not replace by <g
    <a ... xlink:href="myfile.txt" -> replace by <g

    :param svg_lines: List of SVG lines
    :param i: current line
    :return: True if replace required, False otherwise.
    """
    while i < len(svg_lines):
        line = svg_lines[i]
        try:
            link = re.search('xlink:href="(.*?)"', line).group(1)
        except AttributeError:
            link = False
        if link:
            mod = re.search('mod:(.*)', link)
            lit = re.search('lit:(.*)', link)
            if mod:
                return False
            elif lit:
                return False
            else:
                return True
        i += 1
    return True


def guess_module(gm, name, fullname):
    """Finds the module linked with mod:module_name, looking into available
    modules in the model.

    If found, builds name of final html file for the module.

    If not found, issues a warning and ignores link.

    :param gm: the graphyte model
    :param name: the module specified by the user, stripped off extension,
    to be looked up among known modules.
    :param fullname: full link content as specified by the user.
    :return: "module" if name found, "fullname" if name not found.
    """
    if gm.menu_items:
        item_list = gm.menu_items.split(",")
        for item in item_list:
            item = item.strip()
            if name in item:
                item_no_sp = re.sub(r'\s+', r'_', item)
                module = gm.model_no_sp + "_" + item_no_sp + "_v" + gm.version + ".html"
                return module
    logger.warning('              Could not find linked module \"' + fullname + '\", ignoring.\r\n')
    return fullname


def process_svg(gm):
    """Process SVG so it can be embedded in HTML as
    supported by current web browsers.

    Plantuml, Draw.io, Visio specific sections are
    removed or modified to achieve browser support.

    :param gm: the graphyte module object
    :return: processed_svg, the processed SVG

    """

    # TODO: use xpath

    logger.info('         Processing SVG file...' + '\r\n')
    with open(gm.svg_path, 'r') as f:
        svg_fname = os.path.basename(gm.svg_path)
        logger.info('             ' + svg_fname + '\r\n')
        content = f.read()

        # plantuml svg
        if gm.diagram_is_uml():
            content = re.sub(r'\s+<(?!/text)', '<', content)
            content = re.sub(r'><', '>\n<', content)

        # draw.io svg
        is_drawio_file = False

        if "editor=&quot;www.draw.io&quot;" in content \
                or "host=&quot;www.draw.io&quot;" in content \
                or "host=&quot;scdp.cisco.com&quot" in content \
                or "host=&quot;app.diagrams.net&quot" in content \
                or re.search(r'<[^<>]+agent=[^>]+draw.io', content):
            is_drawio_file = True
            content = re.sub(r'width="(.*?)px" height="(.*?)px"'
                             , r'viewBox="0 0 \1 \2"', content)
            content = re.sub(r'><', '>\n<', content)

        processed_svg = ""
        a_tag = False
        svg_tag_level = 0
        svg_tag = False
        in_foreign_obj = False
        skip_line = False
        a_g_stack = []
        curr_tag = ""

        svg_lines = content.splitlines()
        i = 0
        while i < len(svg_lines):
            line = svg_lines[i]
            if re.match(r'^\s*<svg', line):
                svg_tag = True
                svg_tag_level += 1
                if svg_tag_level == 1:
                    line = re.sub(
                        r'<svg',
                        r'<svg id="svg" width="100%" preserveAspectRatio="xMinYMin slice"'
                        , line.rstrip()
                    )
            if svg_tag and svg_tag_level == 1:
                line = re.sub(r'id="(?!svg)"', r'', line.rstrip())
                line = re.sub(r'width="(?!%100)"', r'', line.rstrip())
                line = re.sub(r'height=".*?"', r'', line.rstrip())
                line = re.sub(
                    r'preserveAspectRatio="(?!xMinYMin slice)"'
                    , r'', line.rstrip())  # plantuml
                line = re.sub(r'style=".*?"', r'', line.rstrip())  # plantuml
            if re.match(r'^\s*<g', line):
                a_g_stack.append("g")
            if re.match(r'^\s*<a', line):
                a_tag = True
                if atag_2_gtag(svg_lines, i):
                    a_g_stack.append("g")
                    line = re.sub(r'<a', r'<g', line.rstrip())
                else:
                    a_g_stack.append("a")
            if a_tag:
                link = re.search('xlink:href="(.*?)"', line)
                if link:
                    link_str_old = link.group(1)
                    link_str_old_no_ext = os.path.splitext(link_str_old)[0]
                    mod = re.search('mod:(.*)', link_str_old_no_ext)
                    lit = re.search('lit:(.*)', link_str_old)
                    if mod:
                        link_str_new = guess_module(gm, mod.group(1), link_str_old)
                        line = line.replace(link_str_old, link_str_new)
                    elif lit:
                        link_str_new = lit.group(1)
                        line = line.replace(link_str_old, link_str_new)
                    else:
                        link_str_new = link_str_old.split("\\")[-1]
                        link_str_new = link_str_new.split("/")[-1]
                        gm.push_link(link_str_new)
                        line = line.replace(link_str_old, link_str_new)
                        line = re.sub(r'id=".*"', r'', line.rstrip())
                        line = re.sub(r'xlink:href="(.*?)"', r'class="wrapper" id="\1"', line.rstrip())
                        line = re.sub(r'xlink:actuate="onRequest"', r'', line.rstrip())  # plantuml
                        line = re.sub(r'xlink:show="new"', r'', line.rstrip())  # plantuml
                        line = re.sub(r'xlink:type="simple"', r'', line.rstrip())  # plantuml
            if re.match(r'.*>\s*$', line):
                svg_tag = False
                if a_tag:
                    a_tag = False
            if re.match(r'.*</(a|g)>.*$', line):
                if len(a_g_stack) > 0:
                    curr_tag = a_g_stack.pop()
                if curr_tag == "g":
                    line = re.sub(r'</a', r'</g', line.rstrip())
                curr_tag = ""
            if not is_drawio_file:
                if re.match(r'^\s*<foreignObject', line):
                    in_foreign_obj = True
                if re.match(r'^\s*</foreignObject>', line):
                    in_foreign_obj = False
                    line = ""
            if in_foreign_obj and not is_drawio_file:  # add here other conditions to skip line
                skip_line = True
            if not skip_line:
                processed_svg += (line.rstrip() + "\n")  # appends
            skip_line = False

            # increase loop index
            i += 1
    logger.info('         ...ok' + '\r\n')
    return processed_svg


def build_menu(gm):
    """Build navigation menu for final HTML module, which allows
    navigation between different modules in the graphyte model.

    Stores navigation menu on menu_tags attribute of graphyte module
    object.

    :param gm: the graphyte module object
    :return: None
    """
    logger.info('         Building navigation menu...' + '\r\n')
    if gm.menu_items:
        item_list = gm.menu_items.split(",")
        for item in item_list:
            item = item.strip()
            item_no_sp = re.sub(r'\s+', r'_', item)
            gm.menu_tags += "<li><a href=\"" + gm.model_no_sp \
                            + "_" + item_no_sp + "_v" + gm.version \
                            + ".html\">" + item + "</a></li>"
    else:
        gm.menu_tags += "<li><a href=\"" + gm.model_no_sp \
                        + "_" + gm.module_no_sp + "_v" + gm.version \
                        + ".html\">" + gm.module + "</a></li>"
    logger.info('         ...ok' + '\r\n')
    return


def build_html(gm, processed_svg, file_script, xls_to_script):
    """Assembles final HTML module.

    Uses pre-cooked mod_template and embeds module specific templates,
    parameter lists, navigation menu, SVG diagram, title and viewer initial
    content.

    :param gm: the graphyte module object
    :param processed_svg: the SVG diagram adapted for browser support
    :param file_script: templates and template parameter table
     in JS <script> array format
    :param xls_to_script: optional. Input table of authorized parameters
     in JS <script> array format
    :return: None
    """
    with open("utils/mod_template", "r") as template_file:
        blank_template = template_file.read()

    viewer_init_content = "<br>Click on a diagram element to display " \
                          "its contents on this viewer."
    if not gm.svg_links:
        viewer_init_content = ""

    logger.info('         Building HTML file...' + '\r\n')
    filled_template = str(
        blank_template.replace("%webTitle%", gm.title)
            .replace("%params_csv%", gm.out_html_name_no_ext
                     + "_parameters.csv")
            .replace("%svg%", processed_svg)
            .replace("%templates%", file_script)
            .replace("%menu%", gm.menu_tags))\
        .replace("%alert%", gm.invalid_param_found_alert)\
        .replace("%viewer_init_content%", viewer_init_content)\
        .replace("%xls%", xls_to_script)\
        .replace("%menuwidth%", gm.get_menu_width())\
        .replace("%changes_tab%", gm.changes_tab) \
        .replace("%changes_file%", gm.changes_fname)
    text_file = open(gm.out_html_path, "w")
    text_file.write(filled_template)
    text_file.close()
    logger.info('         ...ok' + '\r\n')
    return
