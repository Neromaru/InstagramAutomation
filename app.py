from argparse import ArgumentParser
from instagram_upload import InstagraUploader


def cli():
    parser = ArgumentParser()
    parser.add_argument('--username', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    # parser.add_argument('--file', type=str, required=True)
    args = parser.parse_args()
    return args.username, args.password


def main():
    username, password = cli()
    uploader = InstagraUploader(username, password)
    uploader._run()

if __name__ == '__main__':
    main()
