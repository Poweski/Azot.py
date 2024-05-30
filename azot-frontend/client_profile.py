import customtkinter as ctk
from tkinter import messagebox
from utils import adjust_window
import requests


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        window_size = adjust_window(800, 600, master)
        master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color="#1c1c1c")
        main_frame.pack(fill="both", expand=True)

        left_frame = ctk.CTkFrame(main_frame)
        left_frame.grid(row=0, column=0, rowspan=1, padx=10, pady=10, sticky="nswe")
        profile_label = ctk.CTkLabel(left_frame, text='Profile', font=('Helvetica', 20))
        profile_label.grid(row=0, column=0, columnspan=2, pady=20)

        ctk.CTkLabel(left_frame, text='Name').grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(left_frame)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(left_frame, text='Surname').grid(row=2, column=0, padx=10, pady=5)
        self.surname_entry = ctk.CTkEntry(left_frame)
        self.surname_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(left_frame, text='Phone').grid(row=3, column=0, padx=10, pady=5)
        self.phone_entry = ctk.CTkEntry(left_frame)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(left_frame, text='Address').grid(row=4, column=0, padx=10, pady=5)
        self.address_entry = ctk.CTkEntry(left_frame)
        self.address_entry.grid(row=4, column=1, padx=10, pady=5)

        ctk.CTkLabel(left_frame, text='ID').grid(row=5, column=0, padx=10, pady=5)
        self.id_entry = ctk.CTkEntry(left_frame, state='disabled')
        self.id_entry.grid(row=5, column=1, padx=10, pady=5)

        ctk.CTkLabel(left_frame, text='Email').grid(row=6, column=0, padx=10, pady=5)
        self.email_entry = ctk.CTkEntry(left_frame, state='disabled')
        self.email_entry.grid(row=6, column=1, padx=10, pady=5)

        self.edit_mode = False
        self.enable_buttons(False)

        ctk.CTkLabel(left_frame, text='').grid(row=7, column=0, columnspan=2, pady=0)
        self.edit_button = ctk.CTkButton(left_frame, text='Edit', command=self.toggle_edit_mode)
        self.edit_button.grid(row=8, column=0, columnspan=2, pady=10)
        self.back_button = ctk.CTkButton(left_frame, text='Back', command=master.create_client_main_frame)
        self.back_button.grid(row=9, column=0, columnspan=2, pady=10)

        image_frame = ctk.CTkFrame(main_frame)
        image_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.enable_buttons(self.edit_mode)
        if self.edit_mode:
            self.edit_button.configure(text='Submit')
            self.back_button.configure(state='disabled')
        else:
            self.edit_button.configure(text='Edit')
            self.back_button.configure(state='normal')

    def enable_buttons(self, state):
        state = 'normal' if state else 'disabled'
        self.name_entry.configure(state=state)
        self.surname_entry.configure(state=state)
        self.phone_entry.configure(state=state)
        self.address_entry.configure(state=state)

    def load_profile(self):
        url = f"https://localhost:8080/api/client/{self.master.active_user_id}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()["content"]

            self.surname_entry.delete(0, ctk.END)
            self.surname_entry.insert(0, data["email"])

            client_info = data["client_info"]
            self.phone_entry.delete(0, ctk.END)
            self.phone_entry.insert(0, client_info["phone"])
            self.address_entry.delete(0, ctk.END)
            self.address_entry.insert(0, client_info["address"])

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to load profile: {e}")

    def save_profile(self):
        id_ = self.name_entry.get()
        email = self.surname_entry.get()
        organization = self.phone_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()

        data = {
            "id": id_,
            "email": email,
            "seller_info": {
                "organization": organization,
                "phone": phone,
                "address": address
            }
        }

        url = f'http://localhost:8080/api/client/{self.master.active_user_id}'
        response = requests.put(url, json=data)

        if response.status_code == 200:
            messagebox.showinfo('Success', 'Profile updated successfully')
        else:
            messagebox.showerror('Error', 'Failed to update profile')
