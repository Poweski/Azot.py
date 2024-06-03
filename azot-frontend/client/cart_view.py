import requests
import threading
from functools import partial
import customtkinter as ctk
from shared import utils

# TODO in production
# TODO change how products are loaded in the seller menu


class CartView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = utils.adjust_window(800, 600, master)
        master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        main_frame.pack(fill='both', expand=True)

        products_frame = ctk.CTkFrame(main_frame)
        products_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        right_frame = ctk.CTkFrame(main_frame)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        self.total = None

        ctk.CTkLabel(right_frame, text='').pack()
        cart_label = ctk.CTkLabel(right_frame, text='Cart', font=('Helvetica', 16))
        cart_label.pack(padx=5, pady=10)
        total_label = ctk.CTkLabel(right_frame, text='In total')
        total_label.pack()
        total_entry = ctk.CTkEntry(right_frame)
        total_entry.insert(0, f'{self.total}')
        total_entry.configure(state='disabled')
        total_entry.pack()

        ctk.CTkLabel(right_frame, text='').pack()
        ctk.CTkButton(right_frame, text='Buy', command=self.buy).pack(pady=10)
        ctk.CTkButton(right_frame, text='Back', command=master.create_client_main_frame).pack(pady=10)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)
        main_frame.rowconfigure(0, weight=1)

    def buy(self):
        url = f'http://localhost:8080/api/client/{self.master.user.id}/cart'
        response = requests.post(url)

        if response.status_code == 200:
            self.master.user.client_info.balance -= self.total
            utils.InfoDialog(self, title='Success', message='Products bought successfully').show()
        else:
            utils.ErrorDialog(self, message='Failed to buy products!').show()

    def actualize_total(self):
        pass

    def display_offers(self):
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
        url = f'http://localhost:8080/api/client/{self.master.user.id}/cart'
        response = requests.get(url)

        if response.status_code == 200:
            product_data = response.json().get('content')
            product_id = product_data['id']
            self.master.viewed_products.append(utils.create_product(product_data))

            self.master.after(0, self.update_product_view, product_frame, placeholder_label, product_data, product_id)
        else:
            self.master.after(0, self.show_error)

    def update_product_view(self, product_frame, placeholder_label, product_data, product_id):
        placeholder_label.pack_forget()
        ctk.CTkLabel(product_frame, text=f'{product_data['name']}').pack()
        ctk.CTkLabel(product_frame, text=f'Price: ${product_data['price']:.2f}').pack()
        ctk.CTkLabel(product_frame, text=f'Items available: {product_data['items_available']}').pack()
        check_command = partial(self.check_product, product_id)
        ctk.CTkButton(product_frame, text='Check', command=check_command, fg_color='red', hover_color='#8B0000').pack()

    def show_error(self):
        utils.ErrorDialog(self, message='Failed to download product').show()

    def check_product(self, product_id):
        self.master.create_product_frame(product_id)
