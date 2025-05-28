def setup_parser(subparser):
    parser = subparser.add_parser('clone',
                                  help='Clone Github Organization repositories')
    parser.add_argument('--gitlab-host',
                        help='Gitlab instance base URL')
    parser.add_argument('--gitlab-group-id',
                        help='Gitlab group ID to clone repositories from')
    parser.add_argument('--gitlab-token',
                        help='Gitlab personal access token')
    parser.add_argument('--target-directory',
                        help='Directory to clone repositories into')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Enable verbosity')

    parser.set_defaults(verbose=False)
    parser.set_defaults(target_directory='.')
    parser.set_defaults(gitlab_host='https://gitlab.com')
    parser.set_defaults(func=execute)


def execute(args):
    from executor.gitlab.clone_executor import CloneExecutor
    parsed_args = {
        "gitlab_host": args.gitlab_host,
        "gitlab_group_id": args.gitlab_group_id,
        "gitlab_token": args.gitlab_token,
        "target_directory": args.target_directory
    }

    executor = CloneExecutor()
    executor.execute(**parsed_args)
