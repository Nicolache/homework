import ast
import collections
import os

from nltk import pos_tag
from vcstools import get_vcs_client

from command_line_arguments import *
from output_format import *
from variables import *


def delete_repos_directories():
    for directory in os.listdir(repos_local_path):
        os.system('rm -rf ' + repos_local_path + '/' + directory)


def repo_clone(https_url, vcs_type):
    reponame = https_url.rsplit('/', 1)[1]
    client = get_vcs_client(vcs_type, repos_local_path + reponame)
    client.checkout(https_url)


def clone_all():
    for url_and_vcstype in repos_to_clone_urls:
        repo_clone(url_and_vcstype[0], url_and_vcstype[1])

def projects_list():
    for directory in os.listdir(repos_local_path):
        yield os.path.join(repos_local_path, directory)


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


def word_belongs_to_parts_of_speech(word, abbreviations):
    logging.debug('word_belongs ' + word)
    logging.debug('abbreviations ' + str(abbreviations))
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] in abbreviations


def get_filenames():
    """Get all *.py files locations inside `Path` location. `Path` is a global variable.

    Returns a generator.
    """
    filenames_counter = 0
    path = Path
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py') and filenames_counter < maxfilenames:
                filenames_counter += 1
                yield os.path.join(dirname, file)


def get_trees(with_filenames=False, with_file_content=False):
    """Generates ast objects, or ast objects in tuple with filenames, and file contents.

    Keyword arguments:
    with_filenames -- `bool`:
        A flag that switches "with filenames" return mode on:
        ((filename, tree), ...)
    with_file_content -- `bool`:
        A flag that switches "with file content" return mode on:
        ((filename, main_file_content, tree), ...)

    Returns a generator.
    """
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


def get_poss_from_name(name, abbreviations):
    """Splits name into words and returns a selected parts of speech.

    Keyword arguments:
    name -- A string that contains a function name, or a variable name, or etc. .
    abbreviations -- Codes of parts of speech in their different forms.

    Returns a generator.
    """
    for word in name.split('_'):
        if word_belongs_to_parts_of_speech(word, abbreviations):
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


def select_names_from_nodes(nodes, search_in):
    """Returns all function, or variable names from all the nodes.

    Keyword arguments:
    nodes -- all the units in programming code tree.

    Returns a generator of function, or variable names from all the nodes.
    """
    if search_in == 'functions':
        names = select_function_names_from_nodes(nodes)
    if search_in == 'variables':
        names = select_variable_names_from_nodes(nodes)
    return names


def select_variable_names_from_nodes(nodes):
    """Extracts from nodes all the variables names in lowercase.

    Keyword arguments:
    nodes -- Nodes of some computer language code.

    Returns a generator.
    """
    for node in nodes:
        if isinstance(node, ast.Name):
            yield node.id.lower()


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


def select_pos_from_names(names_in_lower_case, abbreviations):
    """Generates parts of speech out of functions, variables, etc. names plenty.
    pos is part of speech.

    Keyword arguments:
    names_in_lower_case -- Names of variables, or functions, or etc. in a programming code.
    abbreviations -- Codes of parts of speech in their different forms.

    Returns a generator.
    """
    logging.debug('select_pos_from_names: arg:names_in_lower_case - generator select_function_names_from_nodes')
    parts_of_speech = []
    for name in names_in_lower_case:    
        yield get_poss_from_name(name, abbreviations)


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
    names_in_lower_case = select_names_from_nodes(nodes, args.search_in)
    logging.info('Names extracted.')
    parts_of_speech = select_pos_from_names(names_in_lower_case, abbreviation_sets[args.part])
    unfolded_parts_of_speech = flat(parts_of_speech)
    return collections.Counter(unfolded_parts_of_speech).most_common(top_size)


def main():
    logging.debug(parser)
    logging.debug(args)

    if args.clear:
        delete_repos_directories()
    
    if args.clone:
        clone_all()

    projects = projects_list()
    words = []
    for path in projects:
        words += get_top_verbs_in_path(path)

    console_json_csv_output(words)


if __name__ == "__main__":

    main()
