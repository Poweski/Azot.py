import customtkinter as ctk
from tkinter import messagebox
import requests


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        ctk.CTkLabel(self, text='Profile', font=('Helvetica', 20)).grid(row=0, column=1, pady=10)

        ctk.CTkLabel(self, text='ID').grid(row=1, column=0, padx=10, pady=5)
        self.id_entry = ctk.CTkEntry(self)
        self.id_entry.grid(row=1, column=1, padx=10, pady=5)
        self.id_entry.insert(0, "example_id")

        ctk.CTkLabel(self, text='Email').grid(row=2, column=0, padx=10, pady=5)
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)
        self.email_entry.insert(0, "example_email")

        ctk.CTkLabel(self, text='Organization').grid(row=3, column=0, padx=10, pady=5)
        self.organization_entry = ctk.CTkEntry(self)
        self.organization_entry.grid(row=3, column=1, padx=10, pady=5)
        self.organization_entry.insert(0, "example_organization")

        ctk.CTkLabel(self, text='Phone').grid(row=4, column=0, padx=10, pady=5)
        self.phone_entry = ctk.CTkEntry(self)
        self.phone_entry.grid(row=4, column=1, padx=10, pady=5)
        self.phone_entry.insert(0, "example_phone")

        ctk.CTkLabel(self, text='Address').grid(row=5, column=0, padx=10, pady=5)
        self.address_entry = ctk.CTkEntry(self)
        self.address_entry.grid(row=5, column=1, padx=10, pady=5)
        self.address_entry.insert(0, "example_address")

        ctk.CTkButton(self, text='Save', command=self.save_profile).grid(row=6, column=1, pady=10)
        ctk.CTkButton(self, text='Back', command=master.create_client_main_frame).grid(row=6, column=2, pady=10)

    def save_profile(self):
        id_ = self.id_entry.get()
        email = self.email_entry.get()
        organization = self.organization_entry.get()
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
