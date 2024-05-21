import customtkinter as ctk
from tkinter import messagebox
import requests
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_frontend import App


class AddProductFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        ctk.CTkLabel(self, text='Add Product', font=('Helvetica', 20)).grid(row=0, column=1, pady=10)

        ctk.CTkLabel(self, text='Name').grid(row=1, column=0, padx=10, pady=5)
        self.product_name_entry = ctk.CTkEntry(self)
        self.product_name_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text='Price').grid(row=2, column=0, padx=10, pady=5)
        self.product_price_entry = ctk.CTkEntry(self)
        self.product_price_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkButton(self, text='Add', command=self.add_product).grid(row=3, column=1, pady=10)
        ctk.CTkButton(self, text='Back', command=master.create_main_frame).grid(row=3, column=2, pady=10)

    def add_product(self):
        name = self.product_name_entry.get()
        price = self.product_price_entry.get()
        url = f'http://localhost:8080/api/seller/{self.master.active_user_id}/product'
        data = {'name': name, 'price': price}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            messagebox.showinfo('Success', 'Product added successfully')
            self.master.create_main_frame()
        else:
            messagebox.showerror('Error', 'Failed to add product')


class SellProductFrame(ctk.CTkFrame):
    def __init__(self, master: 'App'):
        super().__init__(master)
        self.master = master

        ctk.CTkLabel(self, text='Sell Product', font=('Helvetica', 20)).grid(row=0, column=1, pady=10)

        ctk.CTkLabel(self, text='Product ID').grid(row=1, column=0, padx=10, pady=5)
        self.sell_product_id_entry = ctk.CTkEntry(self)
        self.sell_product_id_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(self, text='Sell', command=self.sell_product).grid(row=2, column=1, pady=10)
        ctk.CTkButton(self, text='Back', command=master.create_main_frame).grid(row=2, column=2, pady=10)

    def sell_product(self):
        product_id = self.sell_product_id_entry.get()
        url = f'http://localhost:8080/api/client/{self.master.active_user_id}/product/{product_id}'
        response = requests.get(url)
        if response.status_code == 200:
            messagebox.showinfo('Success', 'Product sold successfully')
            self.master.create_main_frame()
        else:
            messagebox.showerror('Error', 'Failed to sell product')
