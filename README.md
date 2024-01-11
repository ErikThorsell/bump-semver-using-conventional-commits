Bump your Semantic Version using Conventional Commits
===

A Python CLI tool for calculating how to bump a Semantic Version based on a commit message.


## Installation and Usage

```shell
$> pip install conventional_semver
```

### Configuration

Create a `.toml` file and modify the settings you want to be different from the PCCC defaults.
An example `config.toml` file is present in this repository.


### Usage

The most basic usage of this tool is to create a config file as described above
and pass a conventional commit message as input to the script. 

```shell
$> conventional_semver "fix: ensure /api/list-all returns properly"
$> 0.0.1
```

It is also possible to provide a SemVer as an argument and have the
script calculate the next version:

```shell
$> conventional_semver --semver 1.0.8 "feat: add new cool feature"
$> 1.1.0
```

The tool also supports the SemVer options for pre-releases and build metadata,
using `--pre-release` and `--build-meta`, which will append the provided
strings in a SemVer compatible manner.

```shell
$> conventional_semver --semver 1.0.8 --pre-release alpha.1 --build-meta $(date -u +"%Y-%m-%dT%H:%M:%SZ") "feat: add new cool feature"
$> 1.1.0-alpha.1+2024-01-11T07:21:57Z
```

Note that the lib used for SemVer parsing is a bit more relaxed than the
official documentation, w.r.t. pre-release and build metadata.
Make sure the strings provided follow the SemVer specification!


## Pipeline example

This tool is particularly useful if you work trunk based, as you can use it in 
combination with the information already present in your git repository to 
automatically tag your new commit.
I have created [a sample
project](https://github.com/ErikThorsell/conventional_semver-test) where I
show how to use the tool in a GitHub Workflow, both for validating PRs and for
tagging new commits on `main`.


## Dependencies

The tool relies on [The Python Conventional Commit Parser](https://github.com/jeremyagray/pccc/tree/main) for the
validation of the commit message and on [Python SemanticVersion](https://github.com/rbarrois/python-semanticversion) for
managing the Semantic Version. The former of these use
[the Enchant C Library used by PyEnchant](https://pyenchant.github.io/pyenchant/install.html).
