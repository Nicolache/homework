import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    '--clear',
    '--clear-local-repos-directory',
    action='store_true',
    help='It removes all the directories \
        inside repos_local_path\
        on start.',
)
parser.add_argument(
    '-c',
    '--clone',
    action='store_true',
    help='It clones all from repos_to_clone_urls.',
)
parser.add_argument(
    '-r',
    '--report_format',
    choices=['console', 'json', 'csv'],
    default='console',
    help="A report format choise.",
)
parser.add_argument(
    '-o',
    '--output',
    action='store',
    type=str,
    help="Redirect output to a file.",
)
parser.add_argument(
    '-s',
    '--search_in',
    choices=['functions', 'variables'],
    default='functions',
    help="Search parts of speech in functions names,\
        or variables names. Functions is default.",
)
parser.add_argument(
    '-p',
    '--part',
    choices=['verbs', 'nouns'],
    default='verbs',
    help="A part of speech. A choice between nouns,\
        and verbs statistics. Verbs is default.",
)
args = parser.parse_args()
