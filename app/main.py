"""  """
import requests
import json
import redis
from fastapi import FastAPI
from User import User

URL = 'https://api.github.com/repos/teradici/deploy/commits'
DEFAULT_START = '2019-06-01'
DEFAULT_END = '2020-05-31'
TIMEOUT_TO_EXPIRE = 120

redis_instance = redis.Redis(host='redis', port=6379)
app = FastAPI()

def get_data(start, end):
    users = []
    cache_id = start+'|'+end
    data = redis_instance.get(cache_id)
    if data:
        data = json.loads(data.decode('utf-8'))
    else:
        response = requests.get('{}?since={}&until={}'.format(URL,start, end))
        if not response.status_code == 200:
            return None
        data = response.json()
        redis_instance.set(cache_id, json.dumps(data), ex=TIMEOUT_TO_EXPIRE)

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
    if not users is None:
        for user in users:
            entry = dict()
            entry['name'] = user.name
            entry['email'] = user.email
            list.append(entry)
    else:
        list = None
    return list

@app.get("/most-frequent")
def most_frequent(start: str = DEFAULT_START, end: str = DEFAULT_END):
    list = []
    users = get_data(start, end)
    if not users is None:
        for user in users[0:5]:
            entry = dict()
            entry['name'] = user.name
            entry['commits'] = user.commits
            list.append(entry)
    else:
        list = None
    return list