import customtkinter as ctk
from shared import utils
import requests
from app_settings import *


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.edit_mode = False

        self.setup_window()
        self.create_main_frame()
        self.create_top_frame()
        self.create_info_frame()
        self.create_balance_frame()
        self.create_bottom_frame()

        self.load_profile()
        self.enable_buttons(False)

    def setup_window(self):
        window_size = utils.adjust_window(800, 600, self.master)
        self.master.geometry(window_size)

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        self.main_frame.pack(fill='both', expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

    def create_top_frame(self):
        top_frame = ctk.CTkFrame(self.main_frame)
        top_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        profile_label = ctk.CTkLabel(top_frame, text='Profile', font=('Helvetica', 24, 'bold'))
        profile_label.pack(pady=20)

    def create_info_frame(self):
        info_frame = ctk.CTkFrame(self.main_frame)
        info_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.name_entry = self.create_labeled_entry(info_frame, 'Name')
        self.surname_entry = self.create_labeled_entry(info_frame, 'Surname')
        self.phone_entry = self.create_labeled_entry(info_frame, 'Phone')
        self.address_entry = self.create_labeled_entry(info_frame, 'Address')

        self.edit_button = ctk.CTkButton(info_frame, text='Edit', command=self.toggle_edit_mode)
        self.edit_button.pack(padx=10, pady=5)

    def create_balance_frame(self):
        balance_frame = ctk.CTkFrame(self.main_frame)
        balance_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        #self.id_entry = self.create_labeled_entry(balance_frame, 'ID', state='disabled')
        self.email_entry = self.create_labeled_entry(balance_frame, 'Email', state='disabled')

        ctk.CTkLabel(balance_frame, text='Your balance:', font=('Helvetica', 18)).pack(padx=10, pady=5)
        self.balance_entry = ctk.CTkEntry(balance_frame, justify='right')
        self.balance_entry.pack(padx=10, pady=5)
        self.balance_entry.insert(0, self.master.user.client_info.balance)
        self.balance_entry.configure(state='disabled')

        self.balance_button = ctk.CTkButton(balance_frame, text='Top Up', command=self.top_up)
        self.balance_button.pack(pady=10)

    def create_bottom_frame(self):
        bottom_frame = ctk.CTkFrame(self.main_frame)
        bottom_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.back_button = ctk.CTkButton(bottom_frame, text='Back', command=self.master.create_client_main_frame)
        self.back_button.pack(pady=1)

    def create_labeled_entry(self, frame, label_text, state='normal'):
        ctk.CTkLabel(frame, text=label_text).pack(padx=10)
        entry = ctk.CTkEntry(frame, width=260, state=state)
        entry.pack(padx=10, pady=1)
        return entry

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.enable_buttons(self.edit_mode)
        if self.edit_mode:
            self.edit_button.configure(text='Submit', fg_color='red', hover_color='#8B0000')
            self.back_button.configure(state='disabled')
            self.balance_button.configure(state='disabled')
        else:
            self.save_profile()
            self.edit_button.configure(text='Edit', fg_color='#1f538d', hover_color='#14375e')
            self.back_button.configure(state='normal')
            self.balance_button.configure(state='normal')

    def enable_buttons(self, state):
        state = 'normal' if state else 'disabled'
        for entry in [self.name_entry, self.surname_entry, self.phone_entry, self.address_entry, self.email_entry]:
            entry.configure(state=state)

    def load_profile(self):
        try:
            self.enable_buttons(True)
            #self.id_entry.insert(0, self.master.user.id)
            self.email_entry.insert(0, self.master.user.email)

            client_info = self.master.user.client_info
            if client_info:
                if client_info.name:
                    self.name_entry.insert(0, client_info.name)
                if client_info.surname:
                    self.surname_entry.insert(0, client_info.surname)
                if client_info.phone:
                    self.phone_entry.insert(0, client_info.phone)
                if client_info.address:
                    self.address_entry.insert(0, client_info.address)
                self.balance_entry.insert(0, client_info.balance)
        except requests.exceptions.RequestException as e:
            utils.ErrorDialog(self, message=f'Failed to load profile: {e}!').show()
        finally:
            self.enable_buttons(False)

    def save_profile(self):
        id = self.master.user.id
        data = {
            'name': self.name_entry.get(),
            'surname': self.surname_entry.get(),
            'address': self.address_entry.get(),
            'phone': self.phone_entry.get()
        }

        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/client/{id}'
        response = requests.put(url, json=data)

        if response.status_code == 200:
            client_info = self.master.user.client_info
            client_info.name = data['name']
            client_info.surname = data['surname']
            client_info.phone = data['phone']
            client_info.address = data['address']
            utils.InfoDialog(self, title='Success', message='Profile updated successfully').show()
        elif response.status_code == 400:
            utils.ErrorDialog(self, message=response.json().get('error')).show()
        else:
            utils.ErrorDialog(self, message='Failed to update profile!').show()

        self.load_profile()

    def top_up(self):
        try:
            value = utils.InputDialog(self, title='Recharge', message='Enter the amount:').show()
            balance_amount = float(value)
            client_id = self.master.user.id
            data = {'balance': balance_amount}
            url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/client/{client_id}/balance'
            response = requests.post(url, json=data)

            if response.status_code == 200:
                self.master.user.client_info.balance += balance_amount
                self.update_balance_entry()
                utils.InfoDialog(self, title='Success', message='Balance topped up successfully').show()
            elif response.status_code == 400:
                utils.ErrorDialog(self, message=response.json().get('error')).show()
            else:
                utils.ErrorDialog(self, message='Failed to top up balance!').show()

        except ValueError:
            utils.ErrorDialog(self, message='Please enter a valid balance amount!').show()

    def update_balance_entry(self):
        self.balance_entry.configure(state='normal')
        self.balance_entry.delete(0, 'end')
        self.balance_entry.insert(0, f'{self.master.user.client_info.balance}')
        self.balance_entry.configure(state='disabled')
