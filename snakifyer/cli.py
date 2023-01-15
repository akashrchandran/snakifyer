import argparse
import json
import os

OS_CONFIG = os.environ.get("APPDATA") if os.name == "nt" else os.path.join(os.environ["HOME"], ".config")
CONFIG_PATH = os.path.join(OS_CONFIG, "snakifyer")
CONFIG_FILE = os.path.join(CONFIG_PATH, "config.json")

parser = argparse.ArgumentParser()

parser.add_argument("-u",
                    "--username",
                    metavar="USERNAME",
                    help='username of snakify account.'
                    )

parser.add_argument("-p",
                    "--password",
                    metavar="PASSWORD",
                    help='skip check for if it already downloaded and is available in directory. '
                    )

parser.add_argument("-r",
                    "--reset",
                    nargs='?',
                    const=True,
                    help="reset config to add new account.",
                    choices=[True, False],
                    )

def parse_cmd(config):
    args = parser.parse_args()
    if args.username:
        config['username'] = args.username
    if args.password:
        config['password'] = args.password
    if args.reset:
        reset_config()
    


def check_config(reset=False):
    if not os.path.exists(CONFIG_FILE) or reset:
        os.makedirs(CONFIG_PATH, exist_ok=True)
        reset_config()
    else:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    return config

def reset_config():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    config = {"email": email, "password": password}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)