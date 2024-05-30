import customtkinter as ctk
from ConfirmDialog import ConfirmDialog
from utils import adjust_window
from SearchBar import SearchBar


class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = adjust_window(800, 600, master)
        master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color="#1c1c1c")
        main_frame.pack(fill="both", expand=True)

        left_frame = ctk.CTkFrame(main_frame, corner_radius=0)
        left_frame.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nswe")
        ctk.CTkLabel(left_frame, text="Azot", font=('Helvetica', 20)).pack(padx=20, pady=10)
        ctk.CTkLabel(left_frame, text="Your balance:", font=('Helvetica', 15)).pack(padx=20, pady=10)
        ctk.CTkLabel(left_frame, text="0", font=('Helvetica', 15)).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Profile', command=master.create_client_profile_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Messages', command=master.create_messages_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Notifications', command=master.create_notifications_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Favorites', command=master.create_favorites_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Cart', command=master.create_cart_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Orders', command=master.create_orders_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Options', command=master.create_options_frame).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text='Log Out', command=self.log_out).pack(padx=20, pady=10)
        ctk.CTkButton(left_frame, text="Close App", command=self.quit).pack(padx=20, pady=10)

        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(top_frame, text='Welcome to Azot!', font=('Helvetica', 20)).pack(pady=10)

        search_frame = ctk.CTkFrame(main_frame)
        search_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.search_bar = SearchBar(search_frame, search_callback=self.handle_search)
        self.search_bar.pack(fill="x")

        offers_frame = ctk.CTkFrame(main_frame, fg_color="#313335")
        offers_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(offers_frame, text='Popular offers', font=('Helvetica', 18)).pack(pady=10)
        # TODO: Show random offers

        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=0)
        main_frame.rowconfigure(1, weight=0)
        main_frame.rowconfigure(2, weight=1)

    def handle_search(self, query):
        pass

    def log_out(self):
        dialog = ConfirmDialog(self, title="Log Out", message="Are you sure you want to log out?")
        if dialog.show():
            self.master.create_login_frame()

    def quit(self):
        dialog = ConfirmDialog(self, title="Quit", message="Are you sure you want to exit?")
        if dialog.show():
            self.master.quit()
