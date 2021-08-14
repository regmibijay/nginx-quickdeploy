import subprocess


def restart_nginx(restart_command="sudo service nginx restart"):
    restart_command = restart_command.split(" ")
    try:
        subprocess.check_output(restart_command)
        return True
    except Exception:
        return False
