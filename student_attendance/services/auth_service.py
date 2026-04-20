from repositories.db import hash_password
from repositories.user_repo import UserRepo


def login(username, password):
    repo = UserRepo()
    return repo.authenticate(username, hash_password(password))