# homework
Homework to check.
This script makes some functions words statistics in given projects.
## Heading 2 ##

    Markup :  ## Heading 2 ##

    -OR-

    Markup: --------------- (below H2 text)

import collections
import os
# import parts_of_speech_statistics
# from parts_of_speech_statistics import get_top_verbs_in_path
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
