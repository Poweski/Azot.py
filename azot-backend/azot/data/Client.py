import User

class Client(User):
    def __init__(self, email, password, uuid, user_details):
        super().__init__(email, password, uuid, user_details)

