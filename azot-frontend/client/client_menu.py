import customtkinter as ctk
from shared import utils
import requests
import threading
from functools import partial
from urllib.request import urlopen
from PIL import Image
import io
from app_settings import *


class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = utils.adjust_window(800, 600, master)
        master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        main_frame.pack(fill='both', expand=True)

        left_frame = ctk.CTkFrame(main_frame, corner_radius=0)
        left_frame.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky='nswe')
        ctk.CTkLabel(left_frame, text='Azot', font=('Helvetica', 20, 'bold')).pack(padx=20, pady=10)
        ctk.CTkLabel(left_frame, text='').pack()
        ctk.CTkLabel(left_frame, text='Your balance:', font=('Helvetica', 15)).pack(padx=20, pady=10)
        ctk.CTkLabel(left_frame, text=f'{self.master.user.client_info.balance} $', font=('Helvetica', 15)).pack(padx=20, pady=10)
        ctk.CTkLabel(left_frame, text='').pack()
        ctk.CTkButton(left_frame, text='Profile', command=master.create_client_profile_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Cart', command=master.create_cart_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Purchases', command=master.create_purchases_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Settings', command=master.create_settings_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Log Out', command=self.log_out).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Close App', command=self.quit).pack(padx=20, pady=10)

        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        ctk.CTkLabel(top_frame, text='Welcome to Azot!', font=('Helvetica', 20, 'bold')).pack(pady=10)

        search_frame = ctk.CTkFrame(main_frame)
        search_frame.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text='What are you looking for?')
        self.search_entry.grid(column=1, row=0, sticky='ew')
        search_button = ctk.CTkButton(search_frame, text='Search', command=self.search)
        search_button.grid(column=2, row=0, padx=5, pady=5)

        self.offers_frame = ctk.CTkFrame(main_frame, fg_color='#313335')
        self.offers_frame.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
        self.popular_offers_label = ctk.CTkLabel(self.offers_frame, text='Popular offers:', font=('Helvetica', 18))
        self.popular_offers_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)
        self.shuffle_button = ctk.CTkButton(self.offers_frame, text='Shuffle', command=self.shuffle_offers)
        self.shuffle_button.grid(row=0, column=2, columnspan=2)
        self.offers_frame.columnconfigure(0, weight=1)
        self.offers_frame.columnconfigure(1, weight=1)
        self.offers_frame.columnconfigure(2, weight=1)
        self.offers_frame.columnconfigure(3, weight=1)
        self.offers_frame.rowconfigure(0, weight=0)
        self.offers_frame.rowconfigure(1, weight=1)
        self.offers_frame.rowconfigure(2, weight=1)

        self.display_offers()

        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=0)
        main_frame.rowconfigure(1, weight=0)
        main_frame.rowconfigure(2, weight=1)

        search_frame.columnconfigure(0, weight=0)
        search_frame.columnconfigure(1, weight=1)
        search_frame.columnconfigure(2, weight=0)

    def display_offers(self):
        if not self.master.viewed_products:
            self.shuffle_offers()
        else:
            for i in range(2):
                for j in range(4):
                    self.create_product_view2(i + 1, j)

    def create_product_view2(self, row, column):
        product_frame = ctk.CTkFrame(self.offers_frame)
        product_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

        placeholder_label = ctk.CTkLabel(product_frame, text='Loading...')
        placeholder_label.pack()

        thread = threading.Thread(target=self.update_product_view2, args=(product_frame, placeholder_label, row, column))
        thread.start()

    def update_product_view2(self, product_frame, placeholder_label, row, column):
        placeholder_label.pack_forget()
        product = self.master.viewed_products[4 * (row - 1) + column]
        ctk.CTkLabel(product_frame, text=f'{product.name}').pack()
        image_url = product.image
        image_data = urlopen(image_url).read()
        image_pil = Image.open(io.BytesIO(image_data))
        new_size = (80, 80)
        image_pil_resized = image_pil.resize(new_size, Image.LANCZOS)
        image_ctk = ctk.CTkImage(light_image=image_pil_resized, size=new_size)
        image_label = ctk.CTkLabel(product_frame, image=image_ctk, text='')
        image_label.pack()
        ctk.CTkLabel(product_frame, text=f'Price: ${product.price:.2f}').pack()
        ctk.CTkLabel(product_frame, text=f'Items available: {product.items_available}').pack()
        check_command = partial(self.check_product, product.id)
        ctk.CTkButton(product_frame, text='Check', command=check_command, fg_color='red', hover_color='#8B0000').pack()

    def shuffle_offers(self):
        self.master.viewed_products.clear()
        for i in range(2):
            for j in range(4):
                self.create_product_view(i + 1, j)

    def create_product_view(self, row, column):
        product_frame = ctk.CTkFrame(self.offers_frame)
        product_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

        placeholder_label = ctk.CTkLabel(product_frame, text='Loading...')
        placeholder_label.pack()

        thread = threading.Thread(target=self.load_product, args=(product_frame, placeholder_label))
        thread.start()

    def load_product(self, product_frame, placeholder_label):
        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/product/random'
        response = requests.get(url)

        if response.status_code == 200:
            product_data = response.json().get('content')
            product_id = product_data['id']
            self.master.viewed_products.append(utils.create_product(product_data))

            self.master.after(0, self.update_product_view, product_frame, placeholder_label, product_data, product_id)
        elif response.status_code == 400:
            self.master.after(0, self.show_error, response.json().get('error'))
        else:
            self.master.after(0, self.show_error, 'Failed to load product!')

    def update_product_view(self, product_frame, placeholder_label, product_data, product_id):
        placeholder_label.pack_forget()
        ctk.CTkLabel(product_frame, text=f'{product_data['name']}').pack()
        image_url = product_data['image']
        image_data = urlopen(image_url).read()
        image_pil = Image.open(io.BytesIO(image_data))
        new_size = (80, 80)
        image_pil_resized = image_pil.resize(new_size, Image.LANCZOS)
        image_ctk = ctk.CTkImage(light_image=image_pil_resized, size=new_size)
        image_label = ctk.CTkLabel(product_frame, image=image_ctk, text='')
        image_label.pack()
        ctk.CTkLabel(product_frame, text=f'Price: ${product_data['price']:.2f}').pack()
        ctk.CTkLabel(product_frame, text=f'Items available: {product_data['items_available']}').pack()
        check_command = partial(self.check_product, product_id)
        ctk.CTkButton(product_frame, text='Check', command=check_command, fg_color='red', hover_color='#8B0000').pack()

    def show_error(self, message):
        utils.ErrorDialog(self, message=message).show()

    def check_product(self, product_id):
        self.master.create_product_frame(product_id)

    def search(self):
        phrase = self.search_entry.get()
        data = {'request': phrase}
        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/product'
        response = requests.post(url, json=data)

        if response.status_code == 200:
            products_list = response.json().get('content')
            row, column = 1, 0
            for product in products_list:
                if column > 3:
                    if row > 2:
                        return
                    row += 1
                    column = 0

                product_frame = ctk.CTkFrame(self.offers_frame)
                product_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

                placeholder_label = ctk.CTkLabel(product_frame, text='Loading...')
                placeholder_label.pack()

                thread = threading.Thread(target=self.update_product_view3, args=(product_frame, placeholder_label, product))
                thread.start()
        else:
            self.show_error()

    def update_product_view3(self, product_frame, placeholder_label, product):
        self.master.viewed_products.append(utils.create_product(product))
        placeholder_label.pack_forget()
        ctk.CTkLabel(product_frame, text=f'{product['name']}').pack()
        image_url = product['image']
        image_data = urlopen(image_url).read()
        image_pil = Image.open(io.BytesIO(image_data))
        new_size = (80, 80)
        image_pil_resized = image_pil.resize(new_size, Image.LANCZOS)
        image_ctk = ctk.CTkImage(light_image=image_pil_resized, size=new_size)
        image_label = ctk.CTkLabel(product_frame, image=image_ctk, text='')
        image_label.pack()
        ctk.CTkLabel(product_frame, text=f'Price: ${product['price']:.2f}').pack()
        ctk.CTkLabel(product_frame, text=f'Items available: {product['items_available']}').pack()
        check_command = partial(self.check_product, product['id'])
        ctk.CTkButton(product_frame, text='Check', command=check_command, fg_color='red', hover_color='#8B0000').pack()

    def log_out(self):
        dialog = utils.ConfirmDialog(self, title='Log Out', message='Are you sure you want to log out?')
        if dialog.show():
            self.master.create_login_frame()

    def quit(self):
        dialog = utils.ConfirmDialog(self, title='Quit', message='Are you sure you want to exit?')
        if dialog.show():
            self.master.quit()