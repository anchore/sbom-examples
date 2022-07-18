#!/usr/bin/env python3

import json
import sys
import os
import re

try:
    results_dir = sys.argv[1]
    input_pname_regexp = sys.argv[2]
    input_pvers_regexp = sys.argv[3]
    pname_regexp = re.compile(input_pname_regexp)
    pvers_regexp = re.compile(input_pvers_regexp)    
except:
    print ("USAGE: {} <sbom_results_directory> <package_name_regexp> <package_version_regexp>".format(sys.argv[0]))
    print ("\n\tExample: {} ./results '.*log4j.*' '.*'\n".format(sys.argv[0]))
    sys.exit(1)

results = []

try:
    for image in os.listdir(results_dir):
        syftjson = "{}/{}/sbom/syftjson.json".format(results_dir, image)
        if os.path.exists(syftjson):
            with open (syftjson, 'r') as FH:
                sbom = json.loads(FH.read())
            for artifact in sbom.get('artifacts', {}):
                pname = artifact.get('name', "")
                pvers = artifact.get('version', "")
                if pname_regexp.findall(pname) and pvers_regexp.findall(pvers):
                    el = {
                        "image": image,
                        "resultsbom": syftjson,
                        "package": pname,
                        "version": pvers,
                    }
                    results.append(el)
    print (json.dumps(results, indent=4))
except Exception as err:
    raise err
    
sys.exit(0)
