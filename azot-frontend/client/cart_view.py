import requests
import threading
from functools import partial
import customtkinter as ctk
from shared import utils
from app_settings import *


class CartView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = utils.adjust_window(800, 600, master)
        master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        main_frame.pack(fill='both', expand=True)

        self.products_frame = ctk.CTkFrame(main_frame, fg_color='#313335')
        self.products_frame.grid(row=0, column=0, rowspan=3, sticky='nsew', padx=10, pady=10)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        self.total = 0

        self.setup_right_frame(main_frame)

        self.display_offers()

    def setup_right_frame(self, main_frame):
        right_top_frame = ctk.CTkFrame(main_frame)
        right_top_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        right_mid_frame = ctk.CTkFrame(main_frame)
        right_mid_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)
        right_bottom_frame = ctk.CTkFrame(main_frame)
        right_bottom_frame.grid(row=2, column=1, sticky='nsew', padx=10, pady=10)

        ctk.CTkLabel(right_top_frame, text='').pack()
        ctk.CTkLabel(right_top_frame, text='Cart', font=('Helvetica', 20, 'bold')).pack(padx=5, pady=10)
        ctk.CTkLabel(right_top_frame, text='').pack()

        ctk.CTkLabel(right_mid_frame, text='').pack()
        ctk.CTkLabel(right_mid_frame, text='In total').pack()
        self.total_entry = ctk.CTkEntry(right_mid_frame, justify='right')
        self.total_entry.insert(0, f'$ {self.total}')
        self.total_entry.configure(state='disabled')
        self.total_entry.pack()
        ctk.CTkLabel(right_mid_frame, text='').pack()

        ctk.CTkLabel(right_bottom_frame, text='').pack()
        ctk.CTkButton(right_bottom_frame, text='Buy', command=self.buy, fg_color='red', hover_color='#8B0000').pack(padx=5, pady=10)
        ctk.CTkButton(right_bottom_frame, text='Back', command=self.master.create_client_main_frame).pack(padx=5, pady=10)
        ctk.CTkLabel(right_bottom_frame, text='').pack()

    def buy(self):
        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/client/{self.master.user.id}/cart'
        response = requests.post(url)

        if response.status_code == 200:
            self.master.user.client_info.balance -= self.total
            utils.InfoDialog(self, title='Success', message='Products bought successfully').show()
        else:
            utils.ErrorDialog(self, message='Failed to buy products!').show()

    def display_offers(self):
        self.placeholder_frame = ctk.CTkFrame(self.products_frame)
        self.placeholder_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        placeholder_label = ctk.CTkLabel(self.placeholder_frame, text='Loading...', font=('Helvetica', 20))
        placeholder_label.pack(padx=20, pady=30)

        self.current_row = 0
        self.current_column = 0

        load_thread = threading.Thread(target=self.load_products, args=(placeholder_label,))
        load_thread.start()

    def load_products(self, placeholder_label):

        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/client/{self.master.user.id}/cart'
        response = requests.get(url)

        if response.status_code == 200:
            products_data = response.json().get('content', {}).get('orders', [])
            if products_data:
                self.master.user.cart.clear()
                for product_data in products_data:
                    quantity = product_data['quantity']
                    product = utils.create_product(product_data['product'])
                    product_tuple = (quantity, product)
                    self.master.user.cart.append(product_tuple)

                self.master.after(0, self.update_product_views, placeholder_label)
            else:
                self.master.after(0, self.show_no_products, placeholder_label)
        else:
            self.master.after(0, self.show_error)

    def update_product_views(self, placeholder_label):
        if len(self.master.user.cart) > 0:
            placeholder_label.pack_forget()
            for product_tuple in self.master.user.cart:
                product_frame = ctk.CTkFrame(self.products_frame)
                self.update_product_view(product_frame, product_tuple)
                product_frame.grid(row=self.current_row, column=self.current_column, padx=5, pady=5, sticky='nsew')

                self.current_column += 1
                if self.current_column > 3:
                    self.current_row += 1
                    self.current_column = 0
        else:
            self.show_no_products(placeholder_label)

    def show_no_products(self, placeholder_label):
        placeholder_label.pack_forget()
        ctk.CTkLabel(self.products_frame, text='No products in cart', font=('Helvetica', 20)).pack(padx=5, pady=10)

    def update_product_view(self, product_frame, product_tuple):
        product_count, product = product_tuple
        self.total += product.price * product_count
        self.total_entry.configure(state='normal')
        self.total_entry.delete(0, 'end')
        self.total_entry.insert(0, f'$ {self.total}')
        self.total_entry.configure(state='disabled')
        ctk.CTkLabel(product_frame, text=f'{product.name}', font=('Helvetica', 14, 'bold')).pack(padx=5, pady=5)
        ctk.CTkLabel(product_frame, text=f'Price: ${product.price:.2f}').pack(padx=5, pady=5)
        ctk.CTkLabel(product_frame, text=f'Amount: {product_count}').pack(padx=5, pady=5)
        ctk.CTkLabel(product_frame, text=f'Total: ${(product.price * product_count):.2f}').pack(padx=5, pady=5)
        edit_command = partial(self.edit, product.id)
        ctk.CTkButton(product_frame, text='Edit', command=edit_command).pack(padx=10, pady=5)
        check_command = partial(self.check_product, product.id)
        ctk.CTkButton(product_frame, text='Check', command=check_command).pack(padx=10, pady=5)

    def show_error(self):
        utils.ErrorDialog(self, message='Failed to download product').show()

    def check_product(self, product_id):
        self.master.create_product_frame(product_id)

    def edit(self, product_id):
        _product = None
        for product in [product for quantity, product in self.master.user.cart]:
            if product_id == product.id:
                _product = product
        edit_message = utils.EditDialog(self, title=_product.name)
        edit_message.show()
