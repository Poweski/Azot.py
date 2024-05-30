import customtkinter as ctk
from tkinter import messagebox
import requests
from utils import adjust_window


class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = adjust_window(350, 400, master)
        master.geometry(window_size)

        ctk.CTkLabel(self, text='Register', font=('Helvetica', 20)).pack(pady=10)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=10, pady=10, fill='both', expand=True)

        self.client_tab = self.tabview.add('Client')
        self.seller_tab = self.tabview.add('Seller')

        self.create_client_registration_tab()
        self.create_seller_registration_tab()

    def create_client_registration_tab(self):
        ctk.CTkLabel(self.client_tab, text='Email').grid(row=0, column=0, padx=10, pady=5)
        self.client_email_entry = ctk.CTkEntry(self.client_tab)
        self.client_email_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.client_tab, text='Password').grid(row=1, column=0, padx=10, pady=5)
        self.client_password_entry = ctk.CTkEntry(self.client_tab, show='*')
        self.client_password_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.client_tab, text='Confirm Password').grid(row=2, column=0, padx=10, pady=5)
        self.client_confirm_password_entry = ctk.CTkEntry(self.client_tab, show='*')
        self.client_confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkButton(self.client_tab, text='Register', command=self.register_client).grid(row=3, column=1, pady=10)
        ctk.CTkButton(self.client_tab, text='Back to Login', command=self.master.create_login_frame).grid(row=4, column=1, pady=10)

    def create_seller_registration_tab(self):
        ctk.CTkLabel(self.seller_tab, text='Email').grid(row=0, column=0, padx=10, pady=5)
        self.seller_email_entry = ctk.CTkEntry(self.seller_tab)
        self.seller_email_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.seller_tab, text='Password').grid(row=1, column=0, padx=10, pady=5)
        self.seller_password_entry = ctk.CTkEntry(self.seller_tab, show='*')
        self.seller_password_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.seller_tab, text='Confirm Password').grid(row=2, column=0, padx=10, pady=5)
        self.seller_confirm_password_entry = ctk.CTkEntry(self.seller_tab, show='*')
        self.seller_confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkButton(self.seller_tab, text='Register', command=self.register_seller).grid(row=3, column=1, pady=10)
        ctk.CTkButton(self.seller_tab, text='Back to Login', command=self.master.create_login_frame).grid(row=4, column=1, pady=10)

    def register_client(self):
        self.register('client')

    def register_seller(self):
        self.register('seller')

    def register(self, user_type):
        if user_type == 'client':
            email = self.client_email_entry.get()
            password = self.client_password_entry.get()
            confirm_password = self.client_confirm_password_entry.get()
        else:
            email = self.seller_email_entry.get()
            password = self.seller_password_entry.get()
            confirm_password = self.seller_confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror('Registration Error', 'Passwords do not match')
            return

        url = f'http://localhost:8080/api/{user_type}/register'
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.master.active_user_id = response.json().get('id')
            self.master.create_main_frame()
        else:
            messagebox.showerror('Registration Error', 'Registration failed')
