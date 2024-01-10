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

The tool also supports the SemVer options for pre-releases and build metadata:

--pre-release
--build-meta

which will append the provided strings in a SemVer compatible manner.

```shell
$> conventional_semver --semver 1.0.8 --pre-release alpha.1 --build-meta $(date -I) "feat: add new cool feature"
$> 1.1.0-alpha.1+2024-01-10
```

Note that the lib used for SemVer parsing is a bit more relaxed than the
official documentation, w.r.t. pre-release and build metadata.
Make sure the strings provided follow the SemVer specification!


## Pipeline example

This tool is particularly useful if you work trunk based, as you can use it in combination with
the information already present in your git repository to automatically tag your new commit.
The example below will compute a `new_tag` based on the latest commit message _and_ the latest
version on the branch and then create a corresponding tag.

```shell
$> new_tag=$(conventional_semver -s -l "feat: add new cool feature")
$> git tag -a $new_tag -m "bump"
$> git push origin $new_tag
```


## Dependencies

The tool relies on [The Python Conventional Commit Parser](https://github.com/jeremyagray/pccc/tree/main) for the
validation of the commit message and on [Python SemanticVersion](https://github.com/rbarrois/python-semanticversion) for
managing the Semantic Version. The former of these use
[the Enchant C Library used by PyEnchant](https://pyenchant.github.io/pyenchant/install.html).
