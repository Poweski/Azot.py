import requests
import threading
import customtkinter as ctk
from shared import utils
from app_settings import *
from datetime import datetime


class OrdersView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = utils.adjust_window(800, 600, master)
        master.geometry(window_size)

        self.main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        self.main_frame.pack(fill='both', expand=True)

        self.setup_top_frame(self.main_frame)

        self.products_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color='#313335')
        self.products_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

        self.display_offers()

    def setup_top_frame(self, main_frame):
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        purchases_label = ctk.CTkLabel(top_frame, text='Your sold products', font=('Helvetica', 20, 'bold'))
        purchases_label.pack(padx=5, pady=10)

        top_button_frame = ctk.CTkFrame(main_frame)
        top_button_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        back_button = ctk.CTkButton(top_button_frame, text='Back', command=self.master.create_seller_main_frame)
        back_button.pack(padx=5, pady=10)

    def display_offers(self):
        self.master.user.purchases = []

        self.placeholder_frame = ctk.CTkFrame(self.products_frame)
        self.placeholder_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        placeholder_label = ctk.CTkLabel(self.placeholder_frame, text='Loading...', font=('Helvetica', 20))
        placeholder_label.pack(padx=20, pady=30)

        self.current_row = 0
        self.current_column = 0

        load_thread = threading.Thread(target=self.load_products, args=(placeholder_label,))
        load_thread.start()

    def load_products(self, placeholder_label):
        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/seller/{self.master.user.id}/purchases'
        response = requests.get(url)

        if response.status_code == 200:
            products_data = response.json().get('content', [])
            if products_data:
                for product_data in products_data:
                    purchase = {
                        'product': product_data['product'],
                        'quantity': product_data['quantity'],
                        'date': product_data['date'],
                        'cost': product_data['cost']
                    }
                    self.master.user.purchases.append(purchase)

                self.master.after(0, self.update_product_views, placeholder_label)
            else:
                self.master.after(0, self.show_no_products, placeholder_label)
        else:
            self.master.after(0, self.show_error, response)

    def update_product_views(self, placeholder_label):
        placeholder_label.pack_forget()
        for purchase in self.master.user.purchases:
            product_frame = ctk.CTkFrame(self.products_frame)
            self.update_product_view(product_frame, purchase)
            product_frame.grid(row=self.current_row, column=self.current_column, padx=5, pady=5, sticky='nsew')

            self.current_column += 1
            if self.current_column > 3:
                self.current_row += 1
                self.current_column = 0

    def show_no_products(self, placeholder_label):
        placeholder_label.pack_forget()
        ctk.CTkLabel(self.placeholder_frame, text='No products sold', font=('Helvetica', 20)).pack(padx=5, pady=10)

    def update_product_view(self, product_frame, purchase):
        date_object = datetime.fromisoformat(purchase['date'].replace("Z", "+00:00"))
        formatted_date = date_object.strftime("%Y-%m-%d")
        formatted_time = date_object.strftime("%H:%M:%S")

        total_entry = ctk.CTkEntry(product_frame, justify='center', font=('Helvetica', 14, 'bold'), width=175)
        total_entry.insert(0, f"{purchase['product']}")
        total_entry.configure(state='disabled')
        total_entry.pack(padx=5, pady=5)

        ctk.CTkLabel(product_frame, text=f"Amount: {purchase['quantity']}").pack(padx=5, pady=5)
        ctk.CTkLabel(product_frame, text=f"Cost: $ {purchase['cost']}").pack(padx=5, pady=5)
        ctk.CTkLabel(product_frame, text=f"Date: {formatted_date}").pack(padx=5, pady=5)
        ctk.CTkLabel(product_frame, text=f"Time: {formatted_time}").pack(padx=5, pady=5)

    def show_error(self, response):
        utils.ErrorDialog(self, message=response.json().get('error')).show()
