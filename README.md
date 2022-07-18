# SBOMER
An example project showing off Software Bill of Material (SBOM). We focus on how to create an SBOM and more importantly, what you can do with an SBOM once you have it!

SBOMer will generate SBOMs from a number of popular container images every night. The list can be found [input_images/popular_dockerhub_images](here). The [https://github.com/syft](Syft) SBOM scanner is used to generate the output SBOMs. Syft is REALLY easy to run. It can output SPDX, CycloneDX, and Syft JSON SBOM files.

This project contains a couple of directories

## [input_images](input_images)
The input image file lives in this directory. You can add new things to scan with a pull request.

## [results](results)
This is where the SBOM output is stored. Feel free to take a look around. We only output JSON right now. If you think XML would be useful, Syft can certainly do that.

## [scripts](scripts)

There are a couple of scripts here that help show off what you an do with an SBOM.

```
generate_dockerhub_images.py
make_sboms.sh
make_vulnscans.sh
package_type_summarize.py
package_name_summarize.py
search_for_package.py
```

We'll discuss what these all do later in teh document

# Creating an SBOM
Let's talk about what an SBOM is and how to create it.

# What can we do with an SBOM?
There are a few things we can do wtih an SBOM today. It's very new technology, so as we see more use of SBOMs, we will see new and novel ideas. If you can think of something we haven't, please let us know with a pull request!

## Vulnerability scanning
You can use an SBOM to scan for vulnerabilities.

It's REALLY fast.

## Searching for packages
Log4j is one of the finest examples of wanting to look for a certain pakage in your data.

Historic data

Current data

## Gaining insight into your software
What do you have? What does it do? Where did you get it from?

Technology used (or not used)

