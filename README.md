# A homework
This is a homework to check.
This is executable in Python3 .
Tested in Python 3.5.X, 3.6.8 .
This script makes some function names, or variable names statistics in given projects. It uses "ast" module to walk the code tree, and "nltk" module to distinguish between parts of speech. You can add some python project directory inside the cloned from git "homework" directory, and launch it the way below:
## An example of using the script. ##

    import collections
    import os
    from parts_of_speech_statistics import *
    
    
    wds = []
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]
    
    
    for project in projects:
        path = os.path.join('.', project)
        wds += get_top_verbs_in_path(path)
    
    
    top_size = 200
    print('total %s words, %s unique' % (len(wds), len(set(wds))))
    for word, occurence in collections.Counter(wds).most_common(top_size):
        print(word, occurence)
