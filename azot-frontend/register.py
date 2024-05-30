import requests
from classes import *
from utils import *


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

        self.create_registration_tab(self.client_tab, 'client')
        self.create_registration_tab(self.seller_tab, 'seller')

    def create_registration_tab(self, tab, user_type):
        ctk.CTkLabel(tab, text='').grid(row=0, column=0, padx=10, pady=1)
        ctk.CTkLabel(tab, text='Email').grid(row=1, column=0, padx=10, pady=5)
        email_entry = ctk.CTkEntry(tab)
        email_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(tab, text='Password').grid(row=2, column=0, padx=10, pady=5)
        password_entry = ctk.CTkEntry(tab, show='*')
        password_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(tab, text='Confirm Password').grid(row=3, column=0, padx=10, pady=5)
        confirm_password_entry = ctk.CTkEntry(tab, show='*')
        confirm_password_entry.grid(row=3, column=1, padx=10, pady=5)

        register_command = self.register_client if user_type == 'client' else self.register_seller
        back_command = self.master.create_login_frame
        ctk.CTkLabel(tab, text='').grid(row=4, column=0, padx=10, pady=1)

        ctk.CTkButton(tab, text='Register', command=register_command).grid(row=5, column=0, columnspan=2, pady=10)
        ctk.CTkButton(tab, text='Back to Login', command=back_command).grid(row=6, column=0, columnspan=2, pady=10)

        if user_type == 'client':
            self.client_email_entry = email_entry
            self.client_password_entry = password_entry
            self.client_confirm_password_entry = confirm_password_entry
        else:
            self.seller_email_entry = email_entry
            self.seller_password_entry = password_entry
            self.seller_confirm_password_entry = confirm_password_entry

    def register_client(self):
        self.register('client')

    def register_seller(self):
        self.register('seller')

    def register(self, user_type):
        email, password, confirm_password = self.get_registration_entries(user_type)

        if password != confirm_password:
            self.show_error_dialog('Passwords do not match!')
            return

        url = f'http://localhost:8080/api/{user_type}/register'
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            self.handle_successful_registration(response.json(), user_type, email, password)
        else:
            self.show_error_dialog('Registration failed!')

    def get_registration_entries(self, user_type):
        if user_type == 'client':
            return self.client_email_entry.get(), self.client_password_entry.get(), self.client_confirm_password_entry.get()
        else:
            return self.seller_email_entry.get(), self.seller_password_entry.get(), self.seller_confirm_password_entry.get()

    def handle_successful_registration(self, user_data, user_type, email, password):
        if user_type == 'seller':
            self.master.user = Seller(id=user_data.get('id'), email=email, password=password)
            self.master.create_seller_main_frame()
        else:
            self.master.user = Client(id=user_data.get('id'), email=email, password=password)
            self.master.create_client_main_frame()

    def show_error_dialog(self, message):
        ErrorDialog(self, message=message).show()
