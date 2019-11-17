# Introduction
zbxtool is a set of python command line utilities for zabbix administration

# Tools directories
admtool : contains a set of tools for zabbix administration

migtool : contains a set of tools for migrate monitoring solutions to zabbix solution

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

