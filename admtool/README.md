
# admtool : tools for zabbix administration

## tool :: export_templates.py
    usage: export_templates.py [-h] [--config CONFIG] [--verbose VERBOSE]
                            [--tplname TPLNAME] [--grpname GRPNAME]
                            [--zbxenv ZBXENV]

    zbxtools :: exports and documents the zabbix templates

    optional arguments:
    -h, --help         show this help message and exit
    --config CONFIG    config file path and name (default: config.ini)
    --verbose VERBOSE  mode verbose (default: false)
    --tplname TPLNAME  template name search option (default: Template)
    --grpname GRPNAME  template group name regex mask (default: Template)
    --zbxenv ZBXENV    config file zabbix environment section

1/ export the templates list in json or html format in subdirectories (hostgroup named) 

2/ document the template in html format in /doc subdirectory
 

## tool :: hosts_config.py
    usage: hosts_config.py [-h] [--config CONFIG] [--verbose VERBOSE]
                        [--zbxenv ZBXENV] [--xlfile XLFILE] [--limit LIMIT]

    zbxtools :: statistics of hosts configuration loading

    optional arguments:
    -h, --help         show this help message and exit
    --config CONFIG    config file path and name (default: config.ini)
    --verbose VERBOSE  mode verbose (default: false)
    --zbxenv ZBXENV    config file zabbix environment section
    --xlfile XLFILE    name of excel output file
    --limit LIMIT      for test purpose, limits the number of host scanned

Create an excel file with 4 sheets
« Hosts » sheet : inventory of all hosts 
- hosts attributes -> excel columns name are prefixed by "ho_"
- List of all affected users macros -> columns are prefixed by "ma_" 
- List of all affected host tags values  -> columns are prefixed by "ta_"
- List of all affected inventory values -> columns are prefixed by "in_"

« Groups » sheet : xref list of all host + associated hostgroups 

« Templates » : xref list of all host + associated templates 

« STATS » sheet : pivot table simples for host count in several columns 


## Order of calling parameters
The calling parameters order are

1- option in command line (-- parameter in command line) 

2- option in config file

3- default option (appear whith --help option))


### example of use
1/ python hosts_config.py --zbxenv prod --limit 10

generate an excel file with first 10 hosts in zabbix production environnement
the generated file is in <zbxtool_dir>/<save_dir>/"zbxenv"/ directory

2/ python templates_export.py --grpname tpl --tplname Template --verbose true

export and document templates which name contains "Template" and pertains in hostgroup "tpl*".
the generated files are in <zbxtool_dir>/<save_dir>/"zbxenv"/"hostgroup" directories