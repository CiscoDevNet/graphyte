#!/usr/bin/env python3
"""param.py

Tools for processing graphyte parameters.

"""

# imports
import logging
import os
import re
import xlrd
# import pprint

# info
__author__ = "Jorge Somavilla"

# initialize logger
logger = logging.getLogger('graphyte')


def process_param_sheet(gm):
    """Process authorized parameters worksheet.

    Extracts list of allowed parameters and stores in graphyte module
    object (gm) attribute.

    Returns table of parameters in JS <script> array format, to be
    embedded in output HTML module.

    :param gm: the graphyte module object
    :return: xls_to_script
    """
    logger.info('         Processing parameter worksheet...' + '\r\n')
    xls_to_script = ""
    allowed_parameters = []
    in_xls_fname = os.path.basename(gm.in_xls_path)
    module_logger = logging.getLogger('graphyte')
    module_logger.info('             ' + in_xls_fname + '\r\n')
    # book = open_workbook(in_xls_path)
    book = xlrd.open_workbook(
        filename=gm.in_xls_path,
        encoding_override="cp1252"
    )
    sheet = book.sheet_by_index(0)

    # read header values into the list
    # keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]
    # dict_list = []

    for row_index in range(1, sheet.nrows + 1):
        # create var title with value in row i, column 0 (param name)
        #  <>  : type 1
        # <{}> : type 2
        # <()> : type 3
        # <[]> : type 4
        var_title = ""
        if row_index == 1:
            # We are adding the headers:
            # var xls_headers = [
            # "Header 0",
            # "Header 1",
            # ...
            # "Header n-1"];
            var_title = "xls_headers"
        else:
            # We are adding a parameter:
            # var p_paramname = [
            # "Value col 0",
            # "Value col 1",
            # ...
            # "Value col n-1"];
            value_0 = sheet.cell(row_index - 1, 0).value
            value_0 = re.sub(r'(\\|\")', r'\\\1', value_0.rstrip())
            # value_0 = re.sub(r'-', r'\-', value_0.rstrip())
            value_0 = re.sub(r'-', r'_dash_', value_0.rstrip())
            value_0 = re.sub(r"[\$]", r'_dollarsign_', value_0.rstrip())
            value_0 = re.sub('[<>\(\)\{\}\[\]]', '', value_0.rstrip())
            value_0 = re.sub('\+', '_plus_', value_0.rstrip())
            value_0 = re.sub(' ', '_', value_0.rstrip())
            var_title = "p_" + value_0

        for col_index in range(sheet.ncols):
            value_j_orig = sheet.cell(row_index - 1, col_index).value
            value_j = value_j_orig
            # replace unicode U+00A0 : NO-BREAK SPACE [NBSP] by space
            try:
                value_j = value_j.replace(u"\u00A0", " ")
                value_j = value_j.replace(u"\u00ED", "")
            except:
                pass
            # value_j = value_j.encode('utf-8')
            value_j = str(value_j)
            # escape '\' and '"'
            value_j = re.sub(r'(\\|\")', r'\\\1', value_j.rstrip())
            value_j = re.sub(r'-', r'\-', value_j.rstrip())
            # replace newlines by spaces
            value_j = value_j.replace('\n', ' ').replace('\r', '')
            if col_index == 0:  # if j=0
                # if special characters in param name...
                if row_index > 1 and not param_name_is_valid(value_j,
                                                             value_j_orig):
                    # ...ignore row
                    break
                # add param name to list of allowed parameters
                allowed_parameters.append(
                    sheet.cell(row_index - 1, col_index).value.strip()
                )
                # remove invalid characters from var name
                var_title = re.sub(r'=', r'_equal_', var_title.rstrip())
                var_title = re.sub(r'\.', r'_dot_', var_title.rstrip())
                var_title = re.sub(r'\[', r'_openbracket_', var_title.rstrip())
                var_title = re.sub(r'\]', r'_closebracket_', var_title.rstrip())
                var_title = re.sub(r'\/', r'_backslash_', var_title.rstrip())
                var_title = re.sub(r'\'', r'_singlequote_', var_title.rstrip())
                # add variable name
                xls_to_script += "    var " + var_title + " = [\n\"" \
                                 + value_j.rstrip()
            else:
                # add line
                xls_to_script += "\",\n\"" + value_j.rstrip()
            # if last item close java array
            if col_index == sheet.ncols - 1:
                xls_to_script += "\"];\n\n"
    gm.allowed_parameters = allowed_parameters
    logger.info('         ...ok' + '\r\n')
    return xls_to_script


