'''  coding: utf-8
1/ read a spectrum xml definition file
2/ produce an external excel definition file

Author : Francois Martin-Lefevre : fml@axynergie.com

'''

import sys
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PARENT_DIR)

import argparse

from xml.dom import minidom
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import NamedStyle, PatternFill, Font, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows

from admtool.zbxtool_functions import parse_config, init_log, logging
from admtool.hosts_config import xl_create_named_style, xl_create_ws

 
def parse_arg():
    parser = argparse.ArgumentParser(add_help=True, description='spectrum_extract :: extract spectrum definitions from xml export file')
    parser.add_argument("--config", type=str,
                        help="config file path and name (default: config.ini)", 
                        default="config.ini")
    parser.add_argument("--verbose", type=bool,
                        help="mode verbose (default: false)",
                        default=False)
    parser.add_argument("--infile", type=str,
                        help="name of input file from spectrum export utility")
    parser.add_argument("--xlfile", type=str,
                        help="name of excel output file")
    parser.add_argument("--limit", type=int,
                        help="for test purpose, limits the number of input definitions processed")

    args=parser.parse_args()

    return args

def get_spectrum_device(xml, attr):
    ''' get spetrum device list
        xml : xml dom object
        attr : list of device attributes 

        result is a list of devices attributes in attr list order
    '''
    spectrum_devices = spectrum_xml.getElementsByTagName('Device')

    verbose_msg = 100
    result = []
    for nb, dev in enumerate(spectrum_devices):
        tmp_result = []
        for at in attr:
            try:
                tmp_result.append(dev.attributes[at].value)
            except KeyError:
                tmp_result.append("")

        if mode_verbose and (nb % verbose_msg == 0) :
            logging.info("loop %s devices read", str(nb) )

        result.append(tmp_result)
        if nb > limit and limit !=0 :
            logging.info("device scan ended loop due to --limit parameter")
            break

    return result




if __name__ == '__main__':

    module = __file__[0:__file__.find(".")]

    ''' process args and config parameters for module variables setting
        1/ args parameter
        2/ config parameters
        3/ if config parameter not exist then args is the default
    '''

    module = __file__[__file__.find("/")+1:__file__.find(".")]
    mod_path = os.path.dirname(os.path.abspath(__file__))
    args = parse_arg()
    conf_file = mod_path + "/" + args.config
    config = parse_config(conf_file,module)

    mode_verbose = args.verbose or config.getboolean("default", "mode_verbose") or False
    init_log(config, mode_verbose)

    logging.info("program started")

    limit = args.limit or 0
    infile = args.xlfile or config[module]["infile"]

    xlfile = args.xlfile or config[module]["xlfile"] or "host.xlsx"

    zbxtool_dir = config["paths"]["zbxtool_dir"]  
    dir_data = zbxtool_dir + "/"  + config[module]["save_dir"] + "/"
    outfile = dir_data + xlfile

    logging.info("output file is : %s", outfile)

    if not os.path.exists(dir_data):
        os.makedirs(dir_data)

    if limit != 0:
        logging.info("input file limit activated %s definitions", str(limit))

    # check input file presency
   
    if not os.path.exists(infile):
        logging.error("input file %s not found", infile)
        sys.exit(8)

    # read xml structure
    spectrum_xml = minidom.parse(infile)

    dev_attr = ["name", "network_address", "model_type", "model_handle", "community_string"]
    dev_title = ["name", "network_address", "model_type", "model_handle", "community_string"]
    dev_data = get_spectrum_device(spectrum_xml, dev_attr)
 

    # create and process excel data 
    wb = Workbook()
    # create named style for excel statistics sheet formating
    xl_create_named_style(wb)

    ws_host = xl_create_ws(wb, "Hosts", dev_title, dev_data)


    del wb["Sheet"]
    wb.save(outfile)

    # ending program

    logging.info("program ended")