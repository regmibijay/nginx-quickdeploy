from argparse import ArgumentParser
import sys
from .file_operations import handle_config, read_config, gen_config
from .misc import greet, adios
from .system_operations import certbot_handler, restart_handler


def main(argv=sys.argv[1:]):
    print(greet())
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="Input json file for easy installation",
        nargs="?",
    )
    arg = parser.parse_args()

    if arg.input:
        print()
        print(f"Reading from {arg.input}")
        config = read_config(arg.input)
        url, res = handle_config(data=config)
        if res:
            cert_status = certbot_handler(url)
            if cert_status == "no_cert":
                print("You chose not to install certs.")
            elif cert_status:
                print("Successfully installed SSL Certs")
            else:
                print("Certbot encountered problem while acquiring certs.")
                print("Try again later.")
            print()
            restart_handler()
            print(adios())
        else:
            print(
                f"Something went wrong reading {arg.input}, please try again."
            )
    else:
        try:
            url, res = gen_config()
            if res:
                print()
                print("Your new website was deployed successfully")
                print()
                cert_status = certbot_handler(url)
                if cert_status == "no_cert":
                    print("You chose not to install certs.")
                elif cert_status:
                    print("Successfully installed SSL Certs")
                else:
                    print("Certbot encountered problem while acquiring certs.")
                    print("Try again later.")
                print()
                restart_handler()
                print(adios())

        except KeyboardInterrupt:
            print("\n")
            print(adios())
            exit()


if __name__ == "__main__":
    main()