def param_name_is_valid(p, q):
    """Checks correct formatting of parameter name.

    Markup allowed: <> <{}> <[]> <()>
    Characters allowed: $,a-z,A-z,0-9,\-,_

    :param p: pre-processed parameter name for JS <script> compatibility
    :param q: original parameter name in template
    :return:
    """
    #if not (re.match(r'<[$,a-z,A-z,0-9,\-,_]+>', p)
    #        or re.match(r'<{[$,a-z,A-z,0-9,\-,_]+}>', p)
    #        or re.match(r'<\([$,a-z,A-z,0-9,\-,_]+\)>', p)
    #        or re.match(r'<\[[$,a-z,A-z,0-9,\-,_]+\]>', p)
    if not (re.match(r'<[$,a-z,A-z,0-9,\.,\[,\],\/,=,\',\-,_]+>', p)
            or re.match(r'<{[$,a-z,A-z,0-9,\.,\[,\],\/,=,\',\-,_]+}>', p)
            or re.match(r'<\([$,a-z,A-z,0-9,\.,\[,\],\/,=,\',\-,_]+\)>', p)
            or re.match(r'<\[[$,a-z,A-z,0-9,\.,\[,\],\/,=,\',\-,_]+\]>', p)
            ):
        logger.info('                 Skipping invalid name: ' + q + '\r\n')
        return False
    return True

#  ([$,a-z,A-Z,0-9,\.,\[,\],\/,=,',\-,_]+
#

def param_is_legal(p, gm):
    """Returns whether a given parameter is allowed (present in the
    variable list) or not.

    :param p: parameter under scrutiny
    :param gm: the graphyte module object
    :return: Boolean. True if found, False if not
    """
    return p in gm.allowed_parameters


def param_is_false_positive(p):
    """Returns whether a parameter-formatted string should be ignored
    and not regarded as such.

    :param p: parameter under scrutiny
    :return: Boolean. True if false positive, false if not.
    """
    # TODO: add input list of ignored parameters
    result = False

    # param cannot have spaces
    if " " in p:
        result = True

    # <*> is JUNOS valid CLI, not a parameter
    if p == "<*>":
        result = True

    # add other checks

    # return boolean
    return result


def add_params_to_script(gm, file_script):
    """Adds the table of parameters detected in templates, with
    optional validation results, in JS <script> array format,
    to file_script, to be embedded in the final HTML module.

    :param gm: the graphyte module object
    :param file_script: template files in JS <script> array format
    :return: file_script, with the appended variable list.
    """
    logger.info('         Building parameters list...' + '\r\n')
    gm.decision_param_list = sorted(
        set(gm.decision_param_list), key=lambda s: s.lower())
    gm.template_param_list = sorted(
        set(gm.template_param_list), key=lambda s: s.lower())
    params_csv = gm.out_html_name_no_ext + "_parameters"
    # spaces dots or hyphens -> underscores
    params_csv_ = re.sub(r'\s|-|\.', r'_', params_csv.rstrip())
    # equal sign ->
    params_csv_ = re.sub(r'=', r'_equal_', params_csv_.rstrip())
    #aqui: \.,\[,\],\/,=,\',
    params_csv_ = re.sub(r'\.', r'_dot_', params_csv_.rstrip())
    params_csv_ = re.sub(r'\[', r'_openbracket_', params_csv_.rstrip())
    params_csv_ = re.sub(r'\]', r'_closebracket_', params_csv_.rstrip())
    params_csv_ = re.sub(r'\/', r'_backslash_', params_csv_.rstrip())
    params_csv_ = re.sub(r'\'', r'_singlequote_', params_csv_.rstrip())



    file_script += "    var v_" + params_csv_ + "_csv" + " = [\n \"" + params_csv + "\.csv"
    if not gm.decision_param_list and not gm.template_param_list:
        file_script += "\",\n\"" + "No parameters found in module."
    else:
        if gm.in_xls_path:
            file_script += "\",\n\"" + "Module,Parameter,File,Validation,Data"
        else:
            file_script += "\",\n\"" + "Module,Parameter,File,Data"
    for p in gm.decision_param_list:
        p = re.sub(r'(\\|\")', r'\\\1', p)
        file_script += "\",\n\"" + gm.out_html_name_no_ext + "," + p.rstrip()
    for p in gm.template_param_list:
        p = re.sub(r'(\\|\")', r'\\\1', p)
        file_script += "\",\n\"" + gm.out_html_name_no_ext + "," + p.strip()
    file_script += "\"];\n\n"
    logger.info('         ...ok' + '\r\n')
    return file_script


