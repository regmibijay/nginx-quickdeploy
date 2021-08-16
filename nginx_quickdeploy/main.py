import sys
from argparse import ArgumentParser

from .file_operations import gen_config, handle_config, read_config
from .misc import adios, greet
from .system_operations import certbot_handler, restart_handler
from .validation import validate_args


def main(argv=sys.argv[1:]):
    print(greet())
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="Input json file for easy installation",
        nargs="?",
    )
    parser.add_argument("-d", "--domain", help="Domain you want to set up.", nargs="?")
    parser.add_argument("-p", "--path", help="Config file path", nargs="?")
    parser.add_argument("--ports", help="Ports to listen to separated by comma(,)", nargs="?")
    parser.add_argument("-w", "--webroot", help="Webroot folder containing index.html", nargs="?")
    parser.add_argument("-f", "--forward", help="Proxy pass URL", nargs="?")
    parser.add_argument("--ssl_cert_path", help="SSL certificate path", nargs="?")
    parser.add_argument("--ssl_key_path", help="SSL key path", nargs="?")
    arg = parser.parse_args()
    if arg.domain:
        if arg.input:
            print()
            print("You specified a json file and gave in CLI params")
            print("Specify the params either via config file or via CLI.")
            print(adios(message="         Script ended abnormally                 "))
            exit()
        print()
        print(f"Processing {arg.domain}")
        url, res = validate_args(arg)
        if res:
            cert_acquire_and_restart(url)
        else:
            print(f"Something went wrong reading {arg.input}, please try again.")

    if arg.input:
        print()
        print(f"Reading from {arg.input}")
        config = read_config(arg.input)
        url, res = handle_config(data=config)
        if res:
            print(f"Succesfully deployed {url}")
            cert_acquire_and_restart(url)
        else:
            print(f"Something went wrong reading {arg.input}, please try again.")
    else:
        try:
            url, res = gen_config()
            if res:
                print()
                print("Your new website was deployed successfully")
                print()
                cert_acquire_and_restart(url)

        except KeyboardInterrupt:
            print("\n")
            print(adios(message="                   Bye                           "))
            exit()


def cert_acquire_and_restart(url):
    try:
        cert_status = certbot_handler(url)
    except KeyboardInterrupt:
        print("\n")
        print(adios(message="                   Bye                           "))
        exit()
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
    exit()


if __name__ == "__main__":
    main()
