import customtkinter as ctk
from utils import adjust_window


class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = adjust_window(800, 600, master)
        master.geometry(window_size)

        ctk.CTkLabel(self, text='Welcome to Azot!', font=('Helvetica', 20)).grid(row=0, column=1, pady=10)

        # Main options
        ctk.CTkButton(self, text='Add Product', command=master.create_add_product_frame).grid(row=1, column=2, padx=10, pady=10)
        ctk.CTkButton(self, text='Sell Product', command=master.create_sell_product_frame).grid(row=1, column=3, padx=10, pady=10)
        # TODO show ones products

        # Left column options
        left_column = 0
        ctk.CTkButton(self, text='Profile', command=master.create_seller_profile_frame).grid(row=1, column=left_column, padx=10, pady=5)
        ctk.CTkButton(self, text='Messages', command=master.create_messages_frame).grid(row=2, column=left_column, padx=10, pady=5)
        ctk.CTkButton(self, text='Notifications', command=master.create_notifications_frame).grid(row=3, column=left_column, padx=10, pady=5)
        ctk.CTkButton(self, text='Your products', command=master.create_announcements_frame).grid(row=7, column=left_column, padx=10, pady=5)
        ctk.CTkButton(self, text="Close App", command=master.quit).grid(row=6, column=left_column, padx=10, pady=5)
