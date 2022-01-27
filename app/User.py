""" 
User class defines the representation of everyone that has committed code to 
https://github.com/teradici/deploy for our simple web application
"""
class User:
    def __init__(self, user):
        self.name = user['name']
        self.email = user['email']
        self.commits = 1