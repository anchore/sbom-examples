#!/usr/bin/env python3

import json
import sys
import os
import re

try:
    results_dir = sys.argv[1]
except:
    print ("USAGE: {} <sbom_results_directory>".format(sys.argv[0]))
    sys.exit(1)

results = {}
tcount = 0
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
                if ptype not in results:
                    results[ptype] = 0
                results[ptype] = results[ptype] + 1
                tcount = tcount + 1

    for ptype in sorted(results, key=results.get, reverse=False):
        print ("type={} count={} percentage_overall={:.2f}%".format(ptype, results[ptype], 100.0 * (results[ptype] / tcount)))
    print ("----------------------------------")
    print ("total_packages_analyzed={}".format(tcount))
except Exception as err:
    raise err
    
sys.exit(0)
