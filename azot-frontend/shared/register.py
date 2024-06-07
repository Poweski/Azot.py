import threading
from .utils import *
from app_settings import *


class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = adjust_window(350, 400, master)
        master.geometry(window_size)

        self.email_entry = None
        self.password_entry = None
        self.confirm_password_entry = None

        ctk.CTkLabel(self, text='Register', font=('Helvetica', 20, 'bold')).pack(pady=10)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=10, pady=10, fill='both', expand=True)

        self.client_tab = self.tabview.add('Client')
        self.seller_tab = self.tabview.add('Seller')

        self.create_registration_tab(self.client_tab, 'client')
        self.create_registration_tab(self.seller_tab, 'seller')

    def create_registration_tab(self, tab, user_type):
        self.master.user_type = user_type

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

        self.email_entry = email_entry
        self.password_entry = password_entry
        self.confirm_password_entry = confirm_password_entry

    def register_client(self):
        threading.Thread(target=self.register_function, args=('client',)).start()

    def register_seller(self):
        threading.Thread(target=self.register_function, args=('seller',)).start()

    def register_function(self, user_type):
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            self.password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
            self.master.after(0, show_error_dialog, 'Passwords do not match!')
            return

        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/{user_type}/register'
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            self.master.after(0, self.handle_successful_registration)
        elif response.status_code == 400:
            self.master.after(0, show_error_dialog, response.json().get('error'))
        else:
            self.master.after(0, show_error_dialog, 'Server error!')

    @staticmethod
    def handle_successful_registration():
        show_success_dialog(f'Activation link has been sent to your email')
