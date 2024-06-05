import datetime


class Client:
    def __init__(self, client_id, email, password, client_info=None, cart=None, purchases=None):
        self.id = client_id
        self.email = email
        self.password = password
        self.client_info = client_info
        self.cart = cart
        self.purchases = purchases

    def __str__(self):
        return (f'Client(id={self.id}, email={self.email}, '
                f'client_info={self.client_info}, cart={self.cart}, '
                f'purchases={self.purchases})')


class ClientInfo:
    def __init__(self, name=None, surname=None, phone=None, address=None, balance=0.0):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.address = address
        self.balance = balance

    def __str__(self):
        return (f'ClientInfo(name={self.name}, surname={self.surname}, '
                f'phone={self.phone}, address={self.address}, '
                f'balance={self.balance})')


class Seller:
    def __init__(self, seller_id, email, password, seller_info=None, products=None, purchases=None):
        self.id = seller_id
        self.email = email
        self.password = password
        self.seller_info = seller_info
        self.products = products
        self.purchases = purchases

    def __str__(self):
        return (f'Seller(id={self.id}, email={self.email}, '
                f'seller_info={self.seller_info}, products={self.products}, '
                f'purchases={self.purchases})')


class SellerInfo:
    def __init__(self, organization=None, phone=None, address=None):
        self.organization = organization
        self.phone = phone
        self.address = address

    def __str__(self):
        return (f'SellerInfo(organization={self.organization}, phone={self.phone}, '
                f'address={self.address})')


class Product:
    def __init__(self, product_id, name, price, description, image, items_available, tags, owner, avg_rating, reviews):
        self.id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.image = image
        self.items_available = items_available
        self.tags = tags
        self.owner = owner
        self.reviews = reviews
        self.avg_rating = avg_rating

    def __str__(self):
        return (f'Product(id={self.id}, name={self.name}, '
                f'price={self.price}, description={self.description}, '
                f'image={self.image}, items_available={self.items_available}, '
                f'tags={self.tags}, owner={self.owner})')


class Purchase:
    def __init__(self, purchase_id, product_name, quantity, cost, seller=None, client=None):
        self.id = purchase_id
        self.product_name = product_name
        self.quantity = quantity
        self.date = datetime.datetime.now()
        self.cost = cost
        self.seller = seller
        self.client = client

    def __str__(self):
        return (f'Purchase(id={self.id}, product_name={self.product_name}, '
                f'quantity={self.quantity}, date={self.date}, '
                f'cost={self.cost}, seller={self.seller}, '
                f'client={self.client})')


class Order:
    def __init__(self, order_id, product, quantity, cart):
        self.id = order_id
        self.product = product
        self.quantity = quantity
        self.cart = cart

    def __str__(self):
        return (f'Order(id={self.id}, product={self.product}, '
                f'quantity={self.quantity}, cart={self.cart})')
