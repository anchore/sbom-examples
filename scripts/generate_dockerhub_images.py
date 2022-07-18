#!/usr/bin/env python3

import requests
import sys
import json

url = "https://hub.docker.com/v2/repositories/library/?page=1&page_size=15"

output = { "containers": [] }

convert_map = {
    # these images do not publish a 'latest' tag
    "library/elasticsearch:latest": ["library/elasticsearch:8.3.2"],
    "library/kibana:latest": ["library/kibana:8.3.2"],
    "library/logstash:latest": ["library/logstash:8.3.2"],    
    "library/jenkins:latest": ["library/jenkins:2.60.3"],
    "library/oraclelinux:latest": ["library/oraclelinux:9"],
    "library/rockylinux:latest": ["library/rockylinux:9"],
    # these images have special tag layouts
    "library/notary:latest": ["library/notary:signer", "library/notary:server"],
    "library/opensuse:latest": ["opensuse/leap:latest", "opensuse/tumbleweed:latest"],
}

skip_map = {
    # these images have limited architecture builds available
    "library/clefos:latest": True,
    "library/docker-dev:latest": True,
    "library/ibm-semeru-runtimes:latest": True,
    "library/ubuntu-upstart:latest": True,
    "library/ubuntu-debootstrap:latest": True,
    "library/scratch:latest": True,
}


input_images = []
try:
    input_file = sys.argv[1]
    with open(input_file, 'r') as FH:
        for line in FH.readlines():
            line = line.strip()
            if line:
                input_images.append(line)
except:
    print ("USAGE: {} <file_with_images>".format(sys.argv[0]))
    sys.exit(1)
    

while True:
    response = requests.get(url)

    container_data = response.json()

    for i in container_data['results']:
        image = "{}/{}:latest".format(i['namespace'], i['name'])
        if image in skip_map:
            continue
        
        if image in convert_map:
            images = convert_map[image]
        else:
            images = [image]

        for i in images:
            istring = "docker.io/{}".format(i)
            if istring not in input_images:
                input_images.append(istring)

    if container_data['next'] is None:
        with open(input_file, 'w') as OFH:
            for i in input_images:
                OFH.write("{}\n".format(i))
        sys.exit(0)

    url = container_data['next']
