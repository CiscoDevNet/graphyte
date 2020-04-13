# imports
import logging
import getpass
from conflux import Conflux
import pprint
import os
import datetime


# info
__author__ = "Jorge Somavilla"

# initialize logger
logger = logging.getLogger('graphyte')

def build_confluence_page(d, c, p, s):
    """Create content structure in Confluence
    as a page tree for all Graphyte modules, under
    existing parent page. Optionally run user-provided
    post-script to perform additional actions.
    :param d: model dictionary
    :param p: parent page URL
    :param s: post script to execute
    :return: boolean result
    """
    usr = getpass.getuser()
    pwd = getpass.getpass(prompt='Password (' + usr + '): ', stream=None)
    conflux = Conflux(
        url=c,
        username=usr,
        password=pwd,
        timeout=1000)

    # retrieve confluence ID of parent page
    parent_id = conflux.get_page_id(p)

    # get title for page
    title = next(iter(d))

    #create new page under parent
    print("creating main page")
    page_id = conflux.create_empty_page_get_id(title, parent_id)
    # add model files to page
    zip_file = d[title]["zipfile"]
    print("attaching zip")
    conflux.attach_file_get_id(zip_file, page_id, 'application/zip')
    href = conflux.build_attachchment_href(
        page_id,
        os.path.basename(zip_file),
        "Full interactive documentation attached."
    )
    del d[title]['zipfile']
    conflux.append_header_to_page(page_id, "Full Model Documentation", "1")
    conflux.append_body_to_page(page_id, href)
    conflux.append_header_to_page(page_id, "Modules", "1")
    conflux.append_children_macro(page_id)

    # todo: add model sources to page

    # add changes file
    conflux.append_header_to_page(page_id, "CHANGES", "1")
    body = conflux.build_template_body("/Users/jsomavil/projects/TdE_R3/BF1/doc_repo/BF1DOC/Multicast IPTV/CHANGES")
    conflux.append_body_to_page(page_id, body)

    # add variables table and upload as attachment
    if 'auth_params' in d[title]:
        print("creating variables page")
        dtu = datetime.datetime.now()
        sdt = dtu.strftime("(%Y-%m-%d@%H:%M:%S)")
        child_id = conflux.create_empty_page_get_id("Variable List " + sdt, page_id)
        conflux.append_header_to_page(child_id, "Allowed Model Variables", "1")
        params_workbook = d[title]['auth_params']
        print("creating variables table")
        conflux.append_workbook_as_tables(child_id,params_workbook)
        if os.path.splitext(params_workbook)[1] == '.xlsx':
            ct = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        else:
            ct = "application/vnd.ms-excel"
        conflux.attach_file_get_id(params_workbook, page_id, ct)
        del d[title]['auth_params']

    # build child page for each module
    for m in d[title]:
        print("creating module page (%s)" % (m))
        m_noext = os.path.splitext(m)[0]
        dtu = datetime.datetime.now()
        sdt = dtu.strftime("(%Y-%m-%d@%H:%M:%S)")
        child_id = conflux.create_empty_page_get_id(m_noext + " " + sdt, page_id)
        # add toc with title
        toc = conflux.build_scroll_ignore(
            conflux.build_toc_with_header("Table of Contents")
        )
        conflux.append_body_to_page(child_id, toc)
        conflux.append_header_to_page(child_id, m, "1")
        conflux.append_header_to_page(child_id, "Diagram", "2")
        print("  adding diagram")
        if 'modsvgpath' in d[title][m]:
            svg_name = next(iter(d[title][m]['modsvgpath']))
            conflux.attach_svg_append_as_img(
                child_id,
                d[title][m]['modsvgpath'][svg_name]
            )
        else:
            conflux.attach_svg_append_as_img(child_id, d[title][m]['modpath'])
        if d[title][m]["templates"]:
            conflux.append_header_to_page(child_id, "Module Templates", "2")
            for t in d[title][m]["templates"]:
                print("  adding template %s " %(t))
                if os.path.splitext(t)[1] == ".csv":
                    fp = d[title][m]["templates"][t]
                    conflux.append_csv_as_table(child_id, fp)
                else:
                    fp = d[title][m]["templates"][t]
                    id, name = conflux.attach_file_get_id(fp, page_id)
                    href = conflux.build_attachchment_href(page_id, name, name)
                    conflux.append_header_to_page(child_id, href, "3")
                    body = conflux.build_template_body(fp)
                    conflux.append_body_to_page(child_id, body)
    print ("done.")
    return True
