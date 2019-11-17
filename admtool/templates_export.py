'''  coding: utf-8
Export templates utility : 
- in a choosed directory
- with template name mask
- with template group name mask

Author : Francois Martin-Lefevre : fml@axynergie.com

'''

import sys
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PARENT_DIR)

import argparse
import filecmp
import re
import tempfile
import xml.dom.minidom

from pyzabbix.api import ZabbixAPI, ZabbixAPIException
from jinja2 import Environment, FileSystemLoader, select_autoescape

from admtool.zbxtool_functions import parse_config, init_log, logging, copy_file, fmt_url_str, fmt_str_trig_expr, zbx_connect, zbx_table

 
def parse_arg():
    parser = argparse.ArgumentParser(add_help=True, description='zbxtools :: exports and documents the zabbix templates ')
    parser.add_argument("--config", type=str,
                        help="config file path and name (default: config.ini)", 
                        default="config.ini")
    parser.add_argument("--verbose", type=bool,
                        help="mode verbose (default: false)",
                        default=False)
    parser.add_argument("--tplname", type =str,
                        help="template name search option (default: Template)",
                        default='Template')
    parser.add_argument("--grpname", type=str,
                        help="template group name regex mask (default: Template)",
                        default='Template')
    parser.add_argument("--zbxenv", type=str,
                        help="config file zabbix environment section")

    args=parser.parse_args()

    return args

def export_tpl(zapi, te):
    ''' format export template output


    '''
    result = ""

    # generate xml file 
    xml_formated = zbx_exportXML(zapi, te)

    with open(tmp_xml, mode='w') as export_file:
        export_file.write(xml_formated)

    # generate json file
    json_formated = zbx_exportJSON(zapi, te)
    with open(tmp_json, mode='w') as export_file:
        export_file.write(json_formated)

    # save file
    hostgroups = zapi.hostgroup.get(output="extend", hostids=te["templateid"])
    for hg in hostgroups:
        if grpmask.search(hg["name"]):
            fdir = dir_data + hg["name"] + "/"
            fn2 = fdir + te["name"] + ".xml"
            fn3 = fdir + te["name"] + ".json"            
            result = copy_file(fdir, tmp_xml, fn2, "xml")
            logging.info("template '%s.xml' %s in '%s' group", te["name"], result, hg["name"])
            result = copy_file(fdir, tmp_json, fn3, "json")
            logging.info("template '%s.json' %s in '%s' group", te["name"], result, hg["name"])
        else:
            result = "nomatch"
            logging.info("template '%s' %s in '%s' group", te["name"], result, hg["name"])    


    return result

def zbx_tpl_fmtquery(resp, qry, sel, title, convert, notshown):
     ''' format the zbx tpl queries for table display
          - resp: response zabbix query
          - qry : query name
          - sel : list of columns value
          - title : list of converted title
          - convert: dictionnary for converted value
          - notshown: restricted list of keywoard how must not be shown

          return a dictionnary with 2 sections
          - title for the first table line
          - data for the data lines
     '''
     result = {}
     lst_title = {}
     lst_line = {}
     lst_data = []

     if len(resp) != 0:
          # populate title with conversion
          for se in sel:
               try:
                    lst_title.update({se: title[se]})
               except KeyError:
                    lst_title.update({se : se})
          result.update({"title":lst_title})
          # populate 
          # table with values
          for val in resp:
               lst_line={}
               # modif not shown value
               for se in sel:
                    # logging.info("type val= %s  type se= %s se = %s type val[se]= %s",type (val), type(se), str(se), type(val[se]))
                    if se == "tags":
                         break
                    tst_val = val[se].lower()
                    for ns in notshown:
                         try: 
                              for val_tst in ns[se]:
                                   if val_tst in tst_val:
                                        for re in ns["restrict"]:
                                             val[re] = "** Not Shown **"
                                             pass
                         except KeyError:
                              pass
               # replace converted value
               for se in sel:
                    se_str = val[se]
                    try:
                         se_str = convert[se][val[se]]
                    except KeyError:
                         se_str = val[se]
                    
                    if se in ["description", "comments", "url"]: 
                         se_str = fmt_url_str(se_str) 
                         se_str = se_str.replace("\n", "<br/>")

                    if se in ["expression"]:
                         se_str = fmt_str_trig_expr(se_str)

                    lst_line.update({se: se_str}) 
               lst_data.append(lst_line)
          result.update({"data":lst_data}) 

     return result


def zbx_render_html(tpl):
    jinja_templates = mod_path + "/jinja_templates"
    env = Environment(
            loader=FileSystemLoader(jinja_templates),
            autoescape=select_autoescape(['xml']),
            trim_blocks=True,
            lstrip_blocks=True)

    # template = env.get_template("tst.html")
    template = env.get_template("zbxtemplate.html")
    
    # print(tpl)

    doc_html = template.render(tpl=tpl)
    
    fname = dir_data + "template.html"

    with open(fname, 'w') as f:
        f.write(doc_html)
    f.closed

    fn = te["name"] + ".html"
    result = save_inhg(zapi,te,fname,fn)
    
    return result


