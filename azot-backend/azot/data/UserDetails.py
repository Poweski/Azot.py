from abc import ABC, abstractmethod


class UserDetails():
    def __init__(self, uuid, name, surname, telephone, address):
        self.uuid = uuid
        self.name = name
        self.surname = surname
        self.telephone = telephone
        self.address = address

