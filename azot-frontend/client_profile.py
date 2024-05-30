from utils import *
import requests


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        window_size = adjust_window(800, 600, master)
        master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color="#1c1c1c")
        main_frame.pack(fill="both", expand=True)

        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nswe")

        profile_label = ctk.CTkLabel(top_frame, text='Profile', font=('Helvetica', 24))
        profile_label.pack(pady=20)

        self.back_button = ctk.CTkButton(top_frame, text='Back', command=master.create_client_main_frame)
        self.back_button.pack(pady=10)

        info_frame = ctk.CTkFrame(main_frame)
        info_frame.grid(row=1, column=0, rowspan=1, padx=10, pady=10, sticky="nswe")

        ctk.CTkLabel(info_frame, text='Name').grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(info_frame)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(info_frame, text='Surname').grid(row=2, column=0, padx=10, pady=5)
        self.surname_entry = ctk.CTkEntry(info_frame)
        self.surname_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(info_frame, text='Phone').grid(row=3, column=0, padx=10, pady=5)
        self.phone_entry = ctk.CTkEntry(info_frame)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(info_frame, text='Address').grid(row=4, column=0, padx=10, pady=5)
        self.address_entry = ctk.CTkEntry(info_frame)
        self.address_entry.grid(row=4, column=1, padx=10, pady=5)

        ctk.CTkLabel(info_frame, text='ID').grid(row=5, column=0, padx=10, pady=5)
        self.id_entry = ctk.CTkEntry(info_frame)
        self.id_entry.grid(row=5, column=1, padx=10, pady=5)

        ctk.CTkLabel(info_frame, text='Email').grid(row=6, column=0, padx=10, pady=5)
        self.email_entry = ctk.CTkEntry(info_frame)
        self.email_entry.grid(row=6, column=1, padx=10, pady=5)

        ctk.CTkLabel(info_frame, text='').grid(row=7, column=0, columnspan=2, pady=0)
        self.edit_button = ctk.CTkButton(info_frame, text='Edit', command=self.toggle_edit_mode)
        self.edit_button.grid(row=8, column=0, columnspan=2, pady=10)

        balance_frame = ctk.CTkFrame(main_frame)
        balance_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(balance_frame, text='Your balance:', font=('Helvetica', 18)).pack(padx=10, pady=5)
        self.balance_entry = ctk.CTkEntry(balance_frame)
        self.balance_entry.pack(padx=10, pady=5)
        self.balance_entry.insert(0, '0')
        self.balance_entry.configure(state='disabled')

        self.balance_button = ctk.CTkButton(balance_frame, text='Top Up', command=self.top_up)
        self.balance_button.pack(pady=10)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=0)
        main_frame.rowconfigure(1, weight=1)

        self.load_profile()
        self.edit_mode = False
        self.enable_buttons(False)

    def top_up(self):
        pass

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
        self.name_entry.configure(state=state)
        self.surname_entry.configure(state=state)
        self.phone_entry.configure(state=state)
        self.address_entry.configure(state=state)

    def load_profile(self):
        try:
            self.id_entry.insert(0, f'{self.master.user.id}')
            self.email_entry.insert(0, f'{self.master.user.email}')
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
                self.balance_entry.insert(0, f'{client_info.balance}')

        except requests.exceptions.RequestException as e:
            error = ErrorDialog(self, message=f"Failed to load profile: {e}!")
            error.show()
        finally:
            self.id_entry.configure(state='disabled')
            self.email_entry.configure(state='disabled')

    def save_profile(self):
        id = self.master.user.id
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()

        data = {
            "name": name,
            "surname": surname,
            "address": address,
            "phone": phone
        }

        url = f'http://localhost:8080/api/client/{id}'
        response = requests.put(url, json=data)

        if response.status_code == 200:
            dialog = ConfirmDialog(self, title="Success", message="Profile updated successfully")
            dialog.show()
        else:
            print(response)
            error = ErrorDialog(self, message="Failed to update profile!")
            error.show()
