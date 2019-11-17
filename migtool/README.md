# migtool : tools for zabbix migration
Purpose of tools is facilitate migration from other monitoring solutions. The steps of a migration process are :

- export monitoring stuff from the primary solution 

- extract and transform the monitoring stuff in zabbix equivalent 

- generate and import zabbix monitoring configuration (templates)

- load zabbix definitions (host and hostgroups)

## export monitoring definition
The tool and steps utilised for producing external export files are specific for each monitoring solution : xml file, a plain text file, or csv file.

They are located in export subdirectory

## extract and transform monitoring stuff
Extract from the original export file the monitoring configuration elements which can be utilized for zabbix configuration. 

The resulting output is an excel file. The excel file format is independant from the source file or zabbix destination configuration. 

## generate zabbix monitoring configuration
Generate and import zabbix configuration : templates, items, triggers, graphs, screen, etc ... 

## load zabbix host configuration
Load zabbix host and hostgroup and attach the hosts to the corresponding templates.

