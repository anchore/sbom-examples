#!/usr/bin/env python3

import json
import sys
import os
import re

try:
    results_dir = sys.argv[1]
    package_type_filter = sys.argv[2]
except:
    print ("USAGE: {} <sbom_results_directory> <package_type>".format(sys.argv[0]))
    print ("\n\tExample: {} ./results java-archive".format(sys.argv[0]))
    print ("\tExample: {} ./results go-module".format(sys.argv[0]))
    print ("\tExample: {} ./results rpm".format(sys.argv[0]))        
    print ("\tExample: {} ./results all".format(sys.argv[0]))
    sys.exit(1)

results = {}
tcount = 0
pcount = 0
try:
    for image in os.listdir(results_dir):
        syftjson = "{}/{}/sbom/syftjson.json".format(results_dir, image)
        if os.path.exists(syftjson):
            with open (syftjson, 'r') as FH:
                sbom = json.loads(FH.read())
            for artifact in sbom.get('artifacts', {}):
                pname = artifact.get('name', "")
                pvers = artifact.get('version', "")
                ptype = artifact.get('type', "")
                plang = artifact.get('language', "")
                if package_type_filter == 'all' or ptype == package_type_filter:
                    if pname not in results:
                        results[pname] = 0
                    results[pname] = results[pname] + 1
                    pcount = pcount + 1
                tcount = tcount + 1

    for pname in sorted(results, key=results.get, reverse=False):
        print ("name={} count={} percentage_type={:.2f}%".format(pname, results[pname], 100.0 * (results[pname] / pcount)))
    print ("----------------------------------")
    print ("total_{}_packages_analyzed={}".format(package_type_filter, pcount))
except Exception as err:
    raise err
    
sys.exit(0)
