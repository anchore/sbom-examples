# SBOM.me

Welcome to SBOM.me. This is a place to not only learn about SBOMs, but also
start creating and using them yourself in just a couple of minutes. It's usually easier to learn by doing than it is just to read, there are plenty of examples here for everyone.

This is all hosted in GitHub, feel free to checkout the
[ABOUT.md](ABOUT.md) for more details on the repository itself.

## What is an SBOM?

A "software bill of materials", or SBOM, is a document that describes the
contents of a software application. Everything from the existing files in
the application to the open source components added during the application
build. The content of the SBOM is meant to represent a snapshot of the
contents at a given time and stage in the lifecycle of software.

You can find more details on SBOM at the [CISA SBOM
site](https://www.cisa.gov/sbom)

### SBOM formats

There are currently two popular SBOM formats in use. [SPDX](https://spdx.dev/) and [CycloneDX](https://cyclonedx.org/). Feel free to visit the websites for each format to better understand them.

Rather than focus on one SBOM format, we encourage generating both SPDX and CycloneDX documents. By generating both formats, it allows SBOM consumers to use whichever format their tools support.

### Lifecycle of an SBOM

While an SBOM is a static document, pinpointing what is in software when a
scan was run, there are different stages of development you can capture and
compare an SBOM. For example we could take a very simple view of breaking
our development down into: source, build, and runtime. Each of these SBOMs
will be different and contain different content. Each stage is important
and should be captured and analyzed.

These stages should be thought of only as examples. There is no definitive list of SBOM lifecycle stages yet. The best explanation of lifecycle is probably from the Supply chain Levels for Software Artifacts, or SLSA project. You can review their lifecycle [here](https://slsa.dev/spec/v0.1/index#slsa-101).

As SBOM usage evolves we will see new and different guidance on this topic. Check back in regularly as we will continue to update this site as the industry helps define how to create and use SBOMs.

#### Source
The source SBOM represents your application during development. This SBOM
could contain development dependencies, development versions of open source
packages, and software needed to build an application. It might contain files that only exist in certain branches of your source management system.

A source SBOM gives you the ability to understand if any of your
dependencies are outdated (including development dependencies, these often
get ignored). You can also use source SBOMs as a sort of time machine to
look back to when a certain file or dependency was first added to the
project.

#### Build
The build SBOM is the SBOM that you generate during a build. It could be a
partial build, or a test build, or even the final build. By generating an
SBOM during the build stage you can look back into what exactly was built
and shipped for any product or component.

This SBOM will differ from the source SBOM because during a build things
can happen that are outside of a development environment. Maybe a container
is created. A binary could be copied into the build. Builds can be signed
during this stage, the signatures and checksums can also be captured by the
SBOM scanner.

#### Runtime

A runtime SBOM is the thing that will be deployed into an environment. It
will contain final builds, supporting libraries (like an operating system
or container image). The configuration files have been updated, defaults
have probably changed. It's even possible someone modified some of the
contents that we were tracking in the build SBOM.

The runtime SBOM can help us understand when our application contains
security vulnerabilities. It can give us insight into what we've changed in
our running deployment vs what we received from our vendor. It can also
give us insight into understanding how old our application and dependencies
are.

## How can I make an SBOM?

The single easiest way to create an SBOM is to use a tool called
[Syft](https://github.com/anchore/syft/)

There are a variety of ways to install Syft, please see these
[instructions](https://github.com/anchore/syft/#installation) for the best
way on your system.

Once Syft is installed, it's very easy to run.

We are going to base these examples on Syft itself. The first thing we will
do is pull the Syft GitHub repository then scan the Syft source code.

`git clone https://github.com/anchore/syft.git`

### Scanning a directory

You can scan many different types of artifacts with Syft. In this instance we will scan a directory with Syft. We should scan the repository we just
checked out.

First run
```
➜  ~ syft  dir:./syft
```

This command will give us a lot of output. This is our source SBOM. There
are a lot of packages that won't end up in our final build, so this is a
great example.

Now if we want to do something more useful, we should run

```
➜  ~ syft  -o json --file=syft-source-sbom.json dir:./syft
 ✔ Indexed ./syft
 ✔ Cataloged packages      [841 packages]
```

The 841 packages will be important later, so keep it in mind. These
packages are all the things included in Syft that we need to develop it.
This isn't an uncommonly large number, this is pretty normal.

The `-o json` tells syft to use the syft json format. Because we will use
this file later with Grype, we are going to stick with the Syft format. But
Syft supports a variety of formats including SPDX and CycloneDX.

The `--file=syft-sbom.json` is the output file of the command.

Now let's generate a build SBOM. How to build Syft is a bit more complex
than we want to cover here, but here's what happens when when we scan the
Syft directory after the build runs.

```
➜  ~ syft  -o json --file=syft-build-sbom.json dir:./syft
 ✔ Indexed ./syft
 ✔ Cataloged packages      [4536 packages]
```

Notice after the build. we have 4536 packages that get scanned now. These
are all the development and build artifacts needed to create the Syft
binary. This shows why there is a difference between source and build SBOMs, and why it's important.

And lastly, let's scan the Syft container, which is what will be deployed. This is the runtime SBOM.

```
➜  ~ ./syft -o json --file=syft-deploy-sbom.json docker.io/anchore/syft:latest 
 ✔ Parsed image
 ✔ Cataloged packages      [227 packages]
```

The container only has 227 packages in it, this seems far more reasonable.
It's important to keep in mind that these 227 packages, as well as all those other packages from source and build are part of our supply chain. All the packages matter.

## What can I do with an SBOM?

Once we have an SBOM, the question of what to do with it arises. There are many vendors and projects dedicated to managing SBOMs. We aren't going to cover SBOM management here, but we will cover some of the use cases that exist today. As SBOM understanding and technology improve, we will see many more use cases.

### Detect drift between the types above

One use is to compare what packages are added and removed between the SBOM types, as well as how those packages change over time.

In our above example, we add and remove a large number of packages between the source, build, and deploy stages. This is a form of SBOM drift that detects changes in a single version. We can also track SBOM drift across versions.

If we look at two different Syft versions

```
➜  ~ syft -o json --file=syft-56-sbom.json anchore/syft:v0.56.0
 ✔ Loaded image
 ✔ Parsed image
 ✔ Cataloged packages      [216 packages]
 ```

```
➜  ~ syft -o json --file=syft-40-sbom.json anchore/syft:v0.40.0
 ✔ Loaded image
 ✔ Parsed image
 ✔ Cataloged packages      [241 packages]
 ```

We can see a difference in the number of packages. We can also inspect the two SBOMs to better understand what is different. We will see some packages added, some removed, and new versions.

### Look for a certain package as deployed

At the end of 2021, the Log4Shell incident altered the course of software supply chain security for many of us. A huge number of organizations were tasked with uncovering if they had Log4j anywhere. For most this means manually searching for Log4j which was extremely disruptive and time consuming.

This is a great use case for keeping track of SBOMs for your software.

If you were lucky enough to have been generating and storing SBOMs before Log4Shell, finding Log4j was really just doing a search across all your SBOMs. That then told you were Log4j is, and also where it was in the past.

There will be events again in the future where we will need to know if we have a certain piece of software running. If you have SBOMs, this is a very easy question to answer.

### Look for vulnerabilities, now and in the future

SBOMs can also be used to scan an application for vulnerabilities. Historically scanning an application for vulnerable components meant pointing the scanner at the software, letting it run, then interpreting the results. These scans could take seconds or minutes and were often disruptive to running systems.

As you can imagine, with an SBOM, you can ask the scanning to skip the discovery phase and just report back on vulnerable packages. There is a companion tool to Syft called [Grype](https://github.com/anchore/grype) that can do just this.

For example we can scan the Syft version 56 SBOM we just generated.

```
➜  ~ grype sbom:syft-56-sbom.json
 ✔ Scanned image           [2 vulnerabilities]

NAME                        INSTALLED  FIXED-IN  TYPE       VULNERABILITY   SEVERITY
google.golang.org/protobuf  v1.28.1              go-module  CVE-2015-5237   High
google.golang.org/protobuf  v1.28.1              go-module  CVE-2021-22570  Medium
```
Rather than having to first scan the Syft container, Grype can use the SBOM to very quickly return results.

We also gain the historic benefit from SBOMs. We can not only scan the latest version of software we have, we could scan history SBOMs to ask questions like "was this container vulnerable to Log4Shell". When there is a significant security event, it can be very valuable to look back in time at things that were once deployed. If you know a vulnerability was being exploited in the past, you can make informed decisions if you know what was vulnerable at that point in time.

The added benefit of this is we often don't keep old container images around for long periods of time as they are large. SBOMs tend to be fairly small, storing them for a very long time makes sense.

### Understand your supply chain

Lastly, and possibly most importantly. SBOMs help us understand our overall supply chain. We can understand the software we are building. The open source components we are pulling in. The versions of libraries in use. The rate at which we are updating the libraries.

There are some tools to do these things today (the SBOM format websites track these tools). Some of the tasks need to be done by hand. We are the beginning of creating the SBOM ecosystem, there are far more ideas than tools at this point. But as all new industries work, part of this challenge is to understand the problems, then create solutions.