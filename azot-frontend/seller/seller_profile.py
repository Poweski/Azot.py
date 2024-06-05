import customtkinter as ctk
from shared import utils
import requests
from app_settings import *


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_window()
        self.create_main_frame()
        self.create_top_frame()
        self.create_profile_form()
        self.create_buttons()

        self.load_profile()
        self.edit_mode = False
        self.enable_edit_fields(False)

    def setup_window(self):
        window_size = utils.adjust_window(800, 600, self.master)
        self.master.geometry(window_size)

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        self.main_frame.pack(fill='both', expand=True)

    def create_top_frame(self):
        self.top_frame = ctk.CTkFrame(self.main_frame)
        self.top_frame.pack(fill='both', expand=True, pady=20, padx=20)
        profile_label = ctk.CTkLabel(self.top_frame, text='Profile', font=('Helvetica', 24, 'bold'))
        profile_label.pack(pady=20)

    def create_profile_form(self):
        self.entries = {}
        labels = ["Organization", "Phone", "Address", "Email"]
        for label in labels:
            ctk.CTkLabel(self.top_frame, text=label).pack(pady=5)
            entry = ctk.CTkEntry(self.top_frame, width=260)
            entry.pack(pady=5)
            self.entries[label.lower()] = entry

    def create_buttons(self):
        ctk.CTkLabel(self.top_frame, text='').pack(pady=5)
        self.edit_button = ctk.CTkButton(self.top_frame, text='Edit', command=self.toggle_edit_mode)
        self.edit_button.pack(pady=5)
        self.back_button = ctk.CTkButton(self.top_frame, text='Back', command=self.master.create_seller_main_frame)
        self.back_button.pack(pady=5)
        ctk.CTkLabel(self.top_frame, text='').pack(pady=5)

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.enable_edit_fields(self.edit_mode)
        if self.edit_mode:
            self.edit_button.configure(text='Submit', fg_color='red', hover_color='#8B0000')
            self.back_button.configure(state='disabled')
        else:
            self.save_profile()
            self.edit_button.configure(text='Edit', fg_color='#1f538d', hover_color='#14375e')
            self.back_button.configure(state='normal')

    def enable_edit_fields(self, state):
        state = 'normal' if state else 'disabled'
        for key, entry in self.entries.items():
            if key not in ['id', 'email']:
                entry.configure(state=state)

    def load_profile(self):
        try:
            user = self.master.user
            self.entries['email'].delete(0, 'end')
            self.entries['email'].insert(0, user.email)
            seller_info = user.seller_info

            if seller_info:
                if seller_info.organization:
                    self.entries['organization'].delete(0, 'end')
                    self.entries['organization'].insert(0, seller_info.organization)
                if seller_info.phone:
                    self.entries['phone'].delete(0, 'end')
                    self.entries['phone'].insert(0, seller_info.phone)
                if seller_info.address:
                    self.entries['address'].delete(0, 'end')
                    self.entries['address'].insert(0, seller_info.address)

        except requests.RequestException as e:
            utils.ErrorDialog(self, message=f'Failed to load profile: {e}!').show()
        finally:
            self.entries['email'].configure(state='disabled')

    def save_profile(self):
        _id = self.master.user.id
        data = {key: entry.get() for key, entry in self.entries.items() if key not in ['id', 'email']}

        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/seller/{_id}'
        response = requests.put(url, json=data)

        if response.status_code == 200:
            user = self.master.user.seller_info
            user.organization = data['organization']
            user.phone = data['phone']
            user.address = data['address']
            utils.InfoDialog(self, title='Success', message='Profile updated successfully').show()
        elif response.status_code == 400:
            utils.ErrorDialog(self, message=response.json().get('error')).show()
        else:
            utils.ErrorDialog(self, message='Failed to update profile').show()

        self.load_profile()
