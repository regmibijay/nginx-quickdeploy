from argparse import ArgumentParser
import sys
from .file_operations import read_config, gen_config
from .misc import greet


def main(argv=sys.argv[1:]):
    print(greet())
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="Input json file for easy installation, currently unsupported",
        nargs="?",
    )
    arg = parser.parse_args()

    if arg.input:
        read_config(arg.i)
    else:
        try:
            res = gen_config()
            if res:
                print()
                print("Your new website was deployed successfully")
                print("Restart nginx to serve it via nginx.")

        except KeyboardInterrupt:
            print("\nBye!")
            exit()


if __name__ == "__main__":
    main()
