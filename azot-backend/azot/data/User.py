from abc import ABC, abstractmethod


class User(ABC):
    @abstractmethod
    def __init__(self, email, password, uuid, user_details):
        self.email = email
        self.password = password
        self.uuid = uuid
        self.user_details = user_details