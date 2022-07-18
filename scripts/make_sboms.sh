#!/bin/bash

if [ ! -x './syft' ]; then
    echo "Command ./syft must exist and be executable"
    exit 1
fi

# construct full set of input images
IMAGES=`cat input_images/* | sort | uniq`

# iterate over each image in the set
for image in ${IMAGES}
do
    echo "Processing image ${image}: start"
    # create a 'directory' friendly string
    ODIR_IMAGE=`echo ${image} | sed "s/\//_/g"`

    # main work - try to create a result directory, try to create a syft native sbom, try to create spdx/cyclone format sboms.  if pre condition fails, skip processing and move on
    if ( mkdir -p ./results/${ODIR_IMAGE}/sbom ); then
	if ( ./syft -q -o json registry:${image} > ./results/${ODIR_IMAGE}/sbom/syftjson.json ); then
	    ./syft -q convert ./results/${ODIR_IMAGE}/sbom/syftjson.json -o spdx-json=./results/${ODIR_IMAGE}/sbom/spdx.json
	    ./syft -q convert ./results/${ODIR_IMAGE}/sbom/syftjson.json -o cyclonedx-json=./results/${ODIR_IMAGE}/sbom/cyclonedx.json
	else
	    rm -f ./results/${ODIR_IMAGE}/sbom/syftjson.json ./results/${ODIR_IMAGE}/sbom/spdx.json ./results/${ODIR_IMAGE}/sbom/cyclonedx.json
	    rmdir ./results/${ODIR_IMAGE}/sbom/ ./results/${ODIR_IMAGE}/
	    echo "cannot generate syft SBOM for image ${image}, moving on"
	fi
    else
	echo "cannot make result directory for image ${ODIR_IMAGE}, moving on"
    fi
    echo "Processing image ${image}: complete"
    echo
done
date > ./results/last_updated
exit 0
