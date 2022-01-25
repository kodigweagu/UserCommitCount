"""  """
class User:
    def __init__(self, user):
        self.name = user['name']
        self.email = user['email']
        self.commits = 1