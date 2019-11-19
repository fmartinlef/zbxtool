'''  coding: utf-8
1/ read a spectrum xml definition file
2/ produce an external excel definition file

implemented rules for definitions export






Author : Francois Martin-Lefevre : fml@axynergie.com

'''

import sys
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PARENT_DIR)

import argparse

import xml.etree.ElementTree as ET

from collections import OrderedDict
from xmljson import BadgerFish
import json

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



def get_spectrum_topology(json, attr, d):
    ''' get spectrum topology

    '''
    result = []
    for key in json:
        tmp_result = []
        if isinstance(json[key], dict):
            tmp_result.append(json[key])
            get_spectrum_topology(json[key], attr ,d+1)
        elif isinstance(json[key], list):
            for it in json[key]:
                try:
                    tmp_result.append(d)
                    for l in attr[key]:
                        tmp_result.append(it[l])
                except KeyError:
                        tmp_result.append("")

    return result

def json_print(json, d):
    ''' print json with indentation

    '''
    indent = ""
    for i in range(d):
        indent = indent + "   "
    for key in json:
        if isinstance(json[key], dict):
            print(indent, key, type(json[key]))
            json_print(json[key],d+1)
        elif isinstance(json[key], list):
            print(indent, key, type(json[key]), " -> ", len(json[key]), " occurences")
            json_print(json[key][0],d+1)
        else:
            print(indent, key, type(json[key]))


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

    bf = BadgerFish(dict_type=OrderedDict, xml_fromstring=False) 

    # read xml structure
    with open(infile) as fd:
        text = fd.read()
        xml_json = bf.data(ET.fromstring(text))

    # test purpose : print json structure
    json_print(xml_json, 0)

    attr = {}
    attr.update({"Topology_Container": ["@name", "@model_type", "@model_handle" ]})
    attr.update({"Device": ["@name", "@network_address", "@model_type", "@model_handle" ]})
    topology = get_spectrum_topology(xml_json["SPECTRUM_Export"]["Topology"], attr, 0)

    # exploit topology information


    # dev_attr = ["name", "network_address", "model_type", "model_handle", "community_string"]
    # dev_title = ["name", "network_address", "model_type", "model_handle", "community_string"]
    # dev_data = get_spectrum_device(xml_tree, dev_attr)
 

    # create and process excel data 
    # wb = Workbook()
    # # create named style for excel statistics sheet formating
    # xl_create_named_style(wb)

    # ws_host = xl_create_ws(wb, "Hosts", dev_title, dev_data)


    # del wb["Sheet"]
    # wb.save(outfile)

    # ending program

    logging.info("program ended")