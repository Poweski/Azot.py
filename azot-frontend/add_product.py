import requests
from tkinter import messagebox
from utils import *


class AddProductFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = adjust_window(350, 300, master)
        master.geometry(window_size)

        ctk.CTkLabel(self, text='Add Product', font=('Helvetica', 20)).grid(row=0, column=1, pady=10)

        ctk.CTkLabel(self, text='Name').grid(row=1, column=0, padx=10, pady=5)
        self.product_name_entry = ctk.CTkEntry(self)
        self.product_name_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text='Price').grid(row=2, column=0, padx=10, pady=5)
        self.product_price_entry = ctk.CTkEntry(self)
        self.product_price_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text='Description').grid(row=3, column=0, padx=10, pady=5)
        self.product_description_entry = ctk.CTkEntry(self)
        self.product_description_entry.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text='Image URL').grid(row=4, column=0, padx=10, pady=5)
        self.product_image_entry = ctk.CTkEntry(self)
        self.product_image_entry.grid(row=4, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text='Tags').grid(row=5, column=0, padx=10, pady=5)
        self.product_tags_entry = ctk.CTkEntry(self)
        self.product_tags_entry.grid(row=5, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text='Items Available').grid(row=6, column=0, padx=10, pady=5)
        self.product_items_available_entry = ctk.CTkEntry(self)
        self.product_items_available_entry.grid(row=6, column=1, padx=10, pady=5)

        ctk.CTkButton(self, text='Add', command=self.add_product).grid(row=7, column=1, pady=10)
        ctk.CTkButton(self, text='Back', command=master.create_main_frame).grid(row=8, column=1, pady=10)

    def add_product(self):
        name = self.product_name_entry.get()
        price = float(self.product_price_entry.get())
        description = self.product_description_entry.get()
        image = self.product_image_entry.get()
        tags = self.product_tags_entry.get()
        items_available = int(self.product_items_available_entry.get())

        url = f'http://localhost:8080/api/seller/{self.master.active_user_id}/product'
        data = {
            'name': name,
            'price': price,
            'description': description,
            'image': image,
            'tags': tags,
            'items_available': items_available
        }

        response = requests.post(url, json=data)
        if response.status_code == 200:
            messagebox.showinfo('Success', 'Product added successfully')
            self.master.create_main_frame()
        else:
            messagebox.showerror('Error', 'Failed to add product')
