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
