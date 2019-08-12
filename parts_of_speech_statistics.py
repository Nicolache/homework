import ast
import collections
import logging
import os

from nltk import pos_tag


MAXFILENAMES = 100
LOG_PATH_NAME = './logs.log'
LOGLEVEL = logging.INFO
# LOGLEVEL = logging.DEBUG
logger = logging.getLogger("")
logger.setLevel(LOGLEVEL)
logging.basicConfig(
    filename=LOG_PATH_NAME,
    level=LOGLEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


def flat(folded_generator_with_verbs):
    """Generating verbs with folded generators
        ((1,2), (3,4)) -> (1, 2, 3, 4)

    Keyword arguments:
    folded_generator_with_verbs -- generator of generators.

    Returns a generator.
    """
    for item in folded_generator_with_verbs:
        for folded_item in item:
            yield folded_item


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


def get_filenames(path):
    """Get all *.py files locations inside `path` location.

    path -- A path string.

    Returns a generator.
    """
    filenames_counter = 0
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py') and filenames_counter < MAXFILENAMES:
                filenames_counter += 1
                yield os.path.join(dirname, file)


def get_trees(path, with_filenames=False, with_file_content=False):
    """Generates ast objects, or ast objects in tuple with filenames, and file contents.

    Keyword arguments:
    path -- A path string.
    with_filenames -- `bool`:
        A flag that switches "with filenames" return mode on:
        ((filename, tree), ...)
    with_file_content -- `bool`:
        A flag that switches "with file content" return mode on:
        ((filename, main_file_content, tree), ...)

    Returns a generator.
    """
    filenames = get_filenames(path)
    filenames_counter = 0
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
            filenames_counter += 1
        except SyntaxError as e:
            logging.warning(e)
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

    Returns a generator.
    """
    for word in function_name.split('_'):
        if is_verb(word):
            yield word


def generate_nodes_out_of_trees(trees):
    """Return all nodes of code.

    Keyword arguments:
    trees -- Trees of some computer language code.

    Returns a generator.
    """
    for tree in trees:
        for node in ast.walk(tree):
            yield node


def select_function_names_from_nodes(nodes):
    """Extracts from nodes all the function names in lowercase.

    Keyword arguments:
    nodes -- Nodes of some computer language code.

    Returns a generator.
    """
    for node in nodes:            
        if isinstance(node, ast.FunctionDef) and\
            not (node.name.lower().startswith('__') and
            node.name.lower().endswith('__')):
                yield node.name.lower()


def select_verbs_from_function_names(function_names_in_lower_case):
    """Generates verbs out of function names plenty.

    Keyword arguments:
    function_names_in_lower_case -- Names plenty.

    Returns a generator.
    """
    for function_name in function_names_in_lower_case:    
        yield get_verbs_from_function_name(function_name)


def get_top_verbs_in_path(path, top_size=10):
    """Return litst of tuples with words and its occurrence.

    Keyword arguments:
    path -- A path string.
    top_size -- Limiting the max number of words.

    The return type is `list`.
    """
    nodes = generate_nodes_out_of_trees(get_trees(path))
    function_names_in_lower_case = select_function_names_from_nodes(nodes)
    logging.info('functions extracted')
    lists_of_verbs = select_verbs_from_function_names(function_names_in_lower_case)
    verbs = flat(lists_of_verbs)
    return collections.Counter(verbs).most_common(top_size)


def get_top_verbs_in_projects(projects):
    """Return litst of tuples with words and their occurrence.

    Keyword arguments:
    projects -- list of path strings.

    The return type is `list`.
    """
    words = []
    for project in projects:
        path = os.path.join('.', project)
        words += get_top_verbs_in_path(path)
    return words


def report_into_log(words, top_size=200):
    """Writes a formatted report into log.

    Keyword arguments:
    words -- list of tuples: (wordname, quantity)
    top_size -- Limiting the max number of words.
    """
    logging.info('total %s words, %s unique' % (len(words), len(set(words))))
    for word, occurence in collections.Counter(words).most_common(top_size):
        logging.info('{}, {}'.format(word, occurence))
