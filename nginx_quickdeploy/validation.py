import re


def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


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


def validate_args(arg):
    from .file_operations import config_lines, write_config

    stan_data = standard_config()
    URL = arg.domain
    stan_data["url"] = arg.domain
    stan_data["path"] = arg.path if arg.path else f"/etc/nginx/sites-available/{arg.domain}"
    stan_data["ports"] = arg.ports.split(",") if arg.ports else ["80", "[::]:80"]
    stan_data["root"] = arg.webroot if arg.webroot else f"/var/www/html/{URL}"
    stan_data["proxy"] = arg.forward if arg.forward else False
    stan_data["ssl_cert_path"] = arg.ssl_cert_path if arg.ssl_cert_path else False
    stan_data["ssl_key_path"] = arg.ssl_key_path if arg.ssl_key_path else False
    CONFIG = config_lines(
        url=stan_data["url"],
        ports=stan_data["ports"],
        root=stan_data["root"],
        proxy=stan_data["proxy"],
        ssl_cert_path=stan_data["ssl_cert_path"],
        ssl_key_path=stan_data["ssl_key_path"],
    )
    return URL, write_config(path=stan_data["path"], data=CONFIG)
