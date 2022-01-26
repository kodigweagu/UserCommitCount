"""  """
from fastapi import FastAPI
from User import User
import requests
import json

import redis

DEFAULT_START = '2019-06-01'
DEFAULT_END = '2020-05-31'
TIMEOUT_TO_EXPIRE = 120

app = FastAPI()
redis_instance = redis.Redis(host='redis', port=6379, db=0)

def get_data(start, end):
    users = []
    data = redis_instance.get(start+'|'+end)
    if data:
        data = json.loads(data.decode('utf-8'))
        print('_\nRedis...\nGetting {} until {} data from redis.\n'.format(start, end))
    else:
        data = requests.get('https://api.github.com/repos/teradici/deploy/commits?since={}&until={}'.format(start, end))
        data = data.json()
        redis_instance.set(start+'|'+end, json.dumps(data), ex=TIMEOUT_TO_EXPIRE)
        print('_\nRedis...\Adding {} until {} data to redis.\n'.format(start, end))

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