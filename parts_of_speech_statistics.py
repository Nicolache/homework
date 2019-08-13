import collections
import os

from nltk import pos_tag
from vcstools import get_vcs_client

from command_line_arguments import args
from output_format import console_json_csv_output
from python_parsing import\
    get_trees,\
    generate_nodes_out_of_trees,\
    select_variable_names_from_nodes,\
    select_function_names_from_nodes
from variables import repos_local_path, logging, abbreviation_sets


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


def flat(folded_generator_with_pos):
    """Generating parts of speech with the help of folded generators
        ((1,2), (3,4)) -> (1, 2, 3, 4)

    Keyword arguments:
    folded_generator_with_pos -- A folded generator with parts of speech.
    It's a generator of generators.

    Returns a generator.
    """
    for item in folded_generator_with_pos:
        for folded_item in item:
            yield folded_item


def word_belongs_to_parts_of_speech(word, abbreviations):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] in abbreviations


def get_poss_from_name(name, abbreviations):
    """Splits name into words and returns a selected parts of speech.

    Keyword arguments:
    name -- A string that contains a function name,
    or a variable name, or etc. .
    abbreviations -- Codes of parts of speech in their different forms.

    Returns a generator.
    """
    for word in name.split('_'):
        if word_belongs_to_parts_of_speech(word, abbreviations):
            yield word


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


def select_pos_from_names(names_in_lower_case, abbreviations):
    """Generates parts of speech out of functions, variables, etc. names plenty.
    pos is part of speech.

    Keyword arguments:
    names_in_lower_case -- Names of variables, or functions,
    or etc. in a programming code.
    abbreviations -- Codes of parts of speech in their different forms.

    Returns a generator.
    """
    parts_of_speech = []
    for name in names_in_lower_case:
        yield get_poss_from_name(name, abbreviations)


def get_top_pos_in_path(path, top_size=10):
    """Get top parts of speech located in `path` paramerer.
    Return litst of tuples with words and its occurrence.

    Keyword arguments:
    path -- A path string.
    top_size -- Limiting the max number of words.

    The return type is `list`.
    """
    nodes = generate_nodes_out_of_trees(get_trees(path))
    names_in_lower_case = select_names_from_nodes(nodes, args.search_in)
    logging.info('Names extracted.')
    parts_of_speech = select_pos_from_names(
        names_in_lower_case,
        abbreviation_sets[args.part]
    )
    unfolded_parts_of_speech = flat(parts_of_speech)
    return collections.Counter(unfolded_parts_of_speech).most_common(top_size)


def get_top_pos_in_projects(projects):
    """Return litst of tuples with words and their occurrence.

    Keyword arguments:
    projects -- list of path strings.

    The return type is `list`.
    """
    words = []
    for project in projects:
        path = os.path.join('.', project)
        words += get_top_pos_in_path(path)
    return words


def main():
    logging.debug(args)

    if args.clear:
        delete_repos_directories()

    if args.clone:
        clone_all()

    projects = projects_list()
    words = get_top_pos_in_projects(projects)
    console_json_csv_output(words)


if __name__ == "__main__":

    main()
