from .utils import *
from app_settings import *
import requests


class ForgotPasswordFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = adjust_window(350, 400, master)
        master.geometry(window_size)

        ctk.CTkLabel(self, text='Forgot Password', font=('Helvetica', 20, 'bold')).pack(pady=10)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=10, pady=10, fill='both', expand=True)

        self.client_tab = self.tabview.add('Client')
        self.seller_tab = self.tabview.add('Seller')

        self.create_forgot_password_tab(self.client_tab, 'client')
        self.create_forgot_password_tab(self.seller_tab, 'seller')

    def create_forgot_password_tab(self, tab, user_type):
        ctk.CTkLabel(tab, text='').grid(row=0, column=0, padx=10, pady=1)
        ctk.CTkLabel(tab, text='Email        ').grid(row=1, column=0, padx=10, pady=5)
        email_entry = ctk.CTkEntry(tab)
        email_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(tab, text='').grid(row=2, column=0, padx=10, pady=1)

        if user_type == 'client':
            self.client_email_entry = email_entry
            ctk.CTkButton(tab, text='Submit', command=self.forgot_password).grid(row=3, column=1, pady=10)
        else:
            self.seller_email_entry = email_entry
            ctk.CTkButton(tab, text='Submit', command=self.forgot_password).grid(row=3, column=1, pady=10)

        ctk.CTkButton(tab, text='Back to Login', command=self.master.create_login_frame).grid(row=4, column=1, pady=10)

    def forgot_password(self):
        user_type = self.master.user_type
        email = self.client_email_entry.get() if user_type == 'client' else self.seller_email_entry.get()
        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/password/{user_type}'
        data = {'email': email}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            self.show_success_dialog()
        elif response.status_code == 400:
            self.show_error_dialog(response.json().get('error'))
        else:
            self.show_error_dialog('Server Error')

    def show_error_dialog(self, message):
        error = ErrorDialog(self, message=message)
        error.show()

    def show_success_dialog(self):
        success = InfoDialog(self, message='Message has been sent to your email.')
        success.show()