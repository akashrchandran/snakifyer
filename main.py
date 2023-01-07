import json

import core

snakifyer = core.Snakify()

config = json.load(open("config.json"))
if config["email"] == "" or config["password"] == "":
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    config["email"] = email
    config["password"] = password
    json.dump(config, open("config.json", "w"), indent=4)
    
snakifyer.login(config["email"], config["password"])

problems = snakifyer.get_all_problems()
for problem in problems:
    code = snakifyer.get_code(problem["slug"])
    ans = snakifyer.get_ans(problem["link"])
    if (isinstance(ans, list)):
        result = snakifyer.submit(problem["slug"], code, ans)
    elif (isinstance(ans, str)):
        result = snakifyer.save_progress(problem["slug"], ans)
    print(f'{problem["name"]}....{result}')