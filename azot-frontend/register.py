import customtkinter as ctk
from tkinter import messagebox
import requests
from utils import adjust_window


class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = adjust_window(350, 350, master)
        master.geometry(window_size)

        ctk.CTkLabel(self, text='Register', font=('Helvetica', 20)).grid(row=0, column=1, pady=10)

        ctk.CTkLabel(self, text='Email').grid(row=1, column=0, padx=10, pady=5)
        self.register_email_entry = ctk.CTkEntry(self)
        self.register_email_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text='Password').grid(row=2, column=0, padx=10, pady=5)
        self.register_password_entry = ctk.CTkEntry(self, show='*')
        self.register_password_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text='Confirm Password').grid(row=3, column=0, padx=10, pady=5)
        self.confirm_password_entry = ctk.CTkEntry(self, show='*')
        self.confirm_password_entry.grid(row=3, column=1, padx=10, pady=5)

        self.register_seller_var = ctk.IntVar()
        ctk.CTkCheckBox(self, text='Seller', variable=self.register_seller_var).grid(row=4, column=1, pady=5)

        ctk.CTkButton(self, text='Register', command=self.register).grid(row=5, column=1, pady=10)
        ctk.CTkButton(self, text='Back to Login', command=master.create_login_frame).grid(row=6, column=1, pady=10)

    def register(self):
        email = self.register_email_entry.get()
        password = self.register_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror('Registration Error', 'Passwords do not match')
            return

        user_type = 'seller' if self.register_seller_var.get() else 'client'
        url = f'http://localhost:8080/api/{user_type}/register'
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.master.active_user_id = response.json().get('id')
            self.master.create_main_frame()
        else:
            messagebox.showerror('Registration Error', 'Registration failed')
