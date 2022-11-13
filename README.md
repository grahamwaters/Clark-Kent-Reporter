# Clark Kent Reporter
## A Mild Mannered-Reporter for your Data Science Projects with hidden superpowers.

![header](images/header.gif)

[![Build Status](https://travis-ci.org/Clark-Kent-Multitool/Clark-Kent-Multitool.svg?branch=master)](https://travis-ci.org/Clark-Kent-Multitool/Clark-Kent-Multitool)
[![Coverage Status](https://coveralls.io/repos/github/Clark-Kent-Multitool/Clark-Kent-Multitool/badge.svg?branch=master)](https://coveralls.io/github/Clark-Kent-Multitool/Clark-Kent-Multitool?branch=master)
[![Documentation Status](https://readthedocs.org/projects/clark-kent-multitool/badge/?version=latest)](https://clark-kent-multitool.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/Clark-Kent-Multitool.svg)](https://badge.fury.io/py/Clark-Kent-Multitool)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Version 1.0.0**

**Created by Graham Waters**

# Table of Contents

- [Clark Kent Reporter](#clark-kent-reporter)
  - [A Mild Mannered-Reporter for your Data Science Projects with hidden superpowers.](#a-mild-mannered-reporter-for-your-data-science-projects-with-hidden-superpowers)
- [Table of Contents](#table-of-contents)
- [Automatic Report Generator For Avid ReadMe Writers](#automatic-report-generator-for-avid-readme-writers)
- [Table of Contents](#table-of-contents-1)
- [Automatic Report Generator For Avid ReadMe Writers](#automatic-report-generator-for-avid-readme-writers-1)
- [Example Use Case](#example-use-case)


# Automatic Report Generator For Avid ReadMe Writers
**Version 1.0.0**

**Created by Graham Waters**


# Table of Contents

- [Clark Kent Reporter](#clark-kent-reporter)
  - [A Mild Mannered-Reporter for your Data Science Projects with hidden superpowers.](#a-mild-mannered-reporter-for-your-data-science-projects-with-hidden-superpowers)
- [Table of Contents](#table-of-contents)
- [Automatic Report Generator For Avid ReadMe Writers](#automatic-report-generator-for-avid-readme-writers)
- [Table of Contents](#table-of-contents-1)
- [Automatic Report Generator For Avid ReadMe Writers](#automatic-report-generator-for-avid-readme-writers-1)
- [Example Use Case](#example-use-case)


# Automatic Report Generator For Avid ReadMe Writers

Converts a traditionally formatted overview (in a readme file) into a populated Jupyter Notebook for data science presentations or findings presentations. If you've ever been under a time constraint and needed to generate a report quickly in Jupyter Notebook format but found that you wrote most of your analysis in a markdown file, then you just found the solution to our mutual dilemma.

This project is currently being developed in my free time, and any pull requests will be reviewed as soon as I can. There are some areas where it could be beefed up and made more robust and dynamic. I welcome your input.

The code has been written with Python 3.9.6 and developed in Visual Studio Code. As far as I am aware, it should run on macOS X 10.11 or later and on any computer. This is not my area of expertise, and if your distribution is incompatible, please add it to the issues section.

Finally, It's worth noting that this software doesn't magically transform your work from a document to a presentation, which will still require the careful work that data scientists and analysts are known for. However, it does make sure you don't have to start from scratch when making an interactive and working notebook out of something that would otherwise take hours manually write everything out again. The idea came about when I was parsing my old repositories for what I wanted to include in my official portfolio. I realized how many readmes I would be reading if I did it the old-fashioned way. I decided to standardize what a data science notebook should look like, and once that was done, it was pretty simple to move forward. After a while, I decided to do away with the manual process and let this little tool automate the whole thing, well, at least most of the grunt work.
I hope this brings you as much joy as it does me!
Happy Coding!

![separator](images/sep_1.gif)
# Example Use Case
Let's say I have a project that generates lorebooks for NovelAI [project](https://github.com/grahamwaters/lorebook_generator_for_novelai)
I can use this this tool to generate my overview notebook for the project as follows:

```python
import clark_kent_reporter as super_man
# Point to the readme file that you want to convert
readme_file = "README.md" # path to the readme file (absolute path).
# Point to the notebook file that you want to generate
notebook_file = "./reports/auto_report.ipynb" # path to the notebook file (relative path).
```

What we have so far is a set of locations one with the markdown that we want to convert, and the other with the notebook that we want to generate. Now we can use the following code to generate the notebook:

```python
$ python -m clark_kent_reporter -r README.md -n ./reports/auto_report.ipynb
# note: this is untested. The best way is to run the script within the cloned repository.
```
