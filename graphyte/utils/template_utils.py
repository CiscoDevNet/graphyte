#!/usr/bin/env python3
"""template_utils.py

Tools to assist with graphyte template processing.

"""

# imports
import logging
import os
import re
from param_utils import param_is_false_positive, param_is_legal
import pprint

pp = pprint.PrettyPrinter(indent=4)

# info
__author__ = "Jorge Somavilla"

# initialize logger
logger = logging.getLogger('graphyte')


def add_templates_to_script(gm):
    """Transforms template text files into JS <script>
    arrays to be embedded in the final HTML module.
    Extracts parameters for validation while doing so.

    :param gm: the graphyte module object
    :return: file_script, templates in JS <script> array format.
    """

    logger.info('         Processing template files...' + '\r\n')
    file_script = ""
    mod_linked_templates = dict()
    #mod_linked_templates['templates'] = {}
    mod_linked_templates = {}
    for dirpath, dirs, src_files in os.walk(gm.file_dir):
        for src_file_name in src_files:
            # Check if file has been linked or is Changes file
            if src_file_name in gm.svg_links or src_file_name == gm.changes_fname:
                # Link to file has been found in the SVG or is Changes file, process it.
                logger.info('             ' + src_file_name + '\r\n')
                file_path = os.path.join(dirpath, src_file_name)
                if os.path.isfile(file_path):
                    file_name = os.path.splitext(src_file_name)[0]
                    #mod_linked_templates['templates'][src_file_name]=file_path
                    if not src_file_name == gm.changes_fname:
                        # do not add changesfile to module templates dict
                        mod_linked_templates[src_file_name] = file_path
                    # spaces dots or hyphens -> underscores
                    file_name = re.sub(r'\s|-|\.|\(|\)|\+', r'_',
                                       file_name.rstrip()
                                       )
                    file_ext = os.path.splitext(src_file_name)[1]
                    file_ext = re.sub(r'\.', r'_', file_ext.rstrip())
                    file_script += "    var v_" + file_name + file_ext \
                                   + " = [\n \"" + src_file_name
                    with open(file_path,
                              encoding="utf8",
                              errors='ignore') as f:
                        for line in f:
                            line = re.sub(r'(\\|\")', r'\\\1', line.rstrip())
                            line = re.sub(r'-', r'\-', line.rstrip())
                            line = re.sub(r'</script>', r'<\/script>', line.rstrip())
                            # line = line.decode('utf-8')
                            file_script += "\",\n\"" + line.rstrip()
                        file_script += "\"];\n\n"

                    # Find decision parameters
                    if file_ext == "_yang" or file_ext == "_xml" or src_file_name == gm.changes_fname:
                        # do nothing
                        continue
                    else:
                        if file_ext == "_csv":
                            with open(file_path,
                                      encoding="utf8",
                                      errors='ignore') as f:
                                for line in f:
                                    if not (line.strip() == ""):
                                        items = line.strip().split(",")
                                        # items.insert(1,src_file_name)
                                        newline = items[0] + "," \
                                            + src_file_name + ","
                                        if gm.in_xls_path:
                                            # define legality of parameter
                                            param_validation_result = ""
                                            # print "Legal?:" + items[0]
                                            if param_is_legal(items[0], gm):
                                                param_validation_result = "ok"
                                                # print "yes csv\n\n"
                                            else:
                                                param_validation_result \
                                                    = "unauthorized"
                                                # print "no csv\n\n"
                                                gm.invalid_param_found_alert \
                                                    = "(!)"
                                            newline += param_validation_result \
                                                       + ","
                                        for item in items[1:-1]:
                                            newline += item + " | "
                                        newline += items[-1]
                                        gm.decision_param_list.append(newline
                                                                      + "\n")
                        else: # txt + others
                        # Find template parameters
                        #if file_ext == "_txt":
                            with open(file_path,
                                      encoding="utf8",
                                      errors='ignore') as f:
                                for line in f:
                                    line.encode('utf-8').strip()
                                    matches = re.findall(r'(<.*?>)',
                                                         line, re.S)
                                    if matches:
                                        for paramfound in matches:
                                            if not param_is_false_positive(
                                                    paramfound
                                            ):
                                                if gm.in_xls_path:
                                                    param_validation_result = ""
                                                    if param_is_legal(
                                                            paramfound, gm
                                                    ):
                                                        param_validation_result\
                                                            = "ok"
                                                    else:
                                                        param_validation_result\
                                                            = "unauthorized"
                                                        gm.invalid_param_found_alert = "(!)"
                                                    gm.template_param_list.append(
                                                        paramfound + ","
                                                        + src_file_name + ","
                                                        + param_validation_result
                                                        + "," + re.sub(
                                                            r',', r''
                                                            , line.strip()))
                                                else:
                                                    gm.template_param_list.append(
                                                        paramfound + ","
                                                        + src_file_name
                                                        + "," + re.sub(r',',
                                                                       r'',
                                                                       line.strip()))
    logger.info('         ...ok' + '\r\n')
    mod_linked_templates2 = dict()
    mod_linked_templates2['templates'] = {}
    mod_linked_templates2['templates'] = mod_linked_templates
    return file_script,mod_linked_templates2
