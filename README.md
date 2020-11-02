<p align="center">
  <a href="https://www.github.com/shisito">
    <img alt="Shisito" src="https://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/hot-pepper.png" width="60" />
  </a>
</p>
<h1 align="center">
  Shisito Markdown Validation
</h1>
<h3 align="center">
  Sweet, spicy, and rich markdown validation tests.
</h3>
<p align="center">
  <a href="https://github.com/teddywilson/shisito/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="Shisito is released under the MIT license." />
  </a>
</p>

Shisito is a Github action used for validating markdown/YAML files as part of your CI pipeline.

Use frameworks like [Gatsby](https://github.com/gatsbyjs/gatsby) and
[Jekyll](https://jekyllrb.com/) to host your content without having to
worry about corrupted markdown files upon deployment.

## Getting started

1. **Add the Shisito Github action to your workflow.**

In your your workflow `.yml` file, add Shisito. You can find the latest version at the following: https://github.com/teddywilson/shisito/releases.

```
name: CI
on: [push]

jobs:
  build-library:
    runs-on: ubuntu-latest
    name: build-library
    steps:
      - uses: actions/checkout@v1
      - uses: teddywilson/shisito@{VERSION}
```

2. **Define your configuration file.**

In the root directory of your repository, you must define a `shisito.yml` file. This configuration file provides Shisito with the information it needs to run validation tests against your files.

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
      - hosts: list
```

That's it!

## Documentation

| Field | Type | Description |
|-------|------|-------------|
|collections|list|Top-level list of file collections you want to run tests against|
|filepattern|string|Filepattern that follows standard Unix file expansion (e.g., `files/*.markdown`, `content/posts/*[1-9].yml`, etc.)|
|fields|list|Individual fields, and their corresponding types, within a collection. Currently, `str`, `int`, and `list` are supported|

NOTE: currently, Shisito offers one level of depth (or two if `list` is used). We are working on supported as many levels of depth as you need.

## Examples
Follow the main example project for a better overview of how Shisito works end to end here: https://github.com/teddywilson/example-shisito-project.

If you have any example projects to offer, please add them here!

## Testing
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

## Contributing
Since Shisito has only just begun development, there is tons of work to do! The main focus at the time being is adding more functionality to the markdown validation test runner. Some of these tasks include the following:
- [ ] More field and type validation, namely list(subtype) validation with multiple levels of depth.
- [ ] Type validation beyond primitives – e.g., phone numbers, emails, etc.
- [ ] Add unit tests to `test_shisito.py` and make `shisito.py` more unit-testable.
- [ ] Literally anything!
