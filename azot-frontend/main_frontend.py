import seller_menu
import client_menu
import seller_profile
import client_profile
from login import LoginFrame
from register import RegistrationFrame
from add_product import AddProductFrame
from settings import SettingsFrame
from utils import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Azot')
        window_size = adjust_window(350, 350, self)
        self.geometry(window_size)
        self.resizable(False, False)
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        self.scaling = '100%'
        self.theme = 'Dark'

        self.user = None

        self.login_frame = None
        self.registration_frame = None
        self.main_frame = None
        self.add_product_frame = None
        self.profile_frame = None
        self.settings_frame = None

        self.create_login_frame()

    def create_login_frame(self):
        self.clear_frame()
        self.login_frame = LoginFrame(self)
        self.login_frame.pack(fill='both', expand=True)

    def create_registration_frame(self):
        self.clear_frame()
        self.registration_frame = RegistrationFrame(self)
        self.registration_frame.pack(fill='both', expand=True)

    def create_seller_main_frame(self):
        self.clear_frame()
        self.main_frame = seller_menu.MainMenuFrame(self)
        self.main_frame.pack(fill='both', expand=True)

    def create_client_main_frame(self):
        self.clear_frame()
        self.main_frame = client_menu.MainMenuFrame(self)
        self.main_frame.pack(fill='both', expand=True)

    def create_add_product_frame(self):
        self.clear_frame()
        self.add_product_frame = AddProductFrame(self)
        self.add_product_frame.pack(fill='both', expand=True)

    def create_client_profile_frame(self):
        self.clear_frame()
        self.profile_frame = client_profile.ProfileFrame(self)
        self.profile_frame.pack(fill='both', expand=True)

    def create_seller_profile_frame(self):
        self.clear_frame()
        self.profile_frame = seller_profile.ProfileFrame(self)
        self.profile_frame.pack(fill='both', expand=True)

    def create_messages_frame(self):
        pass

    def create_notifications_frame(self):
        pass

    def create_favorites_frame(self):
        pass

    def create_cart_frame(self):
        pass

    def create_orders_frame(self):
        pass

    def create_announcements_frame(self):
        pass

    def create_settings_frame(self):
        self.clear_frame()
        self.settings_frame = SettingsFrame(self)
        self.settings_frame.pack(fill='both', expand=True)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def quit(self):
        self.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()
