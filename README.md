# Introduction
zbxtool is a set of python command line utilities for zabbix administration

The utilities scripts are localized in utils subdirectory

# Tools description 
## Order of calling parameters
The calling parameters order are

1- option in command line (-- parameter in command line) 

2- option in config file

3- default option (appear whith --help option))


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

# Installation for developement
Prerequesites : - python 3.7 +


## zbxtool installation and configuration
1/ if not exist create a project directory 
    
    mkdir projects
    cd projects

2/ git clone of project

    git clone https://github.com/fmartinlef/zbxtool.git
    cd zbxtool

3/ create the virtual environnement for development purpose

    python -m venv venv

4/ activate virtual environment

    venv\Scripts\activate.bat -> windows
    source venv/bin/activate -> linux ou macos

5/ python modules pre requisites

    pip install -r requirements.txt

6/ access of utils directory

    cd utils

7/ adapt config.ini for use
    replace variables with the corresponding values
    
        zbx_url = <zabbix url>
        zbx_usr = <zabbix usr>
        zbx_pwd = <zabbix pwd>

8/ execute the utilities

    python hosts_config.py --help
    python templates_export.py --help

## example of use
1/ python hosts_config.py --zbxenv prod --limit 10

generate an excel file with first 10 hosts in zabbix production environnement
the generated file is in <zbxtool_dir>/<save_dir>/"zbxenv"/ directory

2/ python templates_export.py --grpname tpl --tplname Template --verbose true

export and document templates which name contains "Template" and pertains in hostgroup "tpl*".
the generated files are in <zbxtool_dir>/<save_dir>/"zbxenv"/"hostgroup" directories