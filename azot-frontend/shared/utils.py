import customtkinter as ctk
from .classes import *
import requests


def show_success_dialog(self):
    InfoDialog(self, title='Success', message='Password changed successfully').show()


def show_error_dialog(self, message):
    ErrorDialog(self, message=message).show()


def create_seller_user(user_data, email, password):
    seller_info_data = user_data.get('seller_info')
    seller_info = None

    if seller_info_data:
        seller_info = SellerInfo(
            organization=seller_info_data.get('organization'),
            phone=seller_info_data.get('phone'),
            address=seller_info_data.get('address')
        )

    return Seller(
        seller_id=user_data.get('id'),
        email=email,
        password=password,
        seller_info=seller_info,
        products=[],
        purchases=[]
    )


def create_client_user(user_data, email, password):
    client_info_data = user_data.get('client_info')
    client_info = None

    if client_info_data:
        client_info = ClientInfo(
            name=client_info_data.get('name'),
            surname=client_info_data.get('surname'),
            phone=client_info_data.get('phone'),
            address=client_info_data.get('address'),
            balance=client_info_data.get('balance')
        )

    return Client(
        client_id=user_data.get('id'),
        email=email,
        password=password,
        client_info=client_info,
        cart=[],
        purchases=[]
    )


def download_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        product_data = response.json().get('content')
        return create_product(product_data)
    return response.json().get('error')


def adjust_window(window_width, window_height, app):
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    return f'{window_width}x{window_height}+{x}+{y}'


def create_product(product_info):
    return Product(
        product_info['id'],
        product_info['name'],
        product_info['price'],
        product_info['description'],
        product_info['image'],
        product_info['items_available'],
        product_info['tags'],
        product_info['owner'],
        product_info['average_rating'],
        product_info['reviews']
    )


class ErrorDialog(ctk.CTkToplevel):
    def __init__(self, master, title='Error', message='An error has occurred'):
        super().__init__(master)
        self.title(title)
        window_size = adjust_window(400, 150, master)
        self.geometry(window_size)

        self.label = ctk.CTkLabel(self, text=message, font=('Helvetica', 15))
        self.label.pack(pady=20)

        self.button_frame = ctk.CTkFrame(self, bg_color=self.cget('background'), fg_color=self.cget('background'))
        self.button_frame.pack(pady=10)

        self.ok_button = ctk.CTkButton(self.button_frame, text='OK', command=self.on_ok, fg_color='red', hover_color='#8B0000')
        self.ok_button.grid(row=0, column=0, padx=10)

        self.result = None

    def on_ok(self):
        self.result = True
        self.destroy()

    def show(self):
        self.grab_set()
        self.wait_window()
        return self.result


class InfoDialog(ctk.CTkToplevel):
    def __init__(self, master, title='Error', message='An error has occurred'):
        super().__init__(master)
        self.title(title)
        window_size = adjust_window(400, 150, master)
        self.geometry(window_size)

        self.label = ctk.CTkLabel(self, text=message, font=('Helvetica', 15))
        self.label.pack(pady=20)

        self.button_frame = ctk.CTkFrame(self, bg_color=self.cget('background'), fg_color=self.cget('background'))
        self.button_frame.pack(pady=10)

        self.ok_button = ctk.CTkButton(self.button_frame, text='OK', command=self.on_ok)
        self.ok_button.grid(row=0, column=0, padx=10)

        self.result = None

    def on_ok(self):
        self.result = True
        self.destroy()

    def show(self):
        self.grab_set()
        self.wait_window()
        return self.result


class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, master, title='Title', message='Message'):
        super().__init__(master)
        self.title(title)
        window_size = adjust_window(400, 150, master)
        self.geometry(window_size)

        self.label = ctk.CTkLabel(self, text=message, font=('Helvetica', 15), wraplength=250)
        self.label.pack(pady=20)

        self.button_frame = ctk.CTkFrame(self, bg_color=self.cget('background'), fg_color=self.cget('background'))
        self.button_frame.pack(pady=10)

        self.yes_button = ctk.CTkButton(self.button_frame, text='Yes', command=self.on_yes, fg_color='red', hover_color='#8B0000')
        self.yes_button.grid(row=0, column=0, padx=10)

        self.no_button = ctk.CTkButton(self.button_frame, text='No', command=self.on_no)
        self.no_button.grid(row=0, column=1, padx=10)

        self.result = None

    def on_yes(self):
        self.result = True
        self.destroy()

    def on_no(self):
        self.result = False
        self.destroy()

    def show(self):
        self.grab_set()
        self.wait_window()
        return self.result


class InputDialog(ctk.CTkToplevel):
    def __init__(self, master, title='Title', message='Message'):
        super().__init__(master)
        self.title(title)
        window_size = adjust_window(400, 150, master)
        self.geometry(window_size)

        self.label = ctk.CTkLabel(self, text=message, font=('Helvetica', 15), wraplength=250)
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(self, text='Submit', command=self.submit)
        self.submit_button.pack(pady=10)

        self.value = None

    def submit(self):
        self.value = self.entry.get()
        self.destroy()

    def show(self):
        self.grab_set()
        self.wait_window()
        return self.value
