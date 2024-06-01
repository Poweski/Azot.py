import customtkinter as ctk
import requests
from shared import utils


class AddProductFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        window_size = utils.adjust_window(800, 600, self.master)
        self.master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        main_frame.pack(fill='both', expand=True)

        self.create_title_frame(main_frame)

        left_frame = ctk.CTkFrame(main_frame)
        left_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.create_left_frame(left_frame)

        bottom_frame = ctk.CTkFrame(main_frame)
        bottom_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        self.create_bottom_frame(bottom_frame)

        right_frame = ctk.CTkFrame(main_frame)
        right_frame.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')
        self.create_right_frame(right_frame)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=0)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=0)

    def create_title_frame(self, parent):
        title_frame = ctk.CTkFrame(parent)
        title_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        ctk.CTkLabel(title_frame, text='Add Product', font=('Helvetica', 20, 'bold')).pack(pady=10)

    def create_left_frame(self, parent):
        ctk.CTkLabel(parent, text='Name').pack(padx=10, pady=5)
        self.product_name_entry = ctk.CTkEntry(parent, width=230)
        self.product_name_entry.pack(padx=10, pady=5)

        ctk.CTkLabel(parent, text='Price').pack(padx=10, pady=5)
        self.product_price_entry = ctk.CTkEntry(parent, width=230)
        self.product_price_entry.pack(padx=10, pady=5)

        ctk.CTkLabel(parent, text='Items Available').pack(padx=10, pady=5)
        self.product_items_available_entry = ctk.CTkEntry(parent, width=230)
        self.product_items_available_entry.pack(padx=10, pady=5)

        ctk.CTkLabel(parent, text='Image URL').pack(padx=10, pady=5)
        self.product_image_entry = ctk.CTkEntry(parent, width=230)
        self.product_image_entry.pack(padx=10, pady=5)

    def create_bottom_frame(self, parent):
        ctk.CTkButton(parent, text='Add', command=self.add_product).pack(pady=10)
        ctk.CTkButton(parent, text='Cancel', command=self.master.create_seller_main_frame).pack(pady=10)

    def create_right_frame(self, parent):
        ctk.CTkLabel(parent, text='Description').pack(padx=10, pady=5)
        self.product_description_entry = ctk.CTkTextbox(parent, height=250, width=300)
        self.product_description_entry.pack(padx=10, pady=5)

        ctk.CTkLabel(parent, text='Tags').pack(padx=10, pady=5)
        self.product_tags_entry = ctk.CTkTextbox(parent, height=100, width=300)
        self.product_tags_entry.pack(padx=10, pady=5)

    def add_product(self):
        try:
            product_data = self.collect_product_data()
            self.send_product_data(product_data)
        except ValueError as ve:
            utils.ErrorDialog(self, message=f'Input Error: {ve}').show()
        except Exception as e:
            utils.ErrorDialog(self, message=f'An unexpected error occurred: {e}').show()

    def collect_product_data(self):
        name = self.product_name_entry.get().strip()
        price = float(self.product_price_entry.get())
        description = self.product_description_entry.get('1.0', 'end-1c').strip()
        image = self.product_image_entry.get().strip()
        tags = self.product_tags_entry.get('1.0', 'end-1c').strip()
        items_available = int(self.product_items_available_entry.get())

        if not name or not image or not description or not tags:
            raise ValueError("All fields must be filled in")

        return {
            'name': name,
            'price': price,
            'description': description,
            'image': image,
            'tags': tags,
            'items_available': items_available
        }

    def send_product_data(self, data):
        url = f'http://localhost:8080/api/seller/{self.master.user.id}/product'
        response = requests.post(url, json=data)

        if response.status_code == 200:
            # TODO add product to sellers array
            utils.InfoDialog(self, title='Success', message='Product added successfully').show()
        else:
            utils.ErrorDialog(self, message='Failed to add product!').show()
