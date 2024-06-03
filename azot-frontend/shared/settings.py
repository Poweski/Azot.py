import requests
from .utils import *


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.scale_option_menu = None

        self.setup_window()
        self.create_main_frame()
        self.create_title_frame()
        self.create_view_frame()
        self.create_password_frame()
        self.create_bottom_frame()

    def setup_window(self):
        window_size = adjust_window(800, 600, self.master)
        self.master.geometry(window_size)

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        self.main_frame.pack(fill='both', expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

    def create_title_frame(self):
        title_frame = ctk.CTkFrame(self.main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        title_label = ctk.CTkLabel(title_frame, text='Settings', font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=10)

    def create_view_frame(self):
        view_frame = ctk.CTkFrame(self.main_frame)
        view_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        ctk.CTkLabel(view_frame, text='Change View', font=('Helvetica', 20)).pack(padx=10, pady=10)
        self.create_scaling_option(view_frame)
        self.create_theme_option(view_frame)
        self.create_fullscreen_option(view_frame)

    def create_scaling_option(self, parent):
        self.scale_label = ctk.CTkLabel(parent, text='Application scaling:')
        self.scale_label.pack(padx=10)
        scale_values = ['75%', '100%', '125%', '150%', '200%']
        self.scale_option_menu = ctk.CTkOptionMenu(parent, values=scale_values, command=self.change_scaling)
        self.scale_option_menu.set(self.master.scaling)
        self.scale_option_menu.pack(padx=10, pady=10)

    def create_theme_option(self, parent):
        self.theme_label = ctk.CTkLabel(parent, text='Theme:')
        self.theme_label.pack(padx=10)
        self.theme_option_menu = ctk.CTkOptionMenu(parent, values=['Light', 'Dark', 'System'],
                                                   command=self.change_theme)
        self.theme_option_menu.set(self.master.theme)
        self.theme_option_menu.pack(padx=10, pady=10)

    def create_fullscreen_option(self, parent):
        self.fullscreen_label = ctk.CTkLabel(parent, text='Fullscreen:')
        self.fullscreen_label.pack(padx=10)
        self.fullscreen_option_menu = ctk.CTkOptionMenu(parent, values=['Off', 'On'], command=self.change_fullscreen)
        self.fullscreen_option_menu.set(self.master.fullscreen)
        self.fullscreen_option_menu.pack(padx=10, pady=10)

    def create_password_frame(self):
        password_frame = ctk.CTkFrame(self.main_frame)
        password_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        ctk.CTkLabel(password_frame, text='Change Password', font=('Helvetica', 20)).pack(padx=10, pady=10)
        self.create_password_entries(password_frame)
        self.create_password_button(password_frame)

    def create_password_entries(self, parent):
        self.password_label = ctk.CTkLabel(parent, text='New password:')
        self.password_label.pack(padx=10)
        self.password_entry = ctk.CTkEntry(parent, show='*')
        self.password_entry.pack(padx=10, pady=10)

        self.confirm_password_label = ctk.CTkLabel(parent, text='Confirm password:')
        self.confirm_password_label.pack(padx=10)
        self.confirm_password_entry = ctk.CTkEntry(parent, show='*')
        self.confirm_password_entry.pack(padx=10, pady=10)

    def create_password_button(self, parent):
        ctk.CTkLabel(parent, text='').pack()
        self.change_password_button = ctk.CTkButton(parent, text='Submit', command=self.change_password)
        self.change_password_button.pack(padx=10, pady=10)

    def create_bottom_frame(self):
        bottom_frame = ctk.CTkFrame(self.main_frame)
        bottom_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        ctk.CTkLabel(bottom_frame, text='').pack()
        self.back_button = ctk.CTkButton(bottom_frame, text='Back', command=self.create_user_main_frame)
        self.back_button.pack(pady=1)
        ctk.CTkLabel(bottom_frame, text='').pack()

    def change_fullscreen(self, value):
        if value == 'Off':
            self.master.fullscreen = 'Off'
            self.master.attributes('-fullscreen', False)
            self.master.geometry("800x600")
        else:
            self.master.fullscreen = 'On'
            self.master.attributes('-fullscreen', True)
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            self.master.geometry(f"{screen_width}x{screen_height}")

    def create_user_main_frame(self):
        if self.master.user_type == 'client':
            self.master.create_client_main_frame()
        else:
            self.master.create_seller_main_frame()

    def change_scaling(self, value):
        self.master.scaling = value
        scale_factor = float(value.strip('%')) / 100
        ctk.set_widget_scaling(scale_factor)

    def change_theme(self, value):
        ctk.set_appearance_mode(value.lower())
        self.master.theme = value

    def change_password(self):
        if self.password_entry.get() != self.confirm_password_entry.get():
            self.show_error_dialog('Passwords do not match')
            return

        id = self.master.user.id
        password = self.password_entry.get()
        type = self.master.user_type
        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/{id}/change_password'
        data = {'password': password, 'type': type}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            self.master.after(0, self.show_success_dialog)
        elif response.status_code == 400:
            self.master.after(0, self.show_error_dialog, response.json().get('error'))
        else:
            self.master.after(0, self.show_error_dialog, 'Password change failed')
        pass

    def show_success_dialog(self):
        success = InfoDialog(self, title='Success', message='Password changed successfully')
        success.show()

    def show_error_dialog(self, message):
        error = ErrorDialog(self, message=message)
        error.show()
