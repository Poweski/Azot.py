import customtkinter as ctk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_frontend import App


class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master: 'App'):
        super().__init__(master)
        self.master = master

        ctk.CTkLabel(self, text='Welcome to Azot!', font=('Helvetica', 20)).grid(
            row=0, column=1, pady=10)
        ctk.CTkButton(self, text='Add Product', command=master.create_add_product_frame).grid(
            row=1, column=0, padx=10, pady=10)
        ctk.CTkButton(self, text='Sell Product', command=master.create_sell_product_frame).grid(
            row=1, column=1, padx=10, pady=10)
        # ctk.CTkButton(self, text='View Products', command=master.display_products).grid(
        #     row=1, column=2, padx=10, pady=10)
