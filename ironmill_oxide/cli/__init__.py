import requests
from colorama import Fore, Style
from ironmill_oxide.error import OxideError
import ironmill_oxide.cli.get_parser as get_parser
import ironmill_oxide.cli.commands as commands

def main():
    parser = get_parser.main()
    args = parser.parse_args()
    try:
        if args.command == 'init':
            commands.init.main()

        elif args.command == 'add':
            commands.add.main(args.name)

        elif args.command == 'rm':
            commands.rm.main(args.name)

        elif args.command == 'search':
            commands.search.main(args.search_term)

        elif args.command == 'install':
            commands.install.main(not args.no_verify)

        elif args.command == 'publish':
            commands.publish.main(args.filepath)
        
    except OxideError as e:
        parser.error(f'{Fore.RED}{e}{Style.RESET_ALL}')

    except requests.exceptions.ConnectionError as e:
        parser.error(f'{Fore.RED}Connection error:\n{e}{Style.RESET_ALL}')
