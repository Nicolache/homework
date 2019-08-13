# A homework
This is a homework to check.
This is executable in Python3 .
Tested in Python 3.5.2, 3.6.8 .
This script makes some function names, or variable names statistics in given projects. It uses "ast" module to walk the code tree, and "nltk" module to distinguish between parts of speech. You can add some python project directory inside the cloned from git "homework" directory, and launch it the way below:
## An example of using the script. ##

    from parts_of_speech_statistics import get_top_verbs_in_projects, report_into_log
      
    words = get_top_verbs_in_projects(['django', 'flask', 'pyramid', 'reddit', 'requests', 'sqlalchemy'])
    report_into_log(words)
