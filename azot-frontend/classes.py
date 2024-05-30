import datetime


class Client:
    def __init__(self, id, email, password, client_info=None, cart=None, purchases=None):
        self.id = id
        self.email = email
        self.password = password
        self.client_info = client_info
        self.cart = cart
        self.purchases = purchases


class ClientInfo:
    def __init__(self, name=None, surname=None, phone=None, address=None, balance=0.0):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.address = address
        self.balance = balance


class Seller:
    def __init__(self, id, email, password, seller_info=None, products=None, purchases=None):
        self.id = id
        self.email = email
        self.password = password
        self.seller_info = seller_info
        self.products = products
        self.purchases = purchases


class SellerInfo:
    def __init__(self, organization=None, phone=None, address=None):
        self.organization = organization
        self.phone = phone
        self.address = address


class Product:
    def __init__(self, id, name, price, description, image, items_available, tags, owner):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.image = image
        self.items_available = items_available
        self.tags = tags
        self.owner = owner


class Purchase:
    def __init__(self, id, product_name, quantity, cost, seller=None, client=None):
        self.id = id
        self.product_name = product_name
        self.quantity = quantity
        self.date = datetime.datetime.now()
        self.cost = cost
        self.seller = seller
        self.client = client


class Order:
    def __init__(self, id, product, quantity, cart):
        self.id = id
        self.product = product
        self.quantity = quantity
        self.cart = cart
