# Introduction
zbxtool is a set of python command line utilities for zabbix administration

# Tools directories
admtool : contains a set of tools for zabbix administration

excel_tool : excel worksheet for zabbix Hosts massive definitions update


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

6/ configure config.ini files in tools directories

    replace variables with the selected values in admtool and migtool directory
    
8/ execute the utilities
    
    only from zbxtool directory  
    python <tool directory>/<selected tool.py> --help

 
