import customtkinter as ctk
from shared import utils
from app_settings import *
import requests


class EditDialog(ctk.CTkToplevel):
    def __init__(self, master, cart, product_id, title='Title', message='Edit product in cart'):
        super().__init__(master)
        self.title(title)
        self.cart = cart
        self.product_id = product_id

        window_size = utils.adjust_window(250, 200, master)
        self.geometry(window_size)

        self.label = ctk.CTkLabel(self, text=message, font=('Helvetica', 15), wraplength=250)
        self.label.pack(padx=5, pady=10)

        self.submit_button = ctk.CTkButton(self, text='Delete from cart', command=self.delete_from_cart, fg_color='red', hover_color='#8B0000')
        self.submit_button.pack(padx=5, pady=10)

        self.submit_button = ctk.CTkButton(self, text='Change amount', command=self.get_amount)
        self.submit_button.pack(padx=5, pady=10)

        self.submit_button = ctk.CTkButton(self, text='OK', command=self.submit)
        self.submit_button.pack(padx=5, pady=10)

        self.value = 0

    def delete_from_cart(self):
        dialog = utils.ConfirmDialog(self, title='Delete', message='Are you sure you want to delete this product?')
        if dialog.show():
            orders = []
            for product_tuple in self.cart:
                quantity, product = product_tuple
                if product.id != self.product_id:
                    orders.append({
                        'product': product.id,
                        'quantity': quantity
                    })

            data = {'orders': orders}

            url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/client/{self.master.master.user.id}/cart'
            response = requests.put(url, json=data)

            if response.status_code == 200:
                self.master.display_offers()
                utils.InfoDialog(self, title='Success', message='Product deleted successfully').show()
            else:
                utils.ErrorDialog(self, message=response.json().get('error')).show()

    def change_amount(self):
        orders = []
        for product_tuple in self.cart:
            quantity, product = product_tuple
            if product.id != self.product_id:
                orders.append({
                    'product': product.id,
                    'quantity': quantity
                })
            else:
                if 0 <= quantity + self.value <= product.items_available:
                    orders.append({
                        'product': product.id,
                        'quantity': quantity + self.value
                    })
                else:
                    utils.ErrorDialog(self, message=f'Incorrect value provided!').show()

        data = {'orders': orders}

        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/client/{self.master.master.user.id}/cart'
        response = requests.put(url, json=data)

        if response.status_code == 200:
            self.master.display_offers()
            utils.InfoDialog(self, title='Success', message='Amount changed successfully').show()
        else:
            utils.ErrorDialog(self, message=response.json().get('error')).show()

    def get_amount(self):
        seek_quantity = 0
        for product_tuple in self.cart:
            quantity, product = product_tuple
            if product.id == self.product_id:
                seek_quantity = quantity

        value = utils.InputDialog(self, title='Change amount', message='Enter the difference:').show()
        try:
            self.value = int(value)
            if seek_quantity + self.value <= 0:
                raise ValueError
            self.change_amount()
        except ValueError:
            utils.ErrorDialog(self, message=f'Incorrect amount provided!').show()

    def submit(self):
        self.destroy()

    def show(self):
        self.grab_set()
        self.wait_window()
