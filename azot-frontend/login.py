import customtkinter as ctk
from tkinter import messagebox
import requests
from utils import adjust_window


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = adjust_window(350, 400, master)
        master.geometry(window_size)

        ctk.CTkLabel(self, text='Login', font=('Helvetica', 20)).pack(pady=10)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=10, pady=10, fill='both', expand=True)

        self.client_tab = self.tabview.add('Client')
        self.seller_tab = self.tabview.add('Seller')

        self.create_client_login_tab()
        self.create_seller_login_tab()

    def create_client_login_tab(self):
        ctk.CTkLabel(self.client_tab, text='Email').grid(row=0, column=0, padx=10, pady=5)
        self.client_email_entry = ctk.CTkEntry(self.client_tab)
        self.client_email_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.client_tab, text='Password').grid(row=1, column=0, padx=10, pady=5)
        self.client_password_entry = ctk.CTkEntry(self.client_tab, show='*')
        self.client_password_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(self.client_tab, text='Login', command=self.login_client).grid(row=2, column=1, pady=10)
        ctk.CTkButton(self.client_tab, text='Register', command=self.master.create_registration_frame).grid(row=3, column=1, pady=10)

    def create_seller_login_tab(self):
        ctk.CTkLabel(self.seller_tab, text='Email').grid(row=0, column=0, padx=10, pady=5)
        self.seller_email_entry = ctk.CTkEntry(self.seller_tab)
        self.seller_email_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.seller_tab, text='Password').grid(row=1, column=0, padx=10, pady=5)
        self.seller_password_entry = ctk.CTkEntry(self.seller_tab, show='*')
        self.seller_password_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(self.seller_tab, text='Login', command=self.login_seller).grid(row=2, column=1, pady=10)
        ctk.CTkButton(self.seller_tab, text='Register', command=self.master.create_registration_frame).grid(row=3, column=1, pady=10)

    def login_client(self):
        self.login('client')

    def login_seller(self):
        self.login('seller')

    def login(self, user_type):
        email = self.client_email_entry.get() if user_type == 'client' else self.seller_email_entry.get()
        password = self.client_password_entry.get() if user_type == 'client' else self.seller_password_entry.get()
        url = f'http://localhost:8080/api/{user_type}/login'
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.master.active_user_id = response.json().get('id')
            if user_type == 'seller':
                self.master.create_seller_main_frame()
            else:
                self.master.create_client_main_frame()
        else:
            messagebox.showerror('Login Error', 'Invalid email or password')
