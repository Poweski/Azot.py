import requests
from utils import *


class AddProductFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        window_size = adjust_window(800, 600, master)
        master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        main_frame.pack(fill='both', expand=True)

        title_frame = ctk.CTkFrame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        ctk.CTkLabel(title_frame, text='Add Product', font=('Helvetica', 20)).pack(pady=10)

        left_frame = ctk.CTkFrame(main_frame)
        left_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        ctk.CTkLabel(left_frame, text='Name').pack( padx=10, pady=5)
        self.product_name_entry = ctk.CTkEntry(left_frame, width=230)
        self.product_name_entry.pack( padx=10, pady=5)

        ctk.CTkLabel(left_frame, text='Price').pack( padx=10, pady=5)
        self.product_price_entry = ctk.CTkEntry(left_frame, width=230)
        self.product_price_entry.pack( padx=10, pady=5)

        ctk.CTkLabel(left_frame, text='Items Available').pack( padx=10, pady=5)
        self.product_items_available_entry = ctk.CTkEntry(left_frame, width=230)
        self.product_items_available_entry.pack( padx=10, pady=5)

        ctk.CTkLabel(left_frame, text='Image URL').pack( padx=10, pady=5)
        self.product_image_entry = ctk.CTkEntry(left_frame, width=230)
        self.product_image_entry.pack( padx=10, pady=5)

        bottom_frame = ctk.CTkFrame(main_frame)
        bottom_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        ctk.CTkButton(bottom_frame, text='Add', command=self.add_product).pack(pady=10)
        ctk.CTkButton(bottom_frame, text='Cancel', command=master.create_seller_main_frame).pack(pady=10)

        right_frame = ctk.CTkFrame(main_frame)
        right_frame.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')

        ctk.CTkLabel(right_frame, text='Description').pack(padx=10, pady=5)
        self.product_description_entry = ctk.CTkTextbox(right_frame, height=250, width=300)
        self.product_description_entry.pack(padx=10, pady=5)

        ctk.CTkLabel(right_frame, text='Tags').pack(padx=10, pady=5)
        self.product_tags_entry = ctk.CTkTextbox(right_frame, height=100, width=300)
        self.product_tags_entry.pack(padx=10, pady=5)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=0)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=0)

    def add_product(self):
        try:
            name = self.product_name_entry.get()
            price = float(self.product_price_entry.get())
            description = self.product_description_entry.get('1.0', 'end-1c')
            image = self.product_image_entry.get()
            tags = self.product_tags_entry.get('1.0', 'end-1c')
            items_available = int(self.product_items_available_entry.get())

            url = f'http://localhost:8080/api/seller/{self.master.user.id}/product'
            data = {
                'name': name,
                'price': price,
                'description': description,
                'image': image,
                'tags': tags,
                'items_available': items_available
            }

            response = requests.post(url, json=data)
            if response.status_code == 200:
                InfoDialog(self, title='Success', message='Product added successfully').show()
            else:
                ErrorDialog(self, message='Failed to add product!').show()
        except Exception as err:
            ErrorDialog(self, message=f'Error occurred: {err}').show()
