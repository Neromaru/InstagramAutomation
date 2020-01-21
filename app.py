from argparse import ArgumentParser
from instagram_upload import InstagramUploader


def cli():
    parser = ArgumentParser()
    parser.add_argument('--username', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    parser.add_argument('--file', type=str, required=True)
    args = parser.parse_args()
    return args.username, args.password, args.file


def main():
    username, password, file = cli()
    uploader = InstagramUploader(username, password, file)
    uploader.run()


if __name__ == '__main__':
    main()
