from utils import *
import requests


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        window_size = adjust_window(800, 600, master)
        master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        main_frame.pack(fill='both', expand=True)

        top_frame = ctk.CTkFrame(main_frame)
        top_frame.pack(fill='both', expand=True, pady=20, padx=20)

        profile_label = ctk.CTkLabel(top_frame, text='Profile', font=('Helvetica', 24))
        profile_label.pack(pady=20)

        ctk.CTkLabel(top_frame, text='Organization').pack(pady=5)
        self.organization_entry = ctk.CTkEntry(top_frame, width=260)
        self.organization_entry.pack(pady=5)

        ctk.CTkLabel(top_frame, text='Phone').pack(pady=5)
        self.phone_entry = ctk.CTkEntry(top_frame, width=260)
        self.phone_entry.pack(pady=5)

        ctk.CTkLabel(top_frame, text='Address').pack(pady=5)
        self.address_entry = ctk.CTkEntry(top_frame, width=260)
        self.address_entry.pack(pady=5)

        ctk.CTkLabel(top_frame, text='ID').pack(pady=5)
        self.id_entry = ctk.CTkEntry(top_frame, width=260)
        self.id_entry.pack(pady=5)

        ctk.CTkLabel(top_frame, text='Email').pack(pady=5)
        self.email_entry = ctk.CTkEntry(top_frame, width=260)
        self.email_entry.pack(pady=5)

        ctk.CTkLabel(top_frame, text='').pack(pady=5)
        self.edit_button = ctk.CTkButton(top_frame, text='Edit', command=self.toggle_edit_mode)
        self.edit_button.pack(pady=5)

        self.back_button = ctk.CTkButton(top_frame, text='Back', command=master.create_seller_main_frame)
        self.back_button.pack(pady=5)
        ctk.CTkLabel(top_frame, text='').pack(pady=5)

        self.load_profile()
        self.edit_mode = False
        self.enable_buttons(False)

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.enable_buttons(self.edit_mode)
        if self.edit_mode:
            self.edit_button.configure(text='Submit')
            self.back_button.configure(state='disabled')
        else:
            self.save_profile()
            self.edit_button.configure(text='Edit')
            self.back_button.configure(state='normal')

    def enable_buttons(self, state):
        state = 'normal' if state else 'disabled'
        self.organization_entry.configure(state=state)
        self.phone_entry.configure(state=state)
        self.address_entry.configure(state=state)

    def load_profile(self):
        try:
            self.id_entry.insert(0, f'{self.master.user.id}')
            self.email_entry.insert(0, f'{self.master.user.email}')
            seller_info = self.master.user.seller_info
            if seller_info:
                if seller_info.organization:
                    self.organization_entry.insert(0, seller_info.organization)
                if seller_info.phone:
                    self.phone_entry.delete(0, 'end')
                    self.phone_entry.insert(0, seller_info.phone)
                if seller_info.address:
                    self.address_entry.delete(0, 'end')
                    self.address_entry.insert(0, seller_info.address)

        except requests.exceptions.RequestException as e:
            error = ErrorDialog(self, message=f'Failed to load profile: {e}!')
            error.show()
        finally:
            self.id_entry.configure(state='disabled')
            self.email_entry.configure(state='disabled')

    def save_profile(self):
        id = self.master.user.id
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        organization = self.organization_entry.get()

        data = {
            'organization': organization,
            'address': address,
            'phone': phone
        }

        url = f'http://localhost:8080/api/seller/{id}'
        response = requests.put(url, json=data)

        if response.status_code == 200:
            # TODO actualization issues
            self.master.user.phone = phone
            self.master.user.address = address
            self.master.user.organization = organization
            InfoDialog(self, title='Success', message='Profile updated successfully').show()
        else:
            self.load_profile()
            ErrorDialog(self, message='Failed to update profile!').show()
