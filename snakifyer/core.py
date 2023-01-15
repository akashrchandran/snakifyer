import json
import os

from rich.console import Console
from rich.emoji import Emoji
from rich.style import Style

import snakifyer.api as api
from .cli import parse_cmd, check_config

snakifyer = api.Snakify()
console = Console()
config = check_config()
parse_cmd(config)
    
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