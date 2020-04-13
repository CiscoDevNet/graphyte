# imports
import logging
from getpass import getpass
from conflux import Conflux
import pprint
import os
import sys


log = logging.getLogger()
log.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
log.addHandler(stdout_handler)

pwd = getpass()
confluence = Conflux(
    url='https://scdp.cisco.com/conf',
    username='jsomavil',
    password=pwd)



#    url='https://scdp-dev.cisco.com/conf/',
#page_id = confluence.get_page_id("https://scdp-dev.cisco.com/conf/pages/viewpage.action?pageId=19728764")


# remove page and all children
#page_id = confluence.get_page_id("https://scdp.cisco.com/conf/pages/viewpage.action?pageId=59327497")
page_id = confluence.get_page_id("https://scdp.cisco.com/conf/display/TTD/Jorge+tests2")
confluence.remove_page(page_id)
exit(0)

# # append csv
# page_id = confluence.get_page_id("https://scdp.cisco.com/conf/display/TTD/Jorge+tests2")
# csv_file = "/Users/jsomavil/graphyte/repositories/github_devnet/graphyte/graphyte/utils/file.csv"
# confluence.append_csv_as_table(page_id, csv_file)
# exit(0)

# clean children
#confluence.remove_children_pages(confluence.get_page_id("https://scdp.cisco.com/conf/pages/viewpage.action?pageId=59327192"))
#exit(0)

#print page status
# page_id = confluence.get_page_id("https://scdp.cisco.com/conf/display/TTD/Jorge+tests2")
# status = confluence.get_page_by_id(
#     page_id=page_id,
#     expand='space,body.storage,version,container,_links.download,descendants'
#  #expand='space,version,container,_links.download,descendants.attachment'
# )
# confluence.pprint(status)
# exit(0)

#append workbook
#page_id = confluence.get_page_id("https://scdp.cisco.com/conf/display/TTD/Jorge+tests2")
#workbook = "Book2.xlsx"
#workbook = "/Users/jsomavil/graphyte/testbed/MBH_v0.7.1.1/MBH_allowed_parameters_v0.7.1.xlsx"
#confluence.append_workbook_as_tables(page_id, workbook)

# prepend header
#page_id = confluence.get_page_id("https://scdp.cisco.com/conf/display/TTD/Mobile+Backhaul+0.7.1+2020-03-15+20%3A46%3A13.394257")
#confluence.prepend_header_to_page(page_id, "Table of Contents", "1")

# get all attachments
#page_id = confluence.get_page_id("http://scdp.cisco.com/conf/display/TdE/Multicast+IPTV+v5")
#p1 = ".*\.txt"
#dir1 = "/Users/jsomavil/projects/TdE_R3/BF1/v5"
# p2 = ".*TMPLT2.*.txt"
# dir2 = "/Users/jsomavil/projects/TdE_R3/BF1/doc_repo/BF1DOC/200-299"
# p3 = ".*TMPLT3.*.txt"
# dir3 = "/Users/jsomavil/projects/TdE_R3/BF1/doc_repo/BF1DOC/300-399"
# p4 = ".*TMPLT4.*.txt"
# dir4 = "/Users/jsomavil/projects/TdE_R3/BF1/doc_repo/BF1DOC/400-499"
# p5 = ".*TMPLT5.*.txt"
# dir5 = "/Users/jsomavil/projects/TdE_R3/BF1/doc_repo/BF1DOC/500-599"
#confluence.download_all_attachments(page_id, dir1, p1)
# confluence.download_all_attachments(page_id, dir2, p2)
# confluence.download_all_attachments(page_id, dir3, p3)
# confluence.download_all_attachments(page_id, dir4, p4)
# confluence.download_all_attachments(page_id, dir5, p5)
# p = ".*.uml"
# dir = "/Users/jsomavil/projects/TdE_R3/BF1/doc_repo/BF1DOC/diagrams"
# confluence.download_all_attachments(page_id, dir, p)
# p = ".*.svg"
# dir = "/Users/jsomavil/projects/TdE_R3/BF1/doc_repo/BF1DOC/diagrams"
# confluence.download_all_attachments(page_id, dir, p)