def docum_tpl(zapi, te):
    result = {}
    global sel
    global desc

    # sel_template = ["host", "description"]
    # desc_template = ["Nom technique", "Description"]
    sel.update({"template": ["host", "description"]})
    desc.update({"template": ["Nom technique", "Description"]})
    result.update({"template": zbx_tpl_qry(zapi, te, "template")})

    sel.update({"hostgroup": ["name"]})
    desc.update({"hostgroup": ["Hostgroup(s)"]})
    result.update({"hostgroup": zbx_tpl_qry(zapi, te, "hostgroup")})

    sel.update({"macros": ["macro","value"]})
    desc.update({"macros": ["User macro", "Valeur"]})
    result.update({"macros": zbx_tpl_qry(zapi, te, "macros")})

    sel.update({"items": ["name", "key_", "type", "status", "delay", "history", "trends", "description", "url", "params", "snmp_oid"]})
    desc.update({"items": ["Nom Item", "Clef", "Type", "Etat", "Freq", "Detail", "Tendance", "Description", "URL de test", "params", "oid SNMP"]})
    result.update({"items": zbx_tpl_qry(zapi, te, "items")})

    sel.update({"triggers": ["comments", "description", "expression", "priority", "status", "url", "tags"]})
    desc.update({"triggers": ["Description", "Alerte", "Expression", "priorité", "Etat", "Consigne", "tags"]})
    result.update({"triggers": zbx_tpl_qry(zapi, te, "triggers")})

    sel.update({"drules": ["name", "key_", "type", "status", "delay", "description"]})
    desc.update({"drules": ["Nom", "Clef", "type", "Etat", "Freq", "Description"]})
    sel.update({"drule_items": ["name", "key_", "type", "status", "delay", "history", "trends", "description", "url", "params", "snmp_oid"]})
    desc.update({"drule_items": ["Nom Item", "Clef", "Type", "Etat", "Freq", "Detail", "Tendance", "Description", "URL de test", "params", "oid SNMP"]})
    sel.update({"drule_triggers": ["comments", "description", "expression", "priority", "status", "url", "tags"]})
    desc.update({"drule_triggers": ["Description", "Alerte", "Expression", "priorité", "Etat", "Consigne", "tags"]})
 
    result.update({"drules": zbx_tpl_qry(zapi, te, "drules")})
    
    sel.update({"graphs": ["name", "graphtype"]})
    desc.update({"graphs": ["Nom", "Type"]})
    result.update({"graphs": zbx_tpl_qry(zapi, te, "graphs")})

    sel.update({"webscenar": ["name", "delay", "status", "agent"]})
    desc.update({"webscenar": ["Nom", "Freq", "Etat", "Agent"]})
    sel.update({"webstep": ["name", "url", "status_codes", "required"]})
    desc.update({"webstep": ["Etape", "URL", "Html Status", "chaine testee"]})
    result.update({"webscenar": zbx_tpl_qry(zapi, te, "webscenar")})



    # print(result)

    return result


def zbx_exportXML(zapi, te):
     te_xml = zapi.configuration.export(format="xml",
                                        options={"templates": [te["templateid"]]}
                                        )
     dom = xml.dom.minidom.parseString(te_xml)
     te_xml_fmted = dom.toprettyxml()

     return te_xml_fmted

def zbx_exportJSON(zapi, te):
     te_json = zapi.configuration.export(format="json",
                                        options={"templates": [te["templateid"]]}
                                        )
     te_json_fmted = te_json

     return te_json_fmted

