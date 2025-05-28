def setup_parser(subparser):
    parser = subparser.add_parser('clone',
                                  help='Clone Github Organization repositories')
    parser.add_argument('--github-organization',
                        help='Github organization to clone repositories from')
    parser.add_argument('--github-token',
                        help='Github personal access token')
    parser.add_argument('--target-directory',
                        help='Directory to clone repositories into')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Enable verbosity')

    parser.set_defaults(verbose=False)
    parser.set_defaults(target_directory='.')
    parser.set_defaults(func=execute)


def execute(args):
    from executor.github.clone_executor import CloneExecutor
    parsed_args = {
        "github_organization": args.github_organization,
        "github_token": args.github_token,
        "target_directory": args.target_directory
    }

    executor = CloneExecutor()
    executor.execute(**parsed_args)
