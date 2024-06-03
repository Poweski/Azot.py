from .classes import *
from .utils import *
import requests
import threading


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = adjust_window(350, 400, master)
        master.geometry(window_size)

        ctk.CTkLabel(self, text='Login', font=('Helvetica', 20, 'bold')).pack(pady=10)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=10, pady=10, fill='both', expand=True)

        self.client_tab = self.tabview.add('Client')
        self.seller_tab = self.tabview.add('Seller')

        self.create_login_tab(self.client_tab, 'client')
        self.create_login_tab(self.seller_tab, 'seller')

    def create_login_tab(self, tab, user_type):
        ctk.CTkLabel(tab, text='').grid(row=0, column=0, padx=10, pady=1)
        ctk.CTkLabel(tab, text='Email').grid(row=1, column=0, padx=10, pady=5)
        email_entry = ctk.CTkEntry(tab)
        email_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(tab, text='Password').grid(row=2, column=0, padx=10, pady=5)
        password_entry = ctk.CTkEntry(tab, show='*')
        password_entry.grid(row=2, column=1, padx=10, pady=5)
        ctk.CTkLabel(tab, text='').grid(row=3, column=0, padx=10, pady=1)

        if user_type == 'client':
            self.client_email_entry = email_entry
            self.client_password_entry = password_entry
            ctk.CTkButton(tab, text='Login', command=self.login_client).grid(row=4, column=1, pady=10)
        else:
            self.seller_email_entry = email_entry
            self.seller_password_entry = password_entry
            ctk.CTkButton(tab, text='Login', command=self.login_seller).grid(row=4, column=1, pady=10)

        ctk.CTkButton(tab, text='Register', command=self.master.create_registration_frame).grid(row=5, column=1, pady=10)

        ctk.CTkButton(tab, text='Forgot Password?', command=self.master.create_forgot_password_frame).grid(row=6, column=1, pady=10)

    def login_client(self):
        thread = threading.Thread(target=self.login, args=('client',))
        thread.start()

    def login_seller(self):
        thread = threading.Thread(target=self.login, args=('seller',))
        thread.start()

    def login(self, user_type):
        self.master.user_type = user_type
        email = self.client_email_entry.get() if user_type == 'client' else self.seller_email_entry.get()
        password = self.client_password_entry.get() if user_type == 'client' else self.seller_password_entry.get()
        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/{user_type}/login'
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            self.master.after(0, self.handle_successful_login, response.json(), user_type, email, password)
        elif response.status_code == 400:
            self.master.after(0, self.show_error_dialog, response.json().get('error'))
        else:
            self.master.after(0, self.show_error_dialog, 'Server error')

    def handle_successful_login(self, response_data, user_type, email, password):
        user_data = response_data.get('content')
        if user_type == 'seller':
            self.master.user = self.create_seller_user(user_data, email, password)
            self.master.create_seller_main_frame()
        else:
            self.master.user = self.create_client_user(user_data, email, password)
            self.master.create_client_main_frame()

    @staticmethod
    def create_seller_user(user_data, email, password):
        seller_info_data = user_data.get('seller_info')
        seller_info = None

        if seller_info_data:
            seller_info = SellerInfo(
                organization=seller_info_data.get('organization'),
                phone=seller_info_data.get('phone'),
                address=seller_info_data.get('address')
            )
        return Seller(
            seller_id=user_data.get('id'),
            email=email,
            password=password,
            seller_info=seller_info,
            products=[]
        )

    @staticmethod
    def create_client_user(user_data, email, password):
        client_info_data = user_data.get('client_info')
        client_info = None
        if client_info_data:
            client_info = ClientInfo(
                name=client_info_data.get('name'),
                surname=client_info_data.get('surname'),
                phone=client_info_data.get('phone'),
                address=client_info_data.get('address'),
                balance=client_info_data.get('balance')
            )
        return Client(
            client_id=user_data.get('id'),
            email=email,
            password=password,
            client_info=client_info,
            cart=[]
        )

    def show_error_dialog(self, message):
        error = ErrorDialog(self, message=message)
        error.show()
