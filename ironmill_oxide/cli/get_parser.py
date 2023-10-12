import argparse
import importlib.metadata

from ironmill_oxide.util import is_valid_circom

# NOTE Name must match this package's name
__version__ = importlib.metadata.version('ironmill-oxide')

# Create the parser
parser = argparse.ArgumentParser(description='Manage circuits')
parser.add_argument('-v', '--version', action='version', version=__version__)

# Add and document each subcommand
subparsers = parser.add_subparsers(help='sub-command help', dest='command')

""" Add """
parser_add = subparsers.add_parser('add', help='Add the <name> circuit to your manifest')
parser_add.add_argument('name', type=str, help='The name of the circuit')

""" Remove """
parser_remove = subparsers.add_parser('rm', help='Remove the <name> circuit from your manifest')
parser_remove.add_argument('name', type=str, help='The name of the circuit')

""" Init """
parser_init = subparsers.add_parser('init', help='Create a new circuits manifest')

""" Install """
parser_install = subparsers.add_parser('install', help='Install all circuits listed in your manifest')
parser_install.add_argument('-nv', '--no_verify', action='store_true', help="Skip verification of any local or new bundle hashes")

""" Search """
parser_search = subparsers.add_parser('search', help='Search the registry for any circuits that match <search_term>')
parser_search.add_argument('search_term', type=str, help='The term to search')

""" Publish """
parser_publish = subparsers.add_parser('publish', help='Publish a circuit to have it bundled and available with fields from user input')
parser_publish.add_argument('filepath', type=lambda x: is_valid_circom(parser, x), help='Path to the .circom circuit file')


# TODO compile, update, audit, doc
""" Update """
# parser_update = subparsers.add_parser('update', help='Update the lock-file to any changes to the manifest')


def main():
    return parser
