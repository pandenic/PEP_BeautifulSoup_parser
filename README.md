# PEP parsing app

## Description
This application implement parsing of pep site. It has 3 modes:
1) ```python main.py whats-new``` - collects articles info for different versions of python (topics, links and authors).
2) ```python main.py latest-versions``` - collects links on docs, version numbers and statuses for different versions of python.
3) ```python main.py download``` - download docs for the latest version of python.
4) ```python main.py pep``` - count quantity of PEPs divided by status and print mismatched statuses (table vs PEP description card).

Application has several optional parameters:
1) ```-c --clear-cache``` - clear the cache
2) ```-o --output``` - set the mode of output: ```pretty``` - draw a table in command line for output; ```file``` - create a file with output data.

# Libs
- Beautuful Soup
- tqdm
- requests_cache


