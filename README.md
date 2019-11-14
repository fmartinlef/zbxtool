# Introduction
zbxtool est un ensemble d'utilitaires python en ligne de commandes pour l'administration de la plate forme zabbix

Ils sont contenus dans le sous répertoire utils, les utilitaires se lancent depuis ce répertoire, pour y accéder depuis le répertoire zbxtool
    ''cd utils''


# Description des utilitaires 
## Prise en compte des paramètres d'appel
L'ordre de prise en compte des paramètres d'appel des différents scripts est le suivant

1- option passée en paramètre d'appel

2- option configurée dans le fichier de configuration

3- option configurée par défaut (celui qui figure dans l'appel de l'aide du script)


## utilitaire :: export_templates.py
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

1/ Exporte les templates en format xml et json
2/ génère une documentation HTML des templates déposée dans le sous répertoire /doc

## utilitaire :: hosts_config.py
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

Produit un fichier excel avec 4 feuilles
Feuille « Hosts » : inventaire de tous les hosts chargés dans l’environnement zabbix comprenant les champs suivants :
- Caractéristiques des hosts -> les colonnes sont préfixées par la chaîne « ho_ »: nom, description, statut d’ajout (si autodécouverte), état (actif ou inactif), …
- Liste de toutes les users macros -> les colonnes sont préfixées par la chaîne « ma_ »
- Liste de tous les tags affectés à un host -> les colonnes sont préfixées par la chaîne « ta_ »
- Liste de toutes les valeurs alimentées des données d’inventaire -> les colonnes sont préfixées par la chaîne « in_ »

Feuille « Groups » : liste des groupes auxquelles appartiennent les Hosts

Feuille « Templates » : liste des templates auxquels appartiennent les Hosts

Feuille « STATS » : tableaux croisés simples de colonnes choisies dans les feuilles hosts / groups et templates

# Installation environnement pour développement
## Installation environnement python -> sur votre poste de travail windows
Les utilitaires ont été développés avec la version 3.7 de python

si vous disposez des droits d'admin sur votre poste de travail
    https://www.python.org/downloads/release/python-375/

si vous ne disposez pas des droits d'admin sur votre poste de travail
    https://sourceforge.net/projects/portable-python/files/Portable%20Python%203.7/Portable%20Python-3.7.5%20x64.exe/download


Exécuter le fichier qui dizipera le répertoire que vous pourrez alors recopier dans le répertoire de votre choix

L'accès à une console configurée pour exécuter des scripts python s'effectue alors en exécutant le fichier
    Console-Launcher.exe

## Installation et configuration de zbxtool
1/ créer le répertoire projet
    
    mkdir zbxtool
    cd zbxtool

2/ copier le répertoire zbxtool (ou faire un git clone depuis le repo)

3/ créer l'environnement virtuel pour le développement

    python -m venv venv

4/ activer l'environnement virtuel

    venv\Scripts\activate.bat

5/ installer les modules python nécessaires aux utilitaires

    pip install -r requirements.txt

6/ accéder au répertoire d'exécution des utilitaires

    cd utils

7/ vérifier / paramétrer le fichier de configuration selon les besoins
    editer le fichier "config.ini"
    remplacer les variables par les valeurs correspondantes
        zbx_url = <zabbix url>
        zbx_usr = <zabbix usr>
        zbx_pwd = <zabbix pwd>

8/ lancer les utilitaires en ligne de commande

    python hosts_config.py --help
    python templates_export.py --help

9/ synchronisation avec repo bitbucket / github

    ... à mettre en place une fois le repo zbxtool créé ...

