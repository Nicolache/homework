# A homework
This is a homework to check.
This is executable in Python 3.5.X - 3.7.X
This script makes some functions words statistics in given projects. It uses "ast" module to walk the code tree, and "nltk" module to distinguish between parts of speech. You can add some python project directory inside the cloned from git "homework" directory, and launch it the way below:
## An example of using the script. ##

    from parts_of_speech_statistics import get_top_verbs_in_projects, report_into_log
      
    words = get_top_verbs_in_projects(['django', 'flask', 'pyramid', 'reddit', 'requests', 'sqlalchemy'])
    report_into_log(words)
