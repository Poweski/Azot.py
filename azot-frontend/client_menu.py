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
        ctk.CTkLabel(self, text='Popular offers', font=('Helvetica', 18)).grid(row=1, column=2, pady=10)
        # TODO show random offers

        # Left column options
        left_column = 0
        ctk.CTkButton(self, text='Profile', command=master.create_client_profile_frame).grid(row=0, column=left_column, padx=10, pady=5)
        ctk.CTkButton(self, text='Messages', command=master.create_messages_frame).grid(row=1, column=left_column, padx=10, pady=5)
        ctk.CTkButton(self, text='Notifications', command=master.create_notifications_frame).grid(row=2, column=left_column, padx=10, pady=5)
        ctk.CTkButton(self, text='Favorites', command=master.create_favorites_frame).grid(row=3, column=left_column, padx=10, pady=5)
        ctk.CTkButton(self, text='Cart', command=master.create_cart_frame).grid(row=4, column=left_column, padx=10, pady=5)
        ctk.CTkButton(self, text='Orders', command=master.create_orders_frame).grid(row=5, column=left_column, padx=10, pady=5)
