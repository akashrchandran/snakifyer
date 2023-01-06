import requests
import re
from bs4 import BeautifulSoup
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
        match = re.search(r'window.tests = \[(.*?)\];', response.text)
        answers = eval(match[1])
        return [
            {"stderr": "", "stdout": f'{answer["answer"]}', "exception": None}
            for answer in answers
        ]
    
    def submit(self, slug, link, code):
        url = "https://snakify.org/api/v2/solution/checkAnswers"
        payload = {
            "problem": slug,
            "user_code": code,
            "language": "python",
            "answers": self.get_ans(link)
        }
        response = self.session.post(url, json=payload)
        return response.json()['status']
    
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