# A homework
This is a homework to check.
This is executable in Python3 .
Tested in Python 3.5.2, 3.6.8 .
This script makes some function names, or variable names statistics in given projects. It uses "ast" module to walk the code tree, and "nltk" module to distinguish between parts of speech. You can add some python project directory inside the cloned from git "homework" directory, and launch it the way below:
## An example of using the script. ##

    from parts_of_speech_statistics import get_top_pos_in_projects
    from output_format import console_json_csv_output
      
    words = get_top_pos_in_projects(['django', 'flask', 'pyramid', 'reddit', 'requests', 'sqlalchemy'])
    console_json_csv_output(words)
## Python files meaning. ##
**command_line_arguments.py** -- Arguments keys names are defined in this file. Each key has its help line. You can watch help with the **python3 parts_of_speech_statistics.py -h** command as well.  
**output_format.py** -- A part of code that is responsible for different output formats such as json, csv, etc.  
**parts_of_speech_statistics.py** -- The core of the logic. It contains main functions.  
**python_parsing.py** -- A module that is devoted to python language code parsing. Any other language parsing could be applied in a similar module in future.  
**variables.py** -- All variables definitions including logging.  
