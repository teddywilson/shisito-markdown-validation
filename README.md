<p align="center">
  <a href="https://www.github.com/shisito">
    <img alt="Shisito" src="https://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/hot-pepper.png" width="60" />
  </a>
</p>
<h1 align="center">
  Shisito
</h1>
<h3 align="center">
  Sweet and spicy markdown validation tests.
</h3>
<p align="center">
  <a href="https://github.com/teddywilson/shisito/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="Shisito is released under the MIT license." />
  </a>
</p>

NOTE: currently the functionality here is extremely limited and needs tons of work.

### Getting started

1. ** Add Shisito to your Github workflow. **

The first step will be to add the Shisito action to your [Github workflow](https://docs.github.com/en/free-pro-team@latest/actions/learn-github-actions/introduction-to-github-actions).

In your your workflow `.yml` file, add Shisito as a step. For example, a simple CI file (`.github/workflows/ci.yml`) that runs on any push, may look like the following (excluding any other steps you might add):

```
name: CI
on: [push]

jobs:
  build-library:
    runs-on: ubuntu-latest
    name: build-library
    steps:
      - uses: actions/checkout@v1
      # Find most recent version at: https://github.com/teddywilson/shisito/releases
      - uses: teddywilson/shisito@{VERSION}
```

2. ** Define your Shisito configuration file. **

In the root directory of your project, you must define a `shisito.yml` file. This configuration file provides Shisito with the information it needs to run tests against your markdown files.

An example `shisito.yml` file:

```
collections:
  -
    filepattern: authors/*
    fields:
      - name: str    
  -
    filepattern: events/*
    fields:
      - name: str
      - max_capacity: int
```

TODO: document fields and types instead of providing a sample file.

Supported types: `[str, int]`

### Examples
Follow the main example project for a better overview of how Shisito works end to end here: https://github.com/teddywilson/example-shisito-project.

If you have any example projects to offer, please add them here!

### Testing
Currently testing is pretty limited, but I am working on it. For the time being, to test out new functionality, clone the sample project, and run it using a local build of Shisito.

For example:
```
git clone https://github.com/teddywilson/example-shisito-project

cd shisito
Docker build -t shisito .

Docker run \
  -v /Path/to/example-shisito-project:/github/workspace \
  shisito
```

Any help with testing/setup would be greatly appreciated!

### Contributing
Since Shisito has only just begun development, there is tons of work to do! The main focus at the time being is adding more functionality to the markdown validation test runner. Some of these tasks include the following:
- Field and type validation
- Type validation beyond primitives – e.g., phone numbers, emails, etc.
- Literally anything!