def zbx_tpl_qry(zapi, te, qry):
    ''' return a list containing the list of user macro
          - zapi : zabbix context
          - te : template id
          - qry : qry name (macros, items, triggers, drules ...))
          - sel : specified columns
          - desc : table title
          result_fmt = {title: [], data: []}
          * the values of specific list of reserved word are returned with "** not shown **"
    '''
    result = {}
    zbx_resp = ""
    global sel
    global desc

    if mode_verbose:
        logging.info("query template ID = %s / QRY = %s", te, qry)

    #  print("QRY : ", qry, "\nSEL:", sel, "\nDESC:", desc)
    title = dict(zip(sel[qry], desc[qry]))
    convert = zbx_table("init")
    notshown = zbx_table(qry)  

    if qry == "template":
        zbx_resp = zapi.do_request('template.get',{"output": sel[qry],
                             "templateids": te})['result']
    elif qry == "hostgroup":
        zbx_resp = zapi.do_request('hostgroup.get',{"output": sel[qry],
                             "hostids": te})['result']
    elif qry == "macros":
        zbx_resp = zapi.do_request('usermacro.get',{"output": sel[qry],
                             "hostids": te})['result']
    elif qry == "items":
        zbx_resp = zapi.do_request('item.get',{"output": sel[qry],   
                        "hostids": te})['result']
    elif qry == "drule_items":
        zbx_resp = zapi.do_request('itemprototype.get',{"output": sel[qry],   
                        "discoveryids": te})['result']
    elif qry == "drule_triggers":
        zbx_resp = zapi.do_request('triggerprototype.get',{"output": sel[qry],   
                        "discoveryids": te,
                        "expandExpression": True,
                        "selectTags":"extend",
                        })['result']
    elif qry == "triggers":
        zbx_resp = zapi.do_request('trigger.get',
                        {"output": sel[qry],
                        "hostids": te,
                        "expandExpression": True,
                        "selectTags":"extend",
                        })['result']
    elif qry == "webscenar":
        result=[]
        lst_webscenar = zapi.do_request('httptest.get',
                        {"output": sel[qry],
                        "hostids": te,
                        "selectSteps": "extend",
                        "expandName": True,
                        "expandStepName": True
                        })['result']
        # print(lst_webscenar)
        for webscenar in lst_webscenar:
            res_webscenar = {}
            res_webscenar.update({"scenar": zbx_tpl_fmtquery([webscenar],qry,sel[qry], title,convert,notshown)})
            tit_webstep = dict(zip(sel["webstep"], desc["webstep"]))
            res_webscenar.update({"step": zbx_tpl_fmtquery(webscenar["steps"],qry,sel["webstep"], tit_webstep,convert,notshown)})
       
            result.append(res_webscenar)

        # print(result)
        return result

    elif qry == "drules":
        result = []
        lst_drules = zapi.do_request('discoveryrule.get',
                        {"output": "itemid",
                        "hostids": te,
                        })['result']
         # print("drules trouvees:", lst_drules)
        for drule in lst_drules:
            res_drule = {}
            zbx_drules = zapi.do_request('discoveryrule.get',
                             {"output": sel["drules"],
                             "itemids": drule["itemid"],
                             })['result']
            res_drule.update({"drule": zbx_tpl_fmtquery(zbx_drules, qry, sel[qry], title, convert, notshown)})
            res_drule.update({"items": zbx_tpl_qry(zapi, drule["itemid"], "drule_items")})
            res_drule.update({"triggers": zbx_tpl_qry(zapi, drule["itemid"], "drule_triggers")})
            result.append(res_drule)
              # print(result)
        return result

    elif qry == "graphs":
        result = []
        # lst_graphs = zapi.do_request('graph.get',
        #                  {"output": "itemid",
        #                  "hostids": te,
        #                  })['result']

    result=zbx_tpl_fmtquery(zbx_resp, qry, sel[qry], title, convert, notshown) 
       
    return result


def save_inhg(zapi, te, fn1, fn2):
    hostgroups = zapi.hostgroup.get(output="extend", hostids=te["templateid"])
    for hg in hostgroups:
        if grpmask.search(hg["name"]):
            fdir = dir_data + hg["name"] + "/doc/"
            to_file = fdir + fn2
            result = copy_file(fdir, fn1, to_file, "doc")
            logging.info("doc '%s.html' %s in '%s' group", te["name"], result, hg["name"])
        else:
            result = "nomatch"
            logging.info("doc '%s.html' %s in '%s' group", te["name"], result, hg["name"])
    return result


if __name__ == '__main__':

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

    tplmask_name = args.tplname or config[module]["tplname"] or "Template"
    if mode_verbose:
        logging.info("template name mask = " + tplmask_name)

    grpmask_name = args.grpname or config[module]["grpname"] or "Template"
    grpmask = re.compile(grpmask_name)
    if mode_verbose:
        logging.info("group template name mask = " + grpmask_name)

    zbxenv = args.zbxenv or config["default"]["env"] or "Zabbix"
    if mode_verbose:
        logging.info("environnement zabbix = " + zbxenv)


    # init global variable
    global sel
    sel = {}
    global desc
    desc = {}

    # start of program logic
    zbxtool_dir = config["paths"]["zbxtool_dir"]  
    dir_data = zbxtool_dir + "/"  + config[module]["save_dir"] + "/"  + zbxenv + "/"

    if not os.path.exists(dir_data):
        os.makedirs(dir_data)

    tmp_xml = tempfile.NamedTemporaryFile().name
    tmp_json = tempfile.NamedTemporaryFile().name


    logging.info("repertoire de templates = %s " % dir_data)

    zapi = zbx_connect(config,zbxenv)

    # template = zapi.template.get(output="extend")
    
    template = zapi.do_request('template.get',{"output": "extend",
                             "search": {"host": tplmask_name}})['result']

    for te in template:
        export_result = export_tpl(zapi, te)
        
        tpl_data = {}
        tpl_data=docum_tpl(zapi, te["templateid"])
        
        zbx_render_html(tpl_data)


    # ending program

    logging.info("program ended")