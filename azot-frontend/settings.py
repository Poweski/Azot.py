from utils import *


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.scale_label = ctk.CTkLabel(self, text="Application scaling:")
        self.scale_label.grid(row=0, column=0, padx=10, pady=10)
        scale_values = ["75%", "100%", "125%", "150%", "200%"]
        self.scale_optionmenu = ctk.CTkOptionMenu(self, values=scale_values, command=self.change_scaling)
        self.scale_optionmenu.set(master.scaling)
        self.scale_optionmenu.grid(row=0, column=1, padx=10, pady=10)

        self.theme_label = ctk.CTkLabel(self, text="Theme:")
        self.theme_label.grid(row=1, column=0, padx=10, pady=10)
        self.theme_optionmenu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"], command=self.change_theme)
        self.theme_optionmenu.set(master.theme)
        self.theme_optionmenu.grid(row=1, column=1, padx=10, pady=10)

        self.password_label = ctk.CTkLabel(self, text="New password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=10)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        self.confirm_password_label = ctk.CTkLabel(self, text="Confirm password:")
        self.confirm_password_label.grid(row=3, column=0, padx=10, pady=10)
        self.confirm_password_entry = ctk.CTkEntry(self, show="*")
        self.confirm_password_entry.grid(row=3, column=1, padx=10, pady=10)

        self.change_password_button = ctk.CTkButton(self, text="Change Password", command=self.change_password)
        self.change_password_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.back_button = ctk.CTkButton(self, text='Back', command=master.create_client_main_frame)
        self.back_button.grid(row=5, column=0, columnspan=2, pady=10)

    def change_scaling(self, value):
        self.master.scaling = value
        scale_factor = float(value.strip('%')) / 100
        ctk.set_widget_scaling(scale_factor)

    def change_theme(self, value):
        ctk.set_appearance_mode(value.lower())
        self.master.theme = value

    def change_password(self):
        pass
