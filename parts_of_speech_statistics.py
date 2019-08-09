import ast
import collections
import logging
import os

from nltk import pos_tag


maxfilenames = 100
Path = ''
log_path_name = './logs.log'
loglevel = logging.INFO
# loglevel = logging.DEBUG
logger = logging.getLogger("")
logger.setLevel(loglevel)
logging.basicConfig(
    filename=log_path_name,
    level=loglevel,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


def flat(_list):
    """Convert list of lists into 1 dimentional list.
        [[1,2], [3,4]] -> [1, 2, 3, 4]

    Keyword arguments:
    _list -- list of lists

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

    The return is a generator.
    """
    filenames = []
    path = Path
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py') and len(filenames) < maxfilenames:
                yield os.path.join(dirname, file)


def get_trees(with_filenames=False, with_file_content=False):
    """Return list of ast objects.

    Keyword arguments:
    with_filenames -- `bool`:
        A flag that switches the list of tuples mode on in return:
        [(filename, tree), ...]
    with_file_content -- `bool`:
        A flag that switches the list of tuples mode on in return:
        [(filename, main_file_content, tree), ...]

    The return is a generator.
    """
    trees = []
    filenames = get_filenames()
    # logging.info('total %s files' % len(filenames))
    filenames_counter = 0
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
            filenames_counter += 1
        except SyntaxError as e:
            logging.info(e)
            tree = None
        if not with_filenames:
            yield tree
        if with_filenames and not with_filenames:
            yield (filename, tree)
        if with_filenames and with_file_content:
            yield (filename, main_file_content, tree)
    logging.info('Total {} files'.format(filenames_counter))
    logging.info('trees generated')


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


def generate_nodes_out_of_trees(trees):
    """Return all nodes from code.

    Keyword arguments:
    trees -- Trees with some computer language code.

    The return is a generator.
    """
    for tree in trees:
        for node in ast.walk(tree):
            yield node


def get_top_verbs_in_path(path, top_size=10):
    """Return litst of tuples with words and its occurrence.

    Keyword arguments:
    path -- A project path string.
    top_size -- Limiting the max number of words.

    The return type is `list`.
    """
    global Path
    Path = path
    nodes = generate_nodes_out_of_trees(get_trees())
    fncs = []
    for node in nodes:
        if isinstance(node, ast.FunctionDef) and\
            not (node.name.lower().startswith('__') and
            node.name.lower().endswith('__')):
                fncs.append(node.name.lower())
    logging.info('functions extracted')
    lists_of_verbs = []
    for function_name in fncs:
        lists_of_verbs.append(get_verbs_from_function_name(function_name))
    verbs = flat(lists_of_verbs)
    logging.debug(lists_of_verbs)
    return collections.Counter(verbs).most_common(top_size)
