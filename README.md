# The Clark Kent Reporter
<!-- ## A Mild Mannered-Reporter for your Data Science Projects with hidden superpowers. -->

A mild-mannered reporter with hidden superpowers for your data science projects.
---

![header](images/header.gif)


**Version 1.0.0**

**Created by Graham Waters**

<!-- add badges for the issues, release, latest updates, and stars/forks -->

[![GitHub issues](https://img.shields.io/github/issues/grahamwaters/Clark-Kent-Reporter)](https://img.shields.io/github/issues/grahamwaters/Clark-Kent-Reporter)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/grahamwaters/Clark-Kent-Reporter)](https://img.shields.io/github/v/release/grahamwaters/Clark-Kent-Reporter)
[![GitHub last commit](https://img.shields.io/github/last-commit/grahamwaters/Clark-Kent-Reporter)](https://img.shields.io/github/last-commit/grahamwaters/Clark-Kent-Reporter)
[![GitHub stars](https://img.shields.io/github/stars/grahamwaters/Clark-Kent-Reporter)](https://img.shields.io/github/stars/grahamwaters/Clark-Kent-Reporter)
[![GitHub forks](https://img.shields.io/github/forks/grahamwaters/Clark-Kent-Reporter)](https://img.shields.io/github/forks/grahamwaters/Clark-Kent-Reporter)
<!-- add view count to the repo -->
![ViewCount](https://views.whatilearened.today/views/github/grahamwaters/Clark-Kent-Reporter.svg)

# Table of Contents

- [The Clark Kent Reporter](#the-clark-kent-reporter)
  - [A mild-mannered reporter with hidden superpowers for your data science projects.](#a-mild-mannered-reporter-with-hidden-superpowers-for-your-data-science-projects)
- [Table of Contents](#table-of-contents)
- [Automatic Report Generation with Clark Kent Reporter](#automatic-report-generation-with-clark-kent-reporter)
- [What does The Clark Kent Reporter do?](#what-does-the-clark-kent-reporter-do)
- [How to Get Clark Running](#how-to-get-clark-running)
- [Installation](#installation)
- [Contributing](#contributing)
- [Example Use Case](#example-use-case)
  - [The Files](#the-files)
  - [The Steps](#the-steps)
- [License](#license)
- [Acknowledgments](#acknowledgments)
  - [The openai main file](#the-openai-main-file)


# Automatic Report Generation with Clark Kent Reporter
**Latest Version: 1.0.0**

**Created by Graham Waters**

# What does The Clark Kent Reporter do?

<!-- This tool converts a traditionally formatted overview (in a readme file) into a populated Jupyter Notebook for data science presentations or findings presentations. If you've ever been under a time constraint and needed to generate a report quickly in Jupyter Notebook format but found that you wrote most of your analysis in a markdown file, then you just found the solution to our mutual dilemma.

This project is currently being developed in my free time, and any pull requests will be reviewed as soon as I can. There are some areas where it could be beefed up and made more robust and dynamic. I welcome your input.

The code has been written with Python 3.9.6 and developed in Visual Studio Code. As far as I am aware, it should run on macOS X 10.11 or later and on any computer. This is not my area of expertise, and if your distribution is incompatible, please add it to the issues section.

Finally, It's worth noting that this software doesn't magically transform your work from a document to a presentation, which will still require the careful work that data scientists and analysts are known for. However, it does make sure you don't have to start from scratch when making an interactive and working notebook out of something that would otherwise take hours manually write everything out again. The idea came about when I was parsing my old repositories for what I wanted to include in my official portfolio. I realized how many readmes I would be reading if I did it the old-fashioned way. I decided to standardize what a data science notebook should look like, and once that was done, it was pretty simple to move forward. After a while, I decided to do away with the manual process and let this little tool automate the whole thing, well, at least most of the grunt work.
I hope this brings you as much joy as it does me!
Happy Coding! -->

This tool converts a traditionally formatted overview (in a readme file) into a populated Jupyter Notebook for data science presentations or findings presentations. It doesn't magically transform your work from a document to a presentation, which will still require the careful work that data scientists and analysts are known for. However, it does make sure you don't have to start from scratch when making an interactive and working notebook out of something that would otherwise take hours manually write everything out again. I realized how many readmes I would be reading if I did it the old-fashioned way.

![separator](images/sep_1.gif)

# How to Get Clark Running

We recommend using a virtual environment for this. Don't worry if you've never done that before. We did all the heavy lifting for you by including the code here below. Just copy and paste!

```bash
conda create --name clark_kent_reporter python=3.9.6
```
Now that you have your virtual environment set up, you need to activate it. This is done by running the following command:
```bash
conda activate clark_kent_reporter
```
Then install the requirements:
```bash
pip3 install -r requirements.txt
```
You should be good to go!

![separator](images/sep_1.gif)







# Installation
Until we are listed on PyPi you can clone the repo and install locally. I will update this section once we are listed on PyPi.

# Contributing
If you would like to contribute to this project, please feel free to fork the repository and submit a pull request. I will review the pull request as soon as I can. We welcome any and all contributions as this is a growing tool.

# Example Use Case
Let's say I have a project that generates lorebooks for NovelAI [project](https://github.com/grahamwaters/lorebook_generator_for_novelai)
I can use this this tool to generate my overview notebook for the project as follows:

## The Files
1. The readme file for [NovelAI Lorebook Generator](https://github.com/grahamwaters/lorebook_generator_for_novelai) `README.md`.
2. The `MOCKUP_README.md` file in the `root` directory of this repository.

## The Steps
1. Open the [readme file](https://github.com/grahamwaters/lorebook_generator_for_novelai) in a text editor and copy the text.
2. Then I paste the text into the `MOCKUP_README.md` file in the `root` directory of this repository.
3. Then I open [Clark Kent Reporter](scripts/main.py) in Visual Studio Code and run the script.
4. The `destination` and `source` files are set in the `main.py` file. You can change them to whatever you want.
5. The script will generate a notebook file in the `destination` directory. In this case, it will be in the `notebooks` directory. The file will be named `generated_notebook.ipynb`. If this is not the case for you, please open an issue and I will look into it.
# License
This project is licensed under the MIT License - see the `LICENSE.md` file for details
# Acknowledgments
I would like to thank the following people for their support and guidance:
1. Superman - for being the inspiration for this project.
2. Clark Kent, who is clearly not superman. Because he is just a mild mannered reporter.


## The openai main file

Explained:

This script defines a custom preprocessor called CodeBlockPreprocessor that converts markdown cells in a Jupyter Notebook that contain code blocks into markdown cells with the code blocks rendered as code outputs.

It also defines a function called markdown_to_notebook that takes a path to a markdown file and a path to a Jupyter Notebook file as input, and converts the markdown file into a Jupyter Notebook file. It does this by reading the markdown file, creating a Jupyter Notebook with the markdown text, preprocessing the notebook to convert markdown cells with code blocks into code cells, executing the code cells, and then saving the executed notebook to the specified file path.

This script also contains a commented-out function called convert_directory that is not yet implemented. This function would be used to convert all markdown files in a specified input directory into Jupyter Notebooks and save them to a specified output directory.


Then we run the `convert_directory` function.

With this function implemented, you could use the script to convert all markdown files in a specified input directory into Jupyter Notebooks and save them to a specified output directory. For example, you could use the following code to convert all markdown files in the "markdown" directory to Jupyter Notebooks and save them to the "notebooks" directory:
