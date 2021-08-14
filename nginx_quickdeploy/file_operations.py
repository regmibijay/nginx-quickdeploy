# handles all the file operations
import os
from .validation import is_valid_hostname


def read_config(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except OSError:
        print(f"Specified config file {path} could not be read, please make")
        print("sure you have rights to read the file.")
        exit()
    except FileNotFoundError:
        print(f"Specified config file {path} could not be found, please make")
        print("sure you have specified the right path")
        exit()
    except Exception:
        print("There was a problem reading the config file")
        exit()


def gen_config():
    # handling server name
    URL = input(
        "FQDN of your domain, e.g. example.com or subdomain.example.com without http or https:  "
    )
    if URL == "":
        print("URL can not be empty")
        gen_config()
    if not is_valid_hostname(URL):
        print(f"{URL} does not seem to be a valid hostname.")
        gen_config()

    # config path
    PATH = input(
        f"Where should the new config file be saved?, default is /etc/nginx/sites-available/{URL} :  "
    )
    if PATH == "":
        PATH = "/etc/nginx/sites-available/" + URL

    # handling ports
    print(
        "Ports separated by commas(,) in nginx fashion, like 80, [::]:80 etc"
        + os.linesep,
        "For ssl, just add ssl after the port, e.g. 80, 443 ssl, [::]:80, [::]:443 ssl",
        sep="",
    )
    PORT = input("Enter ports here: ")
    if PORT == "":
        PORT = "80"
    PORT = PORT.split(",")

    # root folder
    ROOT = input("Enter the www root path(default /var/www/html):  ")
    if ROOT == "":
        ROOT = "/var/www/html"

    # proxy pass
    PROXY = input("Should this server need to proxy_pass, enter the address here:  ")
    if PROXY == "":
        PROXY = False

    CONFIG = config_lines(url=URL, ports=PORT, root=ROOT, proxy=PROXY)
    return write_config(path=PATH, data=CONFIG)


def config_lines(url, ports, root, proxy=False):
    head = ["server {"]
    head.append(f"  root {root};")
    head.append(f"  server_name {url};")
    for port in ports:
        if not port == "":
            head.append(f"  listen {port};")
    head.append("   location / {")
    head.append("       try_files $uri $uri/;")
    if proxy:
        head.append(f"      proxy_pass {proxy};")
    head.append("   }")
    head.append("}")
    return head


def write_config(path, data: list):
    data = [line + "\n" for line in data]
    try:
        with open(path, "w") as f:
            f.writelines(data)
        return True
    except OSError:
        print(f"Specified config file {path} could not be written, please make")
        print("sure you have rights to read the file.")
        print(*data, sep="\r\n")
        exit()
    except Exception:
        print("There was a problem writing the config file")
        print(*data, sep=os.linesep)
        exit()
