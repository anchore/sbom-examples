# SBOM Examples
Welcome to SBOM-Examples. This site is a project showing off Software Bill of Material (SBOM). We focus on how to create an SBOM and more importantly, what you can do with an SBOM once you have it!

SBOM Examples will generate SBOMs from a number of popular container images every night. The list can be found [input_images/popular_dockerhub_images](here). The [https://github.com/syft](Syft) SBOM scanner is used to generate the output SBOMs. Syft is REALLY easy to run. It can output SPDX, CycloneDX, and Syft JSON SBOM files.

If you plan to work with this Git repository you will need to install the
git-lfs module then run `git-lfs install`. There are a lot of large SBOM
files in this repo that are stored using Git Large File Storage.

This project contains a couple of directories

## [Input Images](input_images)
The input image file lives in this directory. You can add new things to scan with a pull request.

## [Results](results)
This is where the SBOM output is stored. Feel free to take a look around. We only output JSON right now. If you think XML would be useful, Syft can certainly do that.

## [Scripts](scripts)

There are a couple of scripts here that help show off what you an do with an SBOM.

```
generate_dockerhub_images.py
make_sboms.sh
make_vulnscans.sh
package_type_summarize.py
package_name_summarize.py
search_for_package.py
```

We'll discuss what these all do later in the document

# Creating an SBOM
Let's talk about what an SBOM is and how to create it.

You can find out more about SBOMs [https://www.cisa.gov/sbom](here).
There's a lot of great details about the SBOM form from that CISA site.

There are many tools that can generate an SBOM. For the purposes of
simplicity we are going to focus on the Syft SBOM scanner. You can install
Syft a number of ways, take a look at the Syft GitHub
[https://github.com/anchore/syft/#installation](repo).

Once we have syft, it's as easy as running

```
syft debian:latest
```

to scan the latest Debian container image for example. If we want to output
a SPDX JSON file, we can run

```
syft -o spdx-json debian:latest
```

There are a LOT of options for running syft. You can scan container images,
directories, files, registries. And it's all extremely easy.

# What can we do with an SBOM?
There are a few things we can do wtih an SBOM today. It's very new technology, so as we see more use of SBOMs, we will see new and novel ideas. If you can think of something we haven't, please let us know with a pull request!

## Vulnerability scanning
You can use an SBOM to scan for vulnerabilities. And it's REALLY fast.

For example we can use [https://github.com/anchore/grype/](Grype) to scan
an SBOM document instead of scanning the actual content. For example

```
grype sbom:./debian-latest.json
```

## Searching for packages
Log4j is one of the finest examples of wanting to look for a certain pakage in your data.

XXX: Add a note about the scripts that can do this

One use when searching for packages is having the ability to gaze into the
past to ask questions about certain packages that you have shipped. For
example if you need to know if you shipped a certain logging package in any
of your software, you can quickly figure this out by just searching the
stored SBOMs.

You can also use SBOMs to understand your currently running packages. If
you need to know if a specific version of a popular logging package is
being used in production, you can save a lot of time with a list of
currently running SBOMs.

## Gaining insight into your software

SBOMs are a form of observability for our software. We quickly answer
questions like what technologies and languages are in use. Which Linux
distributions are deployed. How are we using certain dependencies. How many
dependencies do we have. What open source licenses are in use. And many
other questions.

The foundation of the software supply chain is an SBOM document.
