import json

from rich.console import Console
from rich.emoji import Emoji
from rich.style import Style

import core

snakifyer = core.Snakify()
console = Console()

config = json.load(open("config.json"))
if config["email"] == "" or config["password"] == "":
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    config["email"] = email
    config["password"] = password
    json.dump(config, open("config.json", "w"), indent=4)

snakifyer.login(config["email"], config["password"])

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