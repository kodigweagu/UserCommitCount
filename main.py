"""  """
from fastapi import FastAPI
from User import User
import requests

DEFAULT_START = '2019-06-01'
DEFAULT_END = '2020-05-31'

app = FastAPI()

def get_data(start, end):
    users = []
    data = requests.get('https://api.github.com/repos/teradici/deploy/commits?since={}&until={}'.format(start, end))
    data = data.json()
    for commit in data:
        user = next((entry for entry in users if entry.email == commit['commit']['author']['email']), None)
        if user == None:
            users.append(User(commit['commit']['author']))
        else:
            user.commits += 1
    users = sorted(users, key = lambda user: (user.commits), reverse=True)
    return users

@app.get("/users")
def list_users(start: str = DEFAULT_START,end: str = DEFAULT_END):
    list = []
    users = get_data(start, end)
    for user in users:
        entry = dict()
        entry['name'] = user.name
        entry['email'] = user.email
        list.append(entry)
    return list

@app.get("/most-frequent")
def most_frequent(start: str = DEFAULT_START, end: str = DEFAULT_END):
    list = []
    users = get_data(start, end)
    for user in users[0:5]:
        entry = dict()
        entry['name'] = user.name
        entry['commits'] = user.commits
        list.append(entry)
    return list