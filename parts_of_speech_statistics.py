import ast
import collections
import logging
import os

from nltk import pos_tag


maxfilenames = 100
Path = ''
log_path_name = './logs.log'
loglevel = logging.INFO
#loglevel = logging.DEBUG
logger = logging.getLogger("")
logger.setLevel(loglevel)
logging.basicConfig(filename = log_path_name, level = loglevel, format = '%(asctime)s - %(levelname)s - %(message)s')


def flat(_list):
    """Convert list of tuples into 1 dimentional list.\
        [(1,2), (3,4)] -> [1, 2, 3, 4]

    Keyword arguments:
    _list -- list of tuples

    The return type is `list`.
    """
    flat_list = []
    for item in _list:
        flat_list = flat_list + list(item)
    return flat_list


def is_verb(word):
    """Check if a string is a verb.

    Keyword arguments:
    word -- A string that is checked.

    The return type is `bool`.
    """
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def get_filenames():
    """Get all *.py files locations inside what `Path` global variable contains.

    The return type is `list`.
    """
    filenames = []
    path = Path
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                filenames.append(os.path.join(dirname, file))
                if len(filenames) == maxfilenames:
                    break
    return filenames


def get_trees(with_filenames=False, with_file_content=False):
    """Return list of ast objects.

    Keyword arguments:
    with_filenames -- `bool`:\
        A flag that switches the list of tuples mode on in return:\
        [(filename, tree), ...]
    with_file_content -- `bool`:\
        A flag that switches the list of tuples mode on in return:\
        [(filename, main_file_content, tree), ...]

    The return type is `list`.
    """
    trees = []
    filenames = get_filenames()
    logging.info('total %s files' % len(filenames))
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            logging.info(e)
            tree = None
        if with_filenames:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
    logging.info('trees generated')
    return trees


def get_verbs_from_function_name(function_name):
    """Split function name into words and return verbs.

    Keyword arguments:
    function_name -- A string that contains a function name.

    The return type is `list`.
    """
    verbs = []
    for word in function_name.split('_'):
        if is_verb(word):
            verbs.append(word)
    return verbs


def get_top_verbs_in_path(path, top_size=10):
    """Return litst of tuples with words and its occurrence.

    Keyword arguments:
    path -- A project path string.
    top_size -- Limiting the max number of words.

    The return type is `list`.
    """
    global Path
    Path = path
    trees = get_trees()
    fncs = []
    for t in trees:
        for node in ast.walk(t):
            if isinstance(node, ast.FunctionDef):
                fnc_name = node.name.lower()
                if not (fnc_name.startswith('__') and fnc_name.endswith('__')):
                    fncs.append(fnc_name)
    logging.info('functions extracted')
    v = []
    for function_name in fncs:
        v.append(get_verbs_from_function_name(function_name))
    verbs = flat(v)
    return collections.Counter(verbs).most_common(top_size)
