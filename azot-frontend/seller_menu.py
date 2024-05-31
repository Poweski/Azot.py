from utils import *


class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = adjust_window(800, 600, master)
        master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        main_frame.pack(fill='both', expand=True)

        left_frame = ctk.CTkFrame(main_frame, corner_radius=0)
        left_frame.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky='nswe')
        ctk.CTkLabel(left_frame, text='Azot', font=('Helvetica', 20)).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Profile', command=master.create_seller_profile_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Add Product', command=master.create_add_product_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Messages', command=master.create_messages_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Orders', command=master.create_orders_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Settings', command=master.create_settings_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Log Out', command=self.log_out).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Close App', command=self.quit).pack(padx=20, pady=10)

        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        ctk.CTkLabel(top_frame, text='Welcome to Azot!', font=('Helvetica', 20)).pack(pady=10)

        offers_frame = ctk.CTkFrame(main_frame, fg_color='#313335')
        offers_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        ctk.CTkLabel(offers_frame, text='Your products:', font=('Helvetica', 18)).pack(pady=10)

        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=0)
        main_frame.rowconfigure(1, weight=1)

    def log_out(self):
        dialog = ConfirmDialog(self, title='Log Out', message='Are you sure you want to log out?')
        if dialog.show():
            self.master.create_login_frame()

    def quit(self):
        dialog = ConfirmDialog(self, title='Quit', message='Are you sure you want to exit?')
        if dialog.show():
            self.master.quit()
