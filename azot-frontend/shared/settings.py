from .utils import *
from app_settings import *


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.scale_option_menu = None

        self.main_frame = None
        self.password_entry = None
        self.confirm_password_entry = None

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
        ctk.CTkLabel(title_frame, text='').pack()
        title_label = ctk.CTkLabel(title_frame, text='Settings', font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=1)
        ctk.CTkLabel(title_frame, text='').pack()

    def create_view_frame(self):
        view_frame = ctk.CTkFrame(self.main_frame)
        view_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        ctk.CTkLabel(view_frame, text='').pack()
        ctk.CTkLabel(view_frame, text='Change View', font=('Helvetica', 20)).pack(padx=10, pady=10)
        ctk.CTkLabel(view_frame, text='').pack()
        self.create_scaling_option(view_frame)
        self.create_theme_option(view_frame)
        self.create_fullscreen_option(view_frame)

    def create_scaling_option(self, parent):
        scale_label = ctk.CTkLabel(parent, text='Application scaling:')
        scale_label.pack(padx=10)
        scale_values = ['75%', '100%', '125%', '150%', '200%']
        scale_option_menu = ctk.CTkOptionMenu(parent, values=scale_values, command=self.change_scaling)
        scale_option_menu.set(self.master.scaling)
        scale_option_menu.pack(padx=10, pady=10)

    def create_theme_option(self, parent):
        theme_label = ctk.CTkLabel(parent, text='Theme:')
        theme_label.pack(padx=10)
        theme_option_menu = ctk.CTkOptionMenu(parent, values=['Light', 'Dark', 'System'],command=self.change_theme)
        theme_option_menu.set(self.master.theme)
        theme_option_menu.pack(padx=10, pady=10)

    def create_fullscreen_option(self, parent):
        fullscreen_label = ctk.CTkLabel(parent, text='Fullscreen:')
        fullscreen_label.pack(padx=10)
        fullscreen_option_menu = ctk.CTkOptionMenu(parent, values=['Off', 'On'], command=self.change_fullscreen)
        fullscreen_option_menu.set(self.master.fullscreen)
        fullscreen_option_menu.pack(padx=10, pady=10)

    def create_password_frame(self):
        password_frame = ctk.CTkFrame(self.main_frame)
        password_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        ctk.CTkLabel(password_frame, text='').pack()
        ctk.CTkLabel(password_frame, text='Change Password', font=('Helvetica', 20)).pack(padx=10, pady=10)
        ctk.CTkLabel(password_frame, text='').pack()
        self.create_password_entries(password_frame)
        self.create_password_button(password_frame)

    def create_password_entries(self, parent):
        password_label = ctk.CTkLabel(parent, text='New password:')
        password_label.pack(padx=10)
        self.password_entry = ctk.CTkEntry(parent, show='*')
        self.password_entry.pack(padx=10, pady=10)

        confirm_password_label = ctk.CTkLabel(parent, text='Confirm password:')
        confirm_password_label.pack(padx=10)
        self.confirm_password_entry = ctk.CTkEntry(parent, show='*')
        self.confirm_password_entry.pack(padx=10, pady=10)

    def create_password_button(self, parent):
        ctk.CTkLabel(parent, text='').pack()
        change_password_button = ctk.CTkButton(parent, text='Submit', command=self.change_password)
        change_password_button.pack(padx=10, pady=10)

    def create_bottom_frame(self):
        bottom_frame = ctk.CTkFrame(self.main_frame)
        bottom_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        ctk.CTkLabel(bottom_frame, text='').pack()
        back_button = ctk.CTkButton(bottom_frame, text='Back', command=self.create_user_main_frame)
        back_button.pack(pady=1)
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
        scale_factor = float(value.strip('%')) / 100
        ctk.set_widget_scaling(scale_factor)
        self.master.scaling = value

    def change_theme(self, value):
        ctk.set_appearance_mode(value.lower())
        self.master.theme = value

    def change_password(self):
        if self.password_entry.get() != self.confirm_password_entry.get():
            self.password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
            show_error_dialog('Passwords do not match')
            return

        id = self.master.user.id
        password = self.password_entry.get()
        type = self.master.user_type
        url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/{id}/change_password'
        data = {'password': password, 'type': type}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            self.master.after(0, show_success_dialog)
        elif response.status_code == 400:
            self.master.after(0, show_error_dialog, response.json().get('error'))
        else:
            self.master.after(0, show_error_dialog, 'Password change failed')

        self.password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0, 'end')
