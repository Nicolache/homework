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


def get_filenames():
    """Get all *.py files locations inside what `Path` global variable contains.

    Returns a generator.
    """
    filenames = []
    path = Path
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py') and len(filenames) < maxfilenames:
                yield os.path.join(dirname, file)


def get_trees(with_filenames=False, with_file_content=False):
    """Generates ast objects, or ast objects in tuple with filenames, and file content.

    Keyword arguments:
    with_filenames -- `bool`:
        A flag that switches "with filenames" return mode on:
        ((filename, tree), ...)
    with_file_content -- `bool`:
        A flag that switches "with file content" return mode on:
        ((filename, main_file_content, tree), ...)

    Returns a generator.
    """
    trees = []
    filenames = get_filenames()
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
    path -- A project path string.
    top_size -- Limiting the max number of words.

    Returns a generator.
    """
    for function_name in function_names_in_lower_case:    
        yield get_verbs_from_function_name(function_name)


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
    function_names_in_lower_case = select_function_names_from_nodes(nodes)
    logging.info('functions extracted')
    lists_of_verbs = select_verbs_from_function_names(function_names_in_lower_case)
    verbs = flat(lists_of_verbs)
    return collections.Counter(verbs).most_common(top_size)
