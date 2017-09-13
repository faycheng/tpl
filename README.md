# tpl

A command line utility for generating files or directories from template.

Official templates: [https://github.com/python-tpl](https://github.com/python-tpl)

Watch the demo:

[![asciicast](https://asciinema.org/a/137513.png)](https://asciinema.org/a/137513)

### Main Features

* Work with Python 3
* Simple but flexible commands
* Render directory names and file names
* Support unlimited levels of directory nesting
* Auto prompt for missing input
* Organize all of your templates in $HOME/.templates
* A lot of official templates
* Support multiple completers: history, list and path
* After generate hook
* Ignore rules for specifying untracked files or dirs


### Installation

Clone this repo to your local machine and move to the repo directory:

```
git clone https://github.com/python-tpl.git
cd python-tpl
```

Make `manager.sh` executable and run install command:

```
chmod +x manager.sh
./manager.sh install
```
 

### Quick Start

Options:

```
> tpl
Usage: tpl [OPTIONS] COMMAND [ARGS]...

  Command line utility for generating files or directories from template

Options:
  --help  Show this message and exit.

Commands:
  pull    pull repo of template from github
  render  generate files or dirs to output dir
  update  update specified template or all templates

```

First, pull a official template that called pypackage-minial:

```
> tpl pull pypackage-minial
Cloning into '/Users/chengfei/.templates/python-tpl/pypackage-minial'...
remote: Counting objects: 20, done.
remote: Compressing objects: 100% (14/14), done.
remote: Total 20 (delta 1), reused 20 (delta 1), pack-reused 0

```

Then generate your project from this tempalte:

```
> tpl render pypackage-minial --output_dir ./
Package Name: candy-temp
Description: smart temp tools
Author: 程飞
License: MIT License
Classifier: development status :: 1 - planning
Classifier: programming language :: python :: 3
Classifier: topic :: software development :: libraries
Classifier: environment :: console
Classifier: q
render python-tpl/pypackage-minial: successfully

```

Now, every thing is okay. You can find a new project in your working directory.

```
> tree candy-temp
candy-temp
├── README.md
├── candy-temp
│   └── __init__.py
├── manager.sh
├── requirements.txt
├── setup.py
└── tests
    └── __init__.py

2 directories, 6 files
```

If you want to update all of templates in $HOME/.templates, you can input this command:

```
> tpl update
Fetching origin
Already up-to-date.
update /Users/chengfei/.templates/python-tpl/pyignores successfully
Fetching origin
Already up-to-date.
update /Users/chengfei/.templates/python-tpl/pymanager successfully
Fetching origin
remote: Counting objects: 3, done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 1), reused 3 (delta 1), pack-reused 0
Unpacking objects: 100% (3/3), done.
From https://github.com/python-tpl/pypackage-minial
   7f193b3..7866eb5  master     -> origin/master
Updating 7f193b3..7866eb5
Fast-forward
 classifiers | 643 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 643 insertions(+)
 create mode 100644 classifiers
update /Users/chengfei/.templates/python-tpl/pypackage-minial successfully

```


### Contribute

1. Fork the repository
1. Raise an issue or make a pull request

### License

MIT License

