import customtkinter as ctk


class SearchBar(ctk.CTkFrame):
    def __init__(self, master, search_callback):
        super().__init__(master)
        self.master = master
        self.search_callback = search_callback

        self.entry = ctk.CTkEntry(self)
        self.entry.grid(column=0, row=0, columnspan=3, sticky='we')

        self.search_button = ctk.CTkButton(self, text="Search", command=self.search)
        self.search_button.grid(padx=5, pady=5, column=4, row=0)

    def search(self):
        pass
