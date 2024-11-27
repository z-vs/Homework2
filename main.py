import subprocess
import configparser


def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def is_git_repository(repo_path):
    command = f"git -C {repo_path} rev-parse --is-inside-work-tree"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip() == "true"
    except subprocess.CalledProcessError:
        return False

