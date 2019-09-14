#!/usr/bin/env python3
"""graphyte.py

Builds a graphyte model consisting on one or more modules. Each module
is implemented via a dedicated call to graphyte_gen.py build_module
function.

Takes as input the path to the directory containing model files, and
optionally an identifier for the model.

Generates the complete graphyte model consisting on one or several
interconnected HTML modules.

Error Codes:
    100: No configuration file \"graphyte.conf\" found.
    101: Bad graphyte.conf format.
    102: No "model" entry found on graphyte.conf file.
    103: No "version" entry found on graphyte.conf file.
    104: At least one .svg or .uml file is required.
    105: Bad diagram_order in graphyte.conf. Files were not found.
    106: File not found.
    107: pyang_uml_no option not valid

"""

# imports
import os
import argparse
import shutil
import logging
import zipfile
import configparser
# import pprint
try:
    from graphyte_gen import build_module
except ImportError:
    print ("Couldn't import graphyte_gen.py module.")
except:
    pass
import datetime

# info
__author__ = "Jorge Somavilla"

# mark start time
start_time = datetime.datetime.now()

uml_no_options = [
    "uses", "leafref", "identity", "identityref", "typedef",
    "annotation", "import", "circles", "stereotypes"
]

def make_zip(src_dir, dst_dir, id):
    """Compress model files into a ZIP file.

    :param src_dir: Directory containing graphyte model files
    :param dst_dir: Target directory for the compressed file
    :param id: Identifier of the graphyte transaction
    :return: None
    """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    zipobj = zipfile.ZipFile(os.path.join(dst_dir, "graphyte-"+id+'.zip'),
                             'w', zipfile.ZIP_DEFLATED)
    rootlen = len(src_dir)
    for base, dirs, files in os.walk(src_dir):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])


