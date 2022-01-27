""" 
The main module in our simple web application runs fastAPI
exposes the API endpoints: /users and /most-frequent
"""
import requests # makes http requests
import json # manipulates json strings
import redis # provides redis service
from fastapi import FastAPI # creates restful API
from User import User

# default values
URL = 'https://api.github.com/repos/teradici/deploy/commits'
DEFAULT_START = '2019-06-01'
DEFAULT_END = '2020-05-31'
TIMEOUT_TO_EXPIRE = 120

# get an instance of the redis service
redis_instance = redis.Redis(host='redis', port=6379)

# initialize the API
app = FastAPI()

def list_users(data):
    # initialize an empty list of users
    users = []
    # count commits for each unique author identified by email
    for commit in data:
        user = next((entry for entry in users if entry.email == commit['commit']['author']['email']), None)
        if user == None:
            users.append(User(commit['commit']['author']))
        else:
            user.commits += 1
    users = sorted(users, key = lambda user: (user.commits), reverse=True)
    # return processed list
    return users

# get_users returns an array of users for everyone that has committed code to URL
@app.get("/users")
def get_users():
    list = []
    # id cache entry as 'users'
    cache_id = 'users'
    data = redis_instance.get(cache_id)
    # check if there is an entry in the cache for cache_id
    if data:
        data = json.loads(data.decode('utf-8'))
    else:
        # if there's no entry in the cache make http request
        response = requests.get(URL)
        # return None for status_code not 200
        if not response.status_code == 200:
            data = None
        else:
            data = response.json()
            # cache valid response
            redis_instance.set(cache_id, json.dumps(data), ex=TIMEOUT_TO_EXPIRE)

    if(not data == None):
        users = list_users(data)
        # format each user in our list in this form: [ { name: string, email: string, } ]
        for user in users:
            entry = dict()
            entry['name'] = user.name
            entry['email'] = user.email
            list.append(entry)
    else:
        list = None
    return list

# most_frequent Count the number of commits which occurred since start until end with the format of the start and end being YYYY-MM-DD see DEFAULT_START and DEFAULT_END
@app.get("/most-frequent")
def most_frequent(start: str = DEFAULT_START, end: str = DEFAULT_END):
    list = []
    # id each cache entry by string in format 'YYYY-MM-DD|YYYY-MM-DD'
    cache_id = start+'|'+end
    data = redis_instance.get(cache_id)
    # check if there is an entry in the cache for cache_id
    if data:
        data = json.loads(data.decode('utf-8'))
    else:
        # if there's no entry in the cache make http request
        response = requests.get('{}?since={}&until={}'.format(URL,start, end))
        # return None for status_code not 200
        if not response.status_code == 200:
            data = None
        else:
            data = response.json()
            # cache valid response
            redis_instance.set(cache_id, json.dumps(data), ex=TIMEOUT_TO_EXPIRE)
            
    if(not data == None):
        users = list_users(data)
        # format each user in our list in this form: [ { name: string, commits: int, } ]
        for user in users[0:5]:
            entry = dict()
            entry['name'] = user.name
            entry['commits'] = user.commits
            list.append(entry)
    else:
        list = None
    return list