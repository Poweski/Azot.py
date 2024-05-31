from utils import *


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.scale_optionmenu = None

        window_size = adjust_window(800, 600, master)
        master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        main_frame.pack(fill='both', expand=True)

        title_frame = ctk.CTkFrame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nswe')

        title_label = ctk.CTkLabel(title_frame, text='Settings', font=('Helvetica', 24))
        title_label.pack(pady=10)

        view_frame = ctk.CTkFrame(main_frame)
        view_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nswe')

        ctk.CTkLabel(view_frame, text='Change View', font=('Helvetica', 20)).pack(padx=10, pady=10)

        ctk.CTkLabel(view_frame, text='').pack()
        self.scale_label = ctk.CTkLabel(view_frame, text='Application scaling:')
        self.scale_label.pack(padx=10)
        scale_values = ['75%', '100%', '125%', '150%', '200%']
        self.scale_optionmenu = ctk.CTkOptionMenu(view_frame, values=scale_values, command=self.change_scaling)
        self.scale_optionmenu.set(master.scaling)
        self.scale_optionmenu.pack(padx=10, pady=10)

        ctk.CTkLabel(view_frame, text='').pack()
        self.theme_label = ctk.CTkLabel(view_frame, text='Theme:')
        self.theme_label.pack(padx=10)
        self.theme_optionmenu = ctk.CTkOptionMenu(view_frame, values=['Light', 'Dark', 'System'], command=self.change_theme)
        self.theme_optionmenu.set(master.theme)
        self.theme_optionmenu.pack(padx=10, pady=10)

        ctk.CTkLabel(view_frame, text='').pack()
        self.fullscreen_label = ctk.CTkLabel(view_frame, text='Fullscreen:')
        self.fullscreen_label.pack(padx=10)
        self.fullscreen_optionmenu = ctk.CTkOptionMenu(view_frame, values=['Off', 'On'], command=self.change_fullscreen)
        self.fullscreen_optionmenu.set(master.fullscreen)
        self.fullscreen_optionmenu.pack(padx=10, pady=10)

        password_frame = ctk.CTkFrame(main_frame)
        password_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nswe')

        ctk.CTkLabel(password_frame, text='Change Password', font=('Helvetica', 20)).pack(padx=10, pady=10)

        ctk.CTkLabel(password_frame, text='').pack()
        self.password_label = ctk.CTkLabel(password_frame, text='New password:')
        self.password_label.pack(padx=10)
        self.password_entry = ctk.CTkEntry(password_frame, show='*')
        self.password_entry.pack(padx=10, pady=10)

        self.confirm_password_label = ctk.CTkLabel(password_frame, text='Confirm password:')
        self.confirm_password_label.pack(padx=10)
        self.confirm_password_entry = ctk.CTkEntry(password_frame, show='*')
        self.confirm_password_entry.pack(padx=10, pady=10)

        ctk.CTkLabel(password_frame, text='').pack()
        self.change_password_button = ctk.CTkButton(password_frame, text='Submit', command=self.change_password)
        self.change_password_button.pack(padx=10, pady=10)

        bottom_frame = ctk.CTkFrame(main_frame)
        bottom_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nswe')

        ctk.CTkLabel(bottom_frame, text='').pack()
        self.back_button = ctk.CTkButton(bottom_frame, text='Back', command=self.create_main_frame)
        self.back_button.pack(pady=1)
        ctk.CTkLabel(bottom_frame, text='').pack()

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=0)
        main_frame.rowconfigure(1, weight=1)

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

    def create_main_frame(self):
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
        # TODO change password and settings overall
        pass
