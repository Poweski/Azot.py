import customtkinter as ctk
from tkinter import messagebox
import requests
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_frontend import App


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master: 'App'):
        super().__init__(master)
        self.master = master

        ctk.CTkLabel(self, text='Login', font=('Helvetica', 20)).grid(row=0, column=1, pady=10)

        ctk.CTkLabel(self, text='Email').grid(row=1, column=0, padx=10, pady=5)
        self.login_email_entry = ctk.CTkEntry(self)
        self.login_email_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text='Password').grid(row=2, column=0, padx=10, pady=5)
        self.login_password_entry = ctk.CTkEntry(self, show='*')
        self.login_password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.seller_var = ctk.IntVar()
        ctk.CTkCheckBox(self, text='Seller', variable=self.seller_var).grid(row=3, column=1, pady=5)

        ctk.CTkButton(self, text='Login', command=self.login).grid(row=4, column=1, pady=10)
        ctk.CTkButton(self, text='Register', command=self.master.create_registration_frame).grid(row=5, column=1, pady=10)

    def login(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()
        user_type = 'seller' if self.seller_var.get() else 'client'
        url = f'http://localhost:8080/api/{user_type}/login'
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.master.active_user_id = response.json().get('id')
            self.master.create_main_frame()
        else:
            messagebox.showerror('Login Error', 'Invalid email or password')
