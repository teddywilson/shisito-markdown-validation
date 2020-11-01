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
      - uses: teddywilson/shisito@v0.0.2
```

2. ** Define your Shisito configuration file. **

In the root directory of your project, you must define a `shisito.yml` file. This configuration file provides Shisito with the information it needs to run tests against your markdown files.

| Key             | Required | Type   | Description                                                |
| --------------- | -------- | ------ |------------------------------------------------------------|
| filepattern     | yes      | string | Filepattern string which follows standard Unix file expansion. E.g., (`files/*`, `files/*/*.md`). If you don't specify a file extension *all* files will be ran against validation tests.|

An example `shisito.yml` file:

```
filepattern: content/posts/*.md
```

### Examples
Follow the main example project for a better overview of how Shisito works end to end here: https://github.com/teddywilson/example-shisito-project.

If you have any example projects to offer, please add them here!

### Contributing
Since Shisito has only just begun development, there is tons of work to do! The main focus at the time being is adding more functionality to the markdown validation test runner. Some of these tasks include the following:
- Validating markdown files exist (lol this is obviously step 1)
- Field and type validation
- Type validation beyond primitives – e.g., phone numbers, emails, etc.
- Literally anything!
