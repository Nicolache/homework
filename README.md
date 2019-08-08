# homework
Homework to check.
This script makes some functions words statistics in given projects.
## An example of using or the script. ##

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
