import argparse
import importlib
import os
import pkgutil
import sys

from typing import List


def load_subcommands(subparsers, package_name):
    """
    Dynamically load all command modules and subcommands from a given package.
    :param subparsers:
    :param package_name:
    :return:
    """
    package = importlib.import_module(package_name)
    package_dir = os.path.dirname(package.__file__)

    for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
        if is_pkg:
            # Recursively load subcommands
            load_subcommands(subparsers, f"{package_name}.{module_name}")
        else:
            module = importlib.import_module(f"{package_name}.{module_name}")
            if hasattr(module, 'setup_parser'):
                module.setup_parser(subparsers)


def verify_and_print_subcommand_help(subcommands: List[str],
                                     commands: List[any],
                                     parsers: List[any],
                                     args):
    for subcommand, command, parser in zip(subcommands, commands, parsers):
        if args.subcommand == subcommand and command is None:
            parser.print_help()
            sys.exit(0)


def main():
    parser = argparse.ArgumentParser(prog="cloner",
                                     description="Command-Line Interface to manage gitlab or github repositories.")
    parser.add_argument('-v', '--version',
                        action="store_true",
                        help="Display cli version")
    subparsers = parser.add_subparsers(dest="subcommand")

    # Load GitLab subcommands
    github_parser = subparsers.add_parser('github', help="Github related commands")
    github_subparsers = github_parser.add_subparsers(dest="github_command")
    load_subcommands(github_subparsers, 'argparser.github')

    # Load GitLab subcommands
    gitlab_parser = subparsers.add_parser('gitlab', help="GitLab related commands")
    gitlab_subparsers = gitlab_parser.add_subparsers(dest="gitlab_command")
    load_subcommands(gitlab_subparsers, 'argparser.gitlab')

    args = parser.parse_args()

    verify_and_print_subcommand_help(subcommands=['github',
                                                  'gitlab'],
                                     commands=[args.github_command if 'github_command' in args else None,
                                               args.gitlab_command if 'gitlab_command' in args else None],
                                     parsers=[github_parser,
                                              gitlab_parser],
                                     args=args)

    # Call the corresponding function if available
    if hasattr(args, 'func'):
        args.func(args)
    elif args.version:
        import __version__
        print(f"cloner version {__version__.version}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
