import json
import os

from rich.console import Console
from rich.emoji import Emoji
from rich.style import Style

import snakifyer.api as api

snakifyer = api.Snakify()
console = Console()

OS_CONFIG = os.environ.get("APPDATA") if os.name == "nt" else os.path.join(os.environ["HOME"], ".config")
CONFIG_PATH = os.path.join(OS_CONFIG, "snakifyer")
CONFIG_FILE = os.path.join(CONFIG_PATH, "config.json")
if not os.path.exists(CONFIG_FILE):
    os.makedirs(CONFIG_PATH, exist_ok=True)
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    with open(CONFIG_FILE, "w+") as f:
        f.write(json.dumps({"email": email, "password": password}, indent=4))

with open(CONFIG_FILE) as f:
    config = json.load(f)
    
snakifyer.login(config["email"], config["password"])

def main():
    problems = snakifyer.get_all_problems()
    with console.status("Starting the Interface", spinner_style=Style(color='yellow')) as status:
        for problem in problems:
            status.update(f"[bold yellow]Working on {problem['name']}")
            code = snakifyer.get_code(problem["slug"])
            ans = snakifyer.get_ans(problem["link"])
            if (isinstance(ans, list)):
                result = snakifyer.submit(problem["slug"], code, ans)
            elif (isinstance(ans, str)):
                result = snakifyer.save_progress(problem["slug"], ans)
            if result == 'ok':
                console.print(f"[bold green]{Emoji('white_check_mark')} {problem['name']} complete")
            else:
                console.print(f"[bold green]{Emoji('x')} {problem['name']} errored out")