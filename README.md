# SBOM.me

Welcome to SBOM.me. This is a place to not only learn about SBOMs, but also
start creating and using them yourself in just a couple of minutes.

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

There are currently two popular SBOM formats in use. SPDX and CycloneDX.

### Lifecycle of an SBOM

While an SBOM is a static document, pinpointing what is in software when a
scan was run, there are differet stages of development you can capture and
compare an SBOM. For example we could take a very simple view of breaking
our development down into: source, build, and runtime. Each of these SBOMs
will be different and contain different content. Each stage is important
and should be captured.

#### Source
The source SBOM represents your application during development. This SBOM
could contain development dependencies, development versions of open source
packages. It might contain files that only exist in certain branches of
your source management system.

A source SBOM gives you the ability to understand if any of your
dependencies are outdated (includeing development dependencies, these often
get ignored). You can also use source SBOMs as a sort of time machine to
look back to when a certain file or dependency was first added to the
project.

#### Build
The build SBOM is the SBOM that you generate during a build. It could be a
partial build, or a test build, or even the final build. By generating an
SBOM during the build stage you can look back into what exactly was built
and shipped for any product or component.

This SBOM will differ from the source SBOM because during a build things
can happen that are outisde of a development environment. Maybe a container
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
give us insight into understnading how old our application and depdnecies
are.

## How can I make an SBOM?

The single easiest way to create an SBOM is to use a tool called
[Syft](https://github.com/anchore/syft/)

There are a variety of ways to install Syft, please see these
[instructions](https://github.com/anchore/syft/#installation) for the best
way on your system.

Once Syft is installed, it's very easy to run.

We are going to base these exapmles on Syft itself. The first thing we will
do is pull the Syft GitHub repository

`git clone https://github.com/anchore/syft.git`

### Scanning a directory

You can scan a directory with Syft. We should scan the repository we just
checked out.

First run
```
➜  ~ syft  src/syft
```

This command will give us a lot of output. This is our source SBOM. There
are a lot of packages that won't end up in our final build, so this is a
great example.

Now if we want to do something more useful, we should run

```
➜  ~ syft  -o json --file=syft-source-sbom.json src/syft
 ✔ Indexed src/syft
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
build.

```
➜  ~ syft  -o json --file=syft-build-sbom.json src/syft
 ✔ Indexed src/syft
 ✔ Cataloged packages      [4536 packages]
```

Notice after the build. we have 4536 packages that get scanned now. These
are all the development and build artifacts needed to create the Syft
binary.

And lastly, let's scan the Syft container, which is what gets deployed.

```
➜  ~ ./syft -o json --file=syft-deploy-sbom.json docker.io/anchore/syft:latest 
 ✔ Parsed image
 ✔ Cataloged packages      [227 packages]
```

The container only has 227 packages in it, this seems far more reasonable.
But it's important to keep in mind that all those other packages are part
of our supply chain. We cannot ignore those packages.

## What can I do with an SBOM?

Detect drift between the types above

Look for a certain package as deployed

Look for vulnerabilities, now and in the future

Understand your supply chain
