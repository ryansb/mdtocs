#MDTOCS

##MarkDown Table Of Contents System

Written to add [doctoc](https://github.com/thlorenz/doctoc) like functionality
to Python using only the standard library.

#Installation

`pip install git+https://github.com/ryansb/mdtocs/`

##Or

```
$ curl -s -L https://raw.github.com/ryansb/mdtocs/master/mdtocs/__init__.py > ~/bin/mdtocs
$ chmod a+x ~/bin/mdtocs
```


#Usage

##From the CLI

```bash
$ #Add table of contents to all markdown files in your current directory
$ mdtocs
$ #Recursively add table of contents to every markdown file below the current directory
$ mdtocs -r
$ #Recursively add table of contents to every markdown file in the specified dirs
$ mdtocs -r README.md LICENSE.md content/ tutorials/
```

##From Python

```python
from mdtocs import tocify, tocify_file_list, tocify_string, tocify_split

orig = [
    "#a markdown doc with headers\n",
    "\n",
    "Separated into lines\n",
]

toc, body = tocify_split(orig)

body = tocify_string(''.join(orig))

body = tocify_file_list(['list', 'of', 'markdown', 'files'])
```

#License

LGPL3, see LICENSE

#Credits

This is a Python version of the nodejs [doctoc](https://github.com/thlorenz/doctoc).
