# PEP parser app

## Description
This application parses the PEP site. It has 3 modes:
1) ```python main.py whats-new``` - collects article info for different versions of Python (topics, links, and authors).
2) ```python main.py latest-versions``` - collects links on docs, version numbers, and statuses for different Python versions.
3) ```python main.py download``` - download docs for the latest version of python.
4) ```python main.py pep``` - count the number of PEPs divided by status and print mismatched statuses (table vs. PEP description card).

The application has several optional parameters:
1) ```-c --clear-cache``` - clear the cache
2) ```-o --output``` - set the mode of output: ```pretty``` - draw a table in command line for output; ```file``` - create a file with output data.

# Libs
| Technologies | Link |
| ---- | ---- |
| ![git_BeautifulSoup](https://github.com/pandenic/PEP_BeautifulSoup_parser/assets/114985447/22f818bc-d8df-4085-bfa6-26b6fd092f1b) | [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) |



