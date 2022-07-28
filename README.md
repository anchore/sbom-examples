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

The single easiest way to create an SBOM is to use a tool called Syft

There are many other tools, for the purpose of simplicity we are only
talking about Syft in this space.

## What can I do with an SBOM?

Detect drift between the types above

Look for a certain package as deployed

Look for vulnerabilities, now and in the future

Understand your supply chain
