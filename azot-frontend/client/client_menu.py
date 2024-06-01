import customtkinter as ctk
from shared import utils, classes
import requests
import threading
from functools import partial
from urllib.request import urlopen
from PIL import Image
import io


class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = utils.adjust_window(800, 600, master)
        master.geometry(window_size)

        self.main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        self.main_frame.pack(fill='both', expand=True)

        self.setup_left_frame()
        self.setup_top_frame()
        self.setup_search_frame()
        self.setup_offers_frame()

        self.shuffle_offers()

        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=0)
        self.main_frame.rowconfigure(2, weight=1)

    def setup_left_frame(self):
        left_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        left_frame.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky='nswe')
        ctk.CTkLabel(left_frame, text='Azot', font=('Helvetica', 20, 'bold')).pack(padx=20, pady=10)
        ctk.CTkLabel(left_frame, text='Your balance:', font=('Helvetica', 15)).pack(padx=20, pady=10)
        balance = self.master.user.client_info.balance
        ctk.CTkLabel(left_frame, text=f'{balance}', font=('Helvetica', 15)).pack(padx=20, pady=10)
        self.create_left_buttons(left_frame)

    def create_left_buttons(self, left_frame):
        buttons = [
            ('Profile', self.master.create_client_profile_frame),
            ('Cart', self.master.create_cart_frame),
            ('Purchases', self.master.create_orders_frame),
            ('Settings', self.master.create_settings_frame),
            ('Log Out', self.log_out),
            ('Close App', self.quit)
        ]
        for text, command in buttons:
            ctk.CTkButton(left_frame, text=text, command=command).pack(padx=20, pady=10)

    def setup_top_frame(self):
        top_frame = ctk.CTkFrame(self.main_frame)
        top_frame.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        ctk.CTkLabel(top_frame, text='Welcome to Azot!', font=('Helvetica', 20, 'bold')).pack(pady=10)

    def setup_search_frame(self):
        search_frame = ctk.CTkFrame(self.main_frame)
        search_frame.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text='Product name')
        self.search_entry.grid(column=1, row=0, sticky='ew')
        search_button = ctk.CTkButton(search_frame, text='Search', command=self.make_search)
        search_button.grid(column=2, row=0, padx=5, pady=5)

        search_frame.columnconfigure(0, weight=0)
        search_frame.columnconfigure(1, weight=1)
        search_frame.columnconfigure(2, weight=0)

    def setup_offers_frame(self):
        self.offers_frame = ctk.CTkFrame(self.main_frame, fg_color='#313335')
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

    def shuffle_offers(self):
        self.clear_offers_frame()
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
        try:
            response = requests.get('http://localhost:8080/api/product/random')
            response.raise_for_status()

            product_data = response.json().get('content')
            product_id = product_data['id']
            self.create_product(product_data)

            self.master.after(0, self.update_product_view, product_frame, placeholder_label, product_data, product_id)
        except requests.RequestException:
            self.master.after(0, self.show_error)

    def update_product_view(self, product_frame, placeholder_label, product_data, product_id):
        placeholder_label.pack_forget()
        ctk.CTkLabel(product_frame, text=f"{product_data['name']}").pack()
        image_url = product_data['image']
        image_data = urlopen(image_url).read()
        image_pil = Image.open(io.BytesIO(image_data))
        new_size = (80, 80)
        image_pil_resized = image_pil.resize(new_size, Image.LANCZOS)
        image_ctk = ctk.CTkImage(light_image=image_pil_resized, size=new_size)
        image_label = ctk.CTkLabel(product_frame, image=image_ctk, text='')
        image_label.pack()
        ctk.CTkLabel(product_frame, text=f"Price: ${product_data['price']:.2f}").pack()
        ctk.CTkLabel(product_frame, text=f"Items available: {product_data['items_available']}").pack()
        check_command = partial(self.check_product, product_id)
        ctk.CTkButton(product_frame, text='Check', command=check_command, fg_color='red', hover_color='#8B0000').pack()

    def show_error(self):
        utils.ErrorDialog(self, message='Failed to download product').show()

    def display_no_results(self):
        self.clear_offers_frame()
        ctk.CTkLabel(self.offers_frame, text='No Results', font=('Helvetica', 18)).grid(row=1, column=0, columnspan=4, padx=5, pady=10)

    def check_product(self, product_id):
        self.master.create_product_frame(product_id)

    def create_product(self, product_info):
        self.master.viewed_products.append(
            classes.Product(
                product_info['id'],
                product_info['name'],
                product_info['price'],
                product_info['description'],
                product_info['image'],
                product_info['items_available'],
                product_info['tags'],
                product_info['owner']
            )
        )

    def make_search(self):
        thread = threading.Thread(target=self.search)
        thread.start()

    def search(self):
        url = 'http://localhost:8080/api/product'
        data = {'request': self.search_entry.get()}

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()

            products = response.json().get('content')
            self.display_search_results(products)
        except requests.RequestException:
            self.master.after(0, self.display_no_results)

    def display_search_results(self, products):
        self.clear_offers_frame()

        row, column = 1, 0
        for product_data in products:
            if column > 3:
                if row > 1:
                    return
                row += 1
                column = 0

            product_id = product_data['id']
            self.create_product(product_data)
            self.create_search_result_view(row, column, product_data, product_id)
            column += 1

    def create_search_result_view(self, row, column, product_data, product_id):
        product_frame = ctk.CTkFrame(self.offers_frame)
        product_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')
        ctk.CTkLabel(product_frame, text=f"{product_data['name']}").pack()
        ctk.CTkLabel(product_frame, text=f"Price: ${product_data['price']:.2f}").pack()
        ctk.CTkLabel(product_frame, text=f"Items available: {product_data['items_available']}").pack()
        check_command = partial(self.check_product, product_id)
        ctk.CTkButton(product_frame, text='Check', command=check_command, fg_color='#382449', hover_color='#301934').pack()

    def clear_offers_frame(self):
        for widget in self.offers_frame.winfo_children():
            if widget not in (self.shuffle_button, self.popular_offers_label):
                widget.destroy()

    def log_out(self):
        dialog = utils.ConfirmDialog(self, title='Log Out', message='Are you sure you want to log out?')
        if dialog.show():
            self.master.create_login_frame()

    def quit(self):
        dialog = utils.ConfirmDialog(self, title='Quit', message='Are you sure you want to exit?')
        if dialog.show():
            self.master.quit()
