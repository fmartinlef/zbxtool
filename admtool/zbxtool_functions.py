
'''  coding: utf-8
implements global functions for zbxtool utilities


Author : Francois Martin-Lefevre : fml@axynergie.com


'''

import configparser
import logging
import os
import difflib
import xml.dom.minidom
import re
import json
import jsondiff
from shutil import copyfile

from  pyzabbix.api import ZabbixAPI, ZabbixAPIException

class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        return os.path.expandvars(value)


def str_to_bool(s):
     ''' convert a string to corresponding boolean value
          "true", "vrai", "1" : True
          "false", "faux", "0" : False
     note : string is lowercase converted before comparison
     '''
     if s.lower() in ["true", "vrai", "1"]:
          return True
     elif s.lower() in ["false", "faux", "0"]:
          return False
     else:
          return s

def bool_to_str(b):
     ''' convert a boolean to corresponding string
     '''
     if b:
          return "True"
     else:
          return "False"

def parse_config(args, module):
     ''' parse configuration file
     '''
     config = configparser.ConfigParser(allow_no_value=True,interpolation=EnvInterpolation())

     config.read(args.config)

     return(config)

def init_log(config, mode_verbose):
     ''' init log record
     '''
     log_level = config["default"]["log_level"]

     log_format='%(asctime)-15s - %(levelname)s - %(module)s.py - %(funcName)s() - %(message)s'
     logging.basicConfig(format=log_format, level=log_level)

     logging.info("program started")
     logging.info("mode verbose = %s " % bool_to_str(mode_verbose))
     logging.info("log_level = %s" % log_level)
    
     return

def zbx_connect(config, env):
     ''' connect to zabbix API
     '''
     mode_verbose = config["default"]["mode_verbose"]

     zbx_url = config[env]["zbx_url"]
     if mode_verbose:
          logging.info("zabbix URL = %s" % zbx_url)
     zbx_usr = config[env]["zbx_usr"]
     zbx_pwd = config[env]["zbx_pwd"]

     zapi = ZabbixAPI(url=zbx_url,user=zbx_usr,password=zbx_pwd)

     if mode_verbose:
         logging.info("connection zabbix API version = %s " % zapi.api_version())

     return zapi


def cmp_file(fn1, fn2, ft):
     ''' file comparison
          implements different techniques depending of file type
          if ft = "xml" <date> export tag excluded
          if ft = "json" date index not compared
          if ft = "doc" no exclusion
     '''

     if ft == "json":
          with open(fn1, 'r') as json_fn1:
               json1 = json.load(json_fn1)
          with open(fn2, 'r') as json_fn2:
               json2 = json.load(json_fn2)

          json1["zabbix_export"]["date"]= ""
          json2["zabbix_export"]["date"]= ""
          if  jsondiff.diff(json1, json2):
               return False
          else:
               return True
     else:
          with open(fn1, 'r') as hosts0:
               with open(fn2, 'r') as hosts1:
                    diff = difflib.unified_diff(
                         hosts0.readlines(),
                         hosts1.readlines(),
                         fromfile='hosts0',
                         tofile='hosts1',
                         n=0,
                    )
                    for line in diff:
                         if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
                              continue
                         elif ft == "xml" and "<date>" in line and "</date>" in line:
                              continue
                         else:
                              # print("difference" + line)
                              return False
               return True
     


def copy_file(fdir, fn1, fn2, ft):
     ''' copy_file utility
               create fdir if not exist
               check differences between fn1 and fn2
               replace fn1 with fn2 if different
     '''

     if not os.path.exists(fdir):
          os.makedirs(fdir)

     if os.path.exists(fn2) and cmp_file(fn1, fn2, ft):
          return  "passed"
     else: 
          copyfile(fn1, fn2)
          return "saved"

def fmt_str_trig_expr(txt):
     ''' format trigger expression
          1: replace template reference by text
          2: add a note with template value at bottom
          test your regex at : http://www.pyregex.com/
     '''
     exprs = re.findall("[\{]([^#$:]+):*", txt)
     exprs_lst = []
     expr_no = 0


     for expr in exprs:
          if expr not in exprs_lst:
               exprs_lst.append(expr)
               expr_no += 1
               txt = txt.replace(expr, "<b>T" + str(expr_no) + "</b>")
               if expr_no == 1:
                    txt = txt + "<br>"
               txt = txt + "<br><b>T" + str(expr_no) + "</b> : " + expr 
     
     # print(exprs, "Num =", expr_no )          

     return txt

def fmt_url_str(txt):
     ''' look and format url string in html format  
          input : txt
          output : txt formated with html <a> tag 
     ''' 
     urls = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", txt) 

     for url in urls:
          if url:
               # print(url)
               txt = txt.replace(url, "<a href='" + url + "'>" + url + "</a>")
               
     return txt

def zbx_table(type):
     ''' Initialize zabbix value tables
     '''

     param = ""
     if type == "init":
          param = {
               "type":
                    {"0":"Zabbix agent",
                    "1":"SNMPv1 agent",
                    "2":"Zabbix trapper",
                    "3":"simple check",
                    "4":"SNMPv2 agent",
                    "5":"Zabbix internal",
                    "6":"SNMPv3 agent",
                    "7":"Zabbix agent (active)",
                    "8":"Zabbix aggregate",
                    "9":"web item",
                    "10":"external check",
                    "11":"database monitor",
                    "12":"IPMI agent",
                    "13":"SSH agent",
                    "14":"TELNET agent",
                    "15":"calculated",
                    "16":"JMX agent",
                    "17":"SNMP trap",
                    "18":"Dependent item",
                    "19":"HTTP agent",
                    },
               "status":
                    {"0":"actif","1":"inactif"},
               "available":
                    {"0":"inconnu","1":"disponible","2":"indisponible"},
               "flags":
                    {"0":"","4":"autodecouverte"},
               "inventory_mode":
                    {"-1":"inactif","0":"manuel","0":"automatique"},
               "ipmi_available":
                    {"0":"inconnu","1":"disponible","2":"indisponible"},
               "jmx_available":
                    {"0":"inconnu","1":"disponible","2":"indisponible"},
               "snmp_available":
                    {"0":"inconnu","1":"disponible","2":"indisponible"},
               "maintenance_status":
                    {"0":"","1":"en maintenance"},
               "priority":
                    {"0": "not classified",
                    "1": "information",
                    "2": "warning",
                    "3": "average",
                    "4": "high",
                    "5": "disaster"}  
          }
     elif type == "macros":
          param = [{"macro": ["user", "usr", "pass", "password", "pwd", "snmp"], "restrict": ["value"]}]
     

     return param



