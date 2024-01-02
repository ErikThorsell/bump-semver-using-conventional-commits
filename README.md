Bump your Semantic Version using Conventional Commits
===

A Python CLI tool for calculating the Semantic Version based on a commit message and an
existing SemVer.

A tool like this shines when put in a trunk based workflow, where every commit on trunk is
built (only once) and must be given a version.
Since **the tool itself never modifies your git repository** you can safely use it both as
part of your PR phase (answering the question: _If this PR is merged right now, what would
the version be_?) and to inform your CI/build-system how to tag a new commit on trunk.


## Installation and Usage

```shell
$> pip install conventional-commits-cli
```

### Example with version provided

For maximum flexibility, the tool can be run with both the message and current version as inputs:

```shell
$> conventional-commits-cli -m "feat: add list_all to /api/v2" -v "1.3.5"
1.4.0
```

### Example with version fetched from branch

It is also possible to fetch the latest tag from the current branch, using the `-l / --local` option:

```shell
# on branch main where HEAD~1 is tagged with 1.3.5
$> conventional-commits-cli -m "feat: add list_all to /api/v2" -l
1.4.0
```

This is particularly useful if you work trunk based as you can use it in combination with
the information already present in your git repository to automatically tag your new commit.
The example below will compute a `new_tag` based on the latest commit message _and_ the latest
version on the branch and then create a corresponding tag.

```shell
$> new_tag=$(conventional-commits-cli -m "$(git show -s --format=%s)" -l)
$> git tag -a $new_tag -m "bump"
$> git push origin $new_tag
```


## Dependencies

The tool relies on [The Python Conventional Commit Parser](https://github.com/jeremyagray/pccc/tree/main) for the
validation of the commit message and on [Python SemanticVersion](https://github.com/rbarrois/python-semanticversion) for
managing the Semantic Version.


## Prerequisites

* [The Enchant C Library used by PyEnchant](https://pyenchant.github.io/pyenchant/install.html)