from argparse import ArgumentParser
import sys
from .file_operations import read_config, gen_config
from .misc import greet
from system_operations import restart_nginx

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
                print("Restarting Nginx with 'sudo service nginx restart'")
                print("You can change the restart command below")
                rc = input("Do you want to restart? [Y/N/Command]")
                if rc.upper() == "N":
                    print("Nginx will not be started. Bye.")
                if rc.upper() == "Y":
                    print("Attempting to restart Nginx")
                    if restart_nginx():
                        print("Nginx restarted successfully")
                    else:
                        print("Problem with restarting nginx")
                else:
                    print(f"Attempting to restart Nginx with {rc}")
                    if restart_nginx(rc):
                        print("Nginx restarted successfully")
                    else:
                        print(
                            "Problem with restarting nginx, please restart manually"
                        )

        except KeyboardInterrupt:
            print("\nBye!")
            exit()


if __name__ == "__main__":
    main()
