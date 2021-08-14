# handles all the file operations
import os
import json
from typing import DefaultDict
from .validation import is_valid_hostname


def read_config(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except OSError:
        print(f"Specified config file {path} could not be read, please make")
        print("sure you have rights to read the file.")
        exit()
    except FileNotFoundError:
        print(f"Specified config file {path} could not be found, please make")
        print("sure you have specified the right path")
        exit()
    except Exception as e:
        print("There was a problem reading the config file")
        print(str(e))
        exit()


def gen_config():
    # handling server name
    URL = input(
        "FQDN of your domain, e.g. example.com or subdomain.example.com without http or https:  "
    )
    if URL == "":
        print("URL can not be empty")
        gen_config()
    while not is_valid_hostname(URL):
        print(f"{URL} does not seem to be a valid hostname.")
        URL = input(
            "FQDN of your domain, e.g. example.com or subdomain.example.com without http or https:  "
        )

    # config path
    print()
    PATH = input(
        f"Where should the new config file be saved?, default is /etc/nginx/sites-available/{URL} :  "
    )
    if PATH == "":
        PATH = "/etc/nginx/sites-available/" + URL

    # handling ports
    print()
    print(
        "Ports separated by commas(,) in nginx fashion, like 80, [::]:80 etc"
        + os.linesep,
        "For ssl, just add ssl after the port, e.g. 80, 443 ssl, [::]:80, [::]:443 ssl",
        sep="",
    )
    PORT = input("Enter ports here: ")
    if PORT == "":
        PORT = "80; [::]:80"
    PORT = PORT.split(",")

    # root folder
    print()
    ROOT = input(f"Enter the www root path(default /var/www/html/{URL}):  ")
    if ROOT == "":
        ROOT = f"/var/www/html{URL}"

    # proxy pass
    print()
    PROXY = input("Proxy address, leave empty to unset:  ")
    if PROXY == "":
        PROXY = False

    CONFIG = config_lines(url=URL, ports=PORT, root=ROOT, proxy=PROXY)
    return URL, write_config(path=PATH, data=CONFIG)


def config_lines(url, ports, root, proxy=False, ssl_cert_path=False, ssl_key_path=False):
    head = ["server {"]
    head.append(f"  root {root};")
    head.append("  index index.html index.htm index.nginx-debian.html;")
    head.append(f"  server_name {url};")
    for port in ports:
        if not port == "":
            head.append(f"  listen {port};")
        if "ssl" in port and ssl_cert_path is False or "ssl" in port and ssl_key_path is False:
            print(f"You have ssl enabled on {port}")
            ssl_cert_path = input(f"Enter ssl cert path(default /etc/letsencrypt/live/{url}/fullchain.pem):  ")
            if ssl_cert_path == "":
                ssl_cert_path = f"/etc/letsencrypt/live/{url}/fullchain.pem"
            if not os.path.isfile(ssl_cert_path):
                print(f"{ssl_cert_path} does not seem to exist.")
                while not os.path.isfile(ssl_cert_path):
                    ssl_cert_path = input("Enter ssl cert path:  ")

            ssl_key_path = input(f"Enter ssl cert path(default /etc/letsencrypt/live/{url}/privkey.pem):  ")
            if ssl_key_path == "":
                ssl_key_path = "/etc/letsencrypt/live/{url}/privkey.pem"
            if not os.path.isfile(ssl_key_path):
                print(f"{ssl_key_path} does not seem to exist.")
                while not os.path.isfile(ssl_key_path):
                    ssl_key_path = input("Enter ssl cert path:  ")

    if ssl_cert_path and ssl_key_path:
        head.append(f"  ssl_certificate {ssl_cert_path};")
        head.append(f"  ssl_certificate_key {ssl_key_path};")
    head.append("  location / {")
    if proxy:
        head.append(f"    proxy_pass {proxy};")
    if not proxy:
        head.append("    try_files $uri $uri/ =404;")
    head.append("  }")
    head.append("}")
    return head


def write_config(path, data: list):
    # data = [line  for line in data]
    try:
        with open(path, "w") as f:
            f.writelines(data)
        return True
    except OSError:
        print()
        print(f"Specified config file {path} could not be written, please make")
        print("sure you have rights to read the file.")
        print()
        print(*data, sep="\r\n")
        exit()
    except Exception as e:
        print()
        print("There was a problem writing the config file")
        print(str(e))
        print()
        print(*data, sep=os.linesep)
        exit()


def handle_config(data: dict):
    stan_data = standard_config()
    for key in data.keys():
        try:
            stan_data[key] = data[key]
        except KeyError:
            print(f"Unknown key {key} found. Please refer to our documentation")
    
    data = stan_data
    mandatory_fields = ["url"]
    if not all([x for x in mandatory_fields if x in data]):
        return False
    URL = data["url"]
    PATH = data["path"] if data["path"] else f"/etc/nginx/sites-available/{URL}"
    PORTS = data["ports"] if data["ports"] else ["80", "[::]:80"]
    ROOT = data["root"] if data["root"] else f"/var/www/html/{URL}"
    PROXY = data["proxy"] if data["proxy"] else False
    SSL_CERT = data["ssl_cert_path"] if data["ssl_cert_path"] else False
    SSL_KEY = data["ssl_key_path"] if data["ssl_key_path"] else False
    CONFIG = config_lines(
        url=URL,
        ports=PORTS,
        root=ROOT,
        proxy=PROXY,
        ssl_cert_path=SSL_CERT,
        ssl_key_path=SSL_KEY
    )
    return URL, write_config(path=PATH, data=CONFIG)


def standard_config():
    return {
        "url": False,
        "path": False,
        "ports": False,
        "root": False,
        "proxy": False,
        "ssl_cert_path": False,
        "ssl_key_path": False,
    }