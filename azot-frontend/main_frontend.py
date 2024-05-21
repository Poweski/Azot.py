import customtkinter as ctk
from login import LoginFrame
from register import RegistrationFrame
from main_menu import MainMenuFrame
from product import AddProductFrame, SellProductFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Azot')
        self.geometry('500x400')

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        self.active_user_id = None

        self.create_login_frame()

    def create_login_frame(self):
        self.clear_frame()
        self.login_frame = LoginFrame(self)
        self.login_frame.pack(pady=20, padx=20, fill='both', expand=True)

    def create_registration_frame(self):
        self.clear_frame()
        self.registration_frame = RegistrationFrame(self)
        self.registration_frame.pack(pady=20, padx=20, fill='both', expand=True)

    def create_main_frame(self):
        self.clear_frame()
        self.main_frame = MainMenuFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill='both', expand=True)

    def create_add_product_frame(self):
        self.clear_frame()
        self.add_product_frame = AddProductFrame(self)
        self.add_product_frame.pack(pady=20, padx=20, fill='both', expand=True)

    def create_sell_product_frame(self):
        self.clear_frame()
        self.sell_product_frame = SellProductFrame(self)
        self.sell_product_frame.pack(pady=20, padx=20, fill='both', expand=True)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()