def main(args):
    """Generate graphyte model, consisting on one or several modules.

    Calls build_module function from graphyte_gen.py once per module.

    :param args: Directory containing input files. Optionally graphyte
    transaction identifier.
    :return:None
    """
    ############################################
    # Argument Parser                          #
    ############################################
    usage = "\nusage: graphyte.py -d|--dir input_files_directory"

    class MyParser(argparse.ArgumentParser):
        """Argument Parser class handles inputs.

        Returns the ArgumentParser object.

        Throws error if malformed arguments.

        """
        def error(self, message):
            """Error if malformed argument. Attach "usage" help.

            :param message: Error message
            :return: None
            """
            logger = logging.getLogger('graphyte')
            logger.error('error: %s\n' % message)
            sys.stderr.write('error: %s\n' % message)
            print (usage)
            sys.exit(2)

    parser = MyParser()
    parser.add_argument('-d', '--dir', required=True,
                        help='Directory containing input files.')
    parser.add_argument('-i', '--id', required=False,
                        help='Session identifier (for use on graphyte server only).')
    args = parser.parse_args()

    basedir = ""
    if args.dir == '':
        sys.exit(usage)
    else:
        basedir = args.dir.strip()
        if not os.path.exists(basedir):
            parser.error("Couldn't find directory: " + basedir)

    identifier = ""
    if args.id:
        identifier = args.id.strip()

    # Create relevant directories
    zip_dir = ""
    if identifier:
        id_dir = basedir + '/archive/' + identifier
        in_dir = id_dir + '/in/'
        out_dir = id_dir + '/out/'
        zip_dir = id_dir + '/zip/'
        work_dir = id_dir + '/work/'
    else:
        in_dir = basedir
        out_dir = basedir + '/www/'
        work_dir = '/tmp/graphyte/work/'

    # TODO: Directories sanity checks

    # create output directory if doesn't exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # empty work directory if exists
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    os.makedirs(work_dir)

    # Logging
    # - CRITICAL: logging.critical(' message\r\n')
    # - ERROR:    logging.error('    message\r\n')
    # - WARNING:  logging.warning('  message\r\n')
    # - INFO:     logging.info('     message\r\n')
    # - DEBUG:    logging.debug('    message\r\n')
    # - NOTSET:   logging.notset('   message\r\n')
    logger = logging.getLogger('graphyte')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(out_dir + "/graphyte.log", mode='w')
    fh.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)

    # graphyte.log header
    logger.info('###########################################################' + '\r\n')
    logger.info('                  Cisco <{graphyte}>' + '\r\n')
    logger.info('                webdoc automation tool' + '\r\n')
    logger.info('' + '\r\n')
    logger.info(' For support please send this file to graphyte at cisco.com' + '\r\n')
    logger.info('###########################################################' + '\r\n')
    if identifier:
        logger.info('     Job ID: ' + identifier + '\r\n')

    def die(message):
        """Stop execution and return an error code.

        :param message: the error code
        :return: None
        """
        logger.error(message)
        elapsed = datetime.datetime.now() - start_time
        logger.info("     Elapsed time {}s".format(elapsed))
        if identifier:
            make_zip(out_dir, zip_dir, identifier)
        print (message)
        sys.exit(1)

    # Build graphyte_gen calls
    #  1. Analyze input files
    #     1.1 Process graphyte.conf file
    #        1.1.1 Get main_title
    #        1.1.2 Get version
    #        1.1.3 Get param list
    #        1.1.4 Get diagram order
    #        1.1.5 Get diagram_ignore_list
    #        1.1.6 Get pyang_no_uml
    #  2. Input files sanity checks
    #     2.1 Check number of modules
    #     2.2 Check param sheet file
    #  3. Build calls and execute
    #     3.1 Build navigation menu
    #     3.2 Loop through modules
    #         3.2.1 build_module

    # 1.
    conf_file = ""
    mod_dict = dict()
    sheet = ""
    sheet_name = ""
    file_dict = dict()
    repeated_fnames = []
    for base, dirs, files in os.walk(in_dir):
        for file in files:
            fname = os.path.splitext(file)[0]
            fext = os.path.splitext(file)[1]
            fpath = os.path.join(base, file)
            if fname in file_dict:
                repeated_fnames.append(fpath)
            else:
                file_dict[file] = fpath
            if file == 'graphyte.conf':
                logger.info(
                    "     Processing configuration file graphyte.conf.\r\n"
                )
                conf_file = os.path.join(base, file)
            elif fext == '.svg' or fext == '.uml' or fext == '.yang':
                mod_dict[file] = fpath

    # 1.1
    if not conf_file:
        die(
            "    Error 100: No configuration file \"graphyte.conf\" found, aborting execution.\r\n"
        )

    conf_parser = configparser.RawConfigParser()
    try:
        conf_parser.read(conf_file)
    except Exception as e:
        die("    Error 101: Bad graphyte.conf format.")

    # 1.1.1
    model = ""
    try:
        model = conf_parser.get('main', 'model')
        logger.info("         model:          {}\r\n".format(model))
    except:
        die(
            "    Error 102: No \"model\" entry found on graphyte.conf file, aborting execution.\r\n"
        )

    # 1.1.2
    version = ""
    try:
        version = conf_parser.get('main', 'version')
        logger.info("         version:        {}\r\n".format(version))
    except:
        die(
            "    Error 103: No \"version\" entry found on graphyte.conf file, aborting execution.\r\n"
        )

    # 1.1.3
    param_ref = ""
    try:
        param_ref = conf_parser.get('parameters', 'auth_params')
        logger.info("         auth_params:    {}\r\n".format(param_ref))
    except:
        pass
    if param_ref:
        if param_ref in file_dict:
            sheet_name = param_ref
            sheet = file_dict[sheet_name]
        else:
            die("    Error 106: File \"{}\" not found.\r\n".format(param_ref))

    # 1.1.4
    diagram_order = ""
    try:
        diagram_order = conf_parser.get('layout', 'diagram_order')
        logger.info("         diagram_order:  {}\r\n".format(diagram_order))
    except:
        pass

    # 1.1.5
    diagram_ignore_list = list()
    try:
        s = conf_parser.get('layout', 'diagram_ignore_list')
        logger.info("         diagram_ignore_list:  {}\r\n".format(s))
        diagram_ignore_list = s.split(",")
    except:
        pass
    for d in diagram_ignore_list:
        logger.info("         removing {} from modules\r\n".format(d))
        mod_dict.pop(d.strip(), None)

    # 1.1.6
    uml_no = ""
    pyang_uml_no = ""

    first = True
    try:
        uml_no = conf_parser.get('layout', 'pyang_uml_no')
        logger.info("         pyang_uml_no:  {}\r\n".format(uml_no))
    except:
        pass
    if uml_no:
        for u in uml_no.split(","):
            if not u in uml_no_options:
                die("    Error 107: pyang_uml_no option \"{}\" not valid."
                    " Valid options are: uses, leafref, identity, identityref,"
                    " typedef, annotation, import, circles, stereotypes\r\n".format(param_ref))
            else:
                if first == False:
                    pyang_uml_no = pyang_uml_no + ","
                else:
                    first = False
                pyang_uml_no = pyang_uml_no + u
    else:
        pyang_uml_no = "annotation"

    # test mode
    test_mode = False
    try:
        test_mode = conf_parser.get('hidden', 'test_mode')
    except:
        pass

    # 2.
    if len(mod_dict) == 0:
        die(
            "    Error 104: At least one .svg, .uml or .yang file is required, aborting execution.\r\n"
        )
    if param_ref and not param_ref == sheet_name:
        logger.warning(
            ("  201: param_ref = \"{}\" not found among uploaded files, skipping parameter validation.\r\n")
            .format(param_ref)
        )
    sheet_option = []
    if sheet:
        sheet_option.append('-s')
        sheet_option.append(sheet)

    # TODO: if any elements in repeated_fnames[] list,
    # issue warning to logfile, continue

    # 3.
    # 3.1
    nav_menu = ""
    count = 0
    error_items = []
    if diagram_order:
        diagram_order_list = [x.strip() for x in diagram_order.split(',') if x != '']
        for d in diagram_order_list:
            if d in mod_dict:
                if not count == 0:
                    nav_menu += ','
                nav_menu += str(os.path.splitext(d)[0])
                count += 1
            else:
                error_items.append(d)
        if error_items:
            die(
                "    Error 105: Bad diagram_order in graphyte.conf. The following files were not found: " + ', '
                .join(error_items) + "\r\n"
            )
        for g in mod_dict:
            if g not in diagram_order_list:
                nav_menu += ','
                nav_menu += str(os.path.splitext(g)[0])
    else:
        for d in mod_dict:
            if not count == 0:
                nav_menu += ','
            nav_menu += str(os.path.splitext(d)[0])
            count += 1

    # 3.2
    num_modules = 0
    for module, mod_path in mod_dict.items():
        # 3.2.1
        sheet_option_cmd = ""
        if len(sheet_option) > 1:
            sheet_option_cmd = sheet_option[0] + " \"" + sheet_option[1] + "\""
        else:
            sheet_option_cmd = ""
        uml_no_option_cmd = ""
        pyang_uml_no_option = []
        if os.path.splitext(mod_path)[1] == ".yang":
            uml_no_option_cmd = "--uml-no " + pyang_uml_no
            pyang_uml_no_option.append('-u')
            pyang_uml_no_option.append(pyang_uml_no)
        logger.info("     Processing module {}\r\n".format(module))
        command = "\n\n------------------------------------------------------------------------------\n\n" \
                  "python3 graphyte_gen.py -i \"{}\" -o \"{}\" -M \"{}\" -V \"{}\" -m \"{}\" -d \"{}\" -n \"{}\" -w \"{}\" {} {}"\
            .format(mod_path, out_dir, model, version, os.path.splitext(module)[0], in_dir, nav_menu, work_dir, sheet_option_cmd, uml_no_option_cmd)
        result = ""
        if test_mode:
            logger.info("     {}\r\n".format(command))
        try:
            print(command)
            # os.system(command)
            module_2 = os.path.splitext(module)[0]
            result = build_module(
                ['-i', mod_path, '-o', out_dir, '-M', model, '-V', version,
                 '-m', module_2, '-d', in_dir, '-n', nav_menu, '-w',
                 work_dir]+sheet_option+pyang_uml_no_option
            )
        except:
            pass
        if result:
            logger.info("     Completed module {}\r\n".format(module))
        else:
            logger.info("     Aborting module {}\r\n".format(module))
        num_modules += 1

    if identifier:
        command2 = "echo \"{}\n    {} {} - {} modules\" >> {}/jobs.log"\
            .format(identifier, model, version, num_modules, basedir)
        os.system(command2)

    # zip files
    if identifier:
        logger.info("     Generating .zip\r\n")
        elapsed = datetime.datetime.now() - start_time
        logger.info("     Elapsed time {}s".format(elapsed))
        make_zip(out_dir, zip_dir, identifier)
    else:
        elapsed = datetime.datetime.now() - start_time
        logger.info("     Elapsed time {}s".format(elapsed))

    exit(0)


if __name__ == "__main__":
    # run when not called via 'import'
    import sys
    main(sys.argv[1:])
