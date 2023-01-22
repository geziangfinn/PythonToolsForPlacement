# Bookshelf-Format-Parser

# About The Project
Benchmark Reader is project that was created as a "by-product" of 2-year experimentation on creating mini hardware placement utilities tools, and other placement related projects.
It serves as a file-parser of all Bookshelf-format Benchmarks and creates an object oriented form of benchmark, as shown below, all according to bookshelf format and standards.
 -  Benchmark (Design instance):
  - Rows
  - Nets
  - Cells
As of 2021 BFP has been the research focus of the paper "Redesign, Extensibility & Evaluation of a Placement Utilities Toolset", DOI: 10.1109/SEEDA-CECNSM53056.2021.9566264.

### Built with 
- Python 3.10.4, compatible with any python 3x. To be safe use the aforementioned version on newer to avoid any obsolete versions of packages.

# Requirements
- Matplotlib. You can install it via a terminal using the command pip3 install matplotlib. (pip3 may be also called as pip depending on the python installations on your system and your OS).

# Getting Started 
- Read/View [example.py](https://github.com/PlebeianDev/Benchmark-Reader-for-Placement-in-Python/blob/master/src/example.py) for simple usage example.
- Be sure to check example.py via a python debugger, so you can have a full view of the design and classes/objects.
- If used as a whole, be sure to place all the project files in the same folder.
- If functions are used separately, will need minor changes depending on how you want to use them.

# New additions
Note that newer additions described below will be updated as I see fit, depending on my research.
- Grid class: Basically divides a bookshelf format design into bins creating multiple instances of Benchmark class.
- Plotter class: Creates graphical representations of design e.g. Plots the full instance of a design using the matplotlib's pyplot. (Note: depending on the size of the design given as input, might take a while to plot)

# Authors
- **George Kranas** (PlebeianDev) -- [Github](https://github.com/PlebeianDev)

# License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/PlebeianDev/Benchmark-Reader-for-Placement-in-Python/blob/master/LICENSE) file for details.

# Disclaimer
All the information in this repository is provided in good will, for those in need. However I make no representation or warranty of any kind, express or implied, regarding the accuracy, adequacy, validity, reliability, availability or completeness of any information, and I am not accountable for any misuse (of any kind), of the information provided, by third-parties.
