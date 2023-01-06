import core
import json

client = core.Snakify()

config = json.load(open("config.json"))
if config["email"] == "" or config["password"] == "":
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    config["email"] = email
    config["password"] = password
    json.dump(config, open("config.json", "w"), indent=4)
    
client.login(config["email"], config["password"])

problems = client.get_all_problems()
for problem in problems:
    code = client.get_code(problem["slug"])
    result = client.submit(problem["slug"], problem['link'], code)
    print(f'{problem["name"]}....{result}')