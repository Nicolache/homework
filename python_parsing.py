import ast
import os
from variables import logging, MAXFILENAMES


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
    """Generates ast objects, or ast objects in tuple
    with filenames, and file contents.

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


def select_variable_names_from_nodes(nodes):
    """Extracts from nodes all the variables names in lowercase.

    Keyword arguments:
    nodes -- Nodes of some computer language code.

    Returns a generator.
    """
    for node in nodes:
        if isinstance(node, ast.Name):
            yield node.id.lower()
