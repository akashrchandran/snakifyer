import re

import requests
from bs4 import BeautifulSoup

class AuthError(Exception):
    pass

class Snakify:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json;charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
        }

    def login(self, email, password):
        url = "https://snakify.org/api/v2/auth/login"
        payload = {
            "email": email,
            "password": password
        }
        req = self.session.post(url, json=payload)
        if not req.cookies.get("sessionid"):
            raise AuthError("Invalid email and password combination")
        self.session.cookies = req.cookies

    def get_code(self, slug):
        url = "https://snakify.org/api/v2/problem/modelSolution"
        payload = {
            "problemUrlname": slug,
            "language": "python"
        }
        response = self.session.post(url, json=payload)
        return response.json()['code']
    
    def get_ans(self, slug):
        url = f"https://snakify.org/{slug}"
        response = self.session.get(url)
        screen_type = re.search(r'window.screenType = \'(.*?)\';', response.text)
        if screen_type[1] == 'inout':
            match = re.search(r'window.tests = \[(.*?)\];', response.text)
            answers = eval(match[1])
            return [
                {"stderr": "", "stdout": f'{answer["answer"]}', "exception": None}
                for answer in answers
            ]
        elif screen_type[1] == 'frontend':
            match = re.search(r'window.defaultSolution = (.*?);', response.text)
            return eval(match[1])
    
    def submit(self, slug, code, ans):
        url = "https://snakify.org/api/v2/solution/checkAnswers"
        payload = {
            "problem": slug,
            "user_code": code,
            "language": "python",
            "answers": ans
        }
        response = self.session.post(url, json=payload)
        return response.json()['status']

    def save_progress(self, slug, ans):
        url = "https://snakify.org/api/v2/solution/saveProgress"
        payload = {
            "problem": slug,
            "user_code": ans,
            "language": "frontend",
            "status": "ok",
            "reuse_submission": False
        }
        response = self.session.post(url, json=payload)
        return "ok" if response.text == "{}" else "error"
    
    def get_all_problems(self):
        req = self.session.get('https://snakify.org/profile/')
        soup = BeautifulSoup(req.text, 'html.parser')
        links = soup.find_all(class_ = ["problem-status__", "problem-status__error"])
        return [
            {
                'name': link.text,
                'link': link['href'],
                'slug': link['href'].split('/')[-2],
            }
            for link in links
        ]