import subprocess


def restart_nginx(restart_command="sudo service nginx restart"):
    restart_command = restart_command.split(" ")
    try:
        subprocess.check_output(restart_command)
        return True
    except Exception:
        return False


def restart_handler():
    print("Restarting Nginx with 'sudo service nginx restart'")
    print("You can change the restart command below")
    rc = input("Do you want to restart? [Y/N/Command]:  ")
    if rc.upper() == "N":
        print("Nginx will not be started. Bye.")
    elif rc.upper() == "Y":
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


def certbot_handler(domain):
    print()
    res = input(f"Do you want to acquire Letsencrypt certs for the webserver {domain}? [y/n]:  ")
    if res.upper() == "Y":
        if get_cert_letsencrypt(domain=domain):
            return True
        else:
            return False
    else:
        print("Affirmative, no certs will be acquired.")
        return "no_cert"


def get_cert_letsencrypt(domain):
    try:
        subprocess.check_output(["sudo", "certbot", "--nginx", "--force-renewal", "--redirect", "--domains", f"{domain}"])
        return True
    except Exception as e:
        print(str(e))
        return False
