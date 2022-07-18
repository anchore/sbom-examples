#!/bin/bash

# construct full set of input images
IMAGES=`cat input_images/* | sort | uniq`

# iterate over each image in the set
for image in ${IMAGES}
do
    echo "Processing image ${image}: start"
    # create a 'directory' friendly string
    ODIR_IMAGE=`echo ${image} | sed "s/\//_/g"`

    # main work - try to create a result directory, try to create a syft native sbom, try to create spdx/cyclone format sboms.  if pre condition fails, skip processing and move on
    if [ -f ./results/${ODIR_IMAGE}/sbom/syftjson.json ]; then
	if ( mkdir -p ./results/${ODIR_IMAGE}/vulnscan ); then
	    if ( ./grype -q -o json ./results/${ODIR_IMAGE}/sbom/syftjson.json > ./results/${ODIR_IMAGE}/vulnscan/grypejson.json ); then
		./grype -q -o cyclonedx ./results/${ODIR_IMAGE}/sbom/syftjson.json > ./results/${ODIR_IMAGE}/vulnscan/cyclonedx.json
	    else
		rm -f ./results/${ODIR_IMAGE}/vulnscan/grypejson.json ./results/${ODIR_IMAGE}/vulnscan/cyclonedx.json 
		rmdir ./results/${ODIR_IMAGE}/vulnscan/
		echo "cannot generate grype vulnscan for image ${image}, moving on"
	    fi
	else
	    echo "cannot make result directory for image ${ODIR_IMAGE}, moving on"
	fi
    fi
    echo "Processing image ${image}: complete"
    echo
done
