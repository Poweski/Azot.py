import customtkinter as ctk
from tkinter import messagebox
import requests
from utils import adjust_window


class SellProductFrame(ctk.CTkFrame):
    def __init__(self, master: 'App'):
        super().__init__(master)
        self.master = master

        window_size = adjust_window(350, 300, master)
        master.geometry(window_size)

        ctk.CTkLabel(self, text='Sell Product', font=('Helvetica', 20)).grid(row=0, column=1, pady=10)

        ctk.CTkLabel(self, text='Product ID').grid(row=1, column=0, padx=10, pady=5)
        self.sell_product_id_entry = ctk.CTkEntry(self)
        self.sell_product_id_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(self, text='Sell', command=self.sell_product).grid(row=2, column=1, pady=10)
        ctk.CTkButton(self, text='Back', command=master.create_main_frame).grid(row=3, column=1, pady=10)

    def sell_product(self):
        product_id = self.sell_product_id_entry.get()
        url = f'http://localhost:8080/api/client/{self.master.active_user_id}/product/{product_id}'
        response = requests.get(url)
        if response.status_code == 200:
            messagebox.showinfo('Success', 'Product sold successfully')
            self.master.create_main_frame()
        else:
            messagebox.showerror('Error', 'Failed to sell product')
