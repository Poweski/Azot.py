import requests
import customtkinter as ctk
from shared import utils
from urllib.request import urlopen
from PIL import Image
import io
from app_settings import *

# TODO in production


class CartView(ctk.CTkFrame):
    def __init__(self, master, orders):
        super().__init__(master)
        self.master = master
        self.orders = orders

        window_size = utils.adjust_window(800, 600, master)
        master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        main_frame.pack(fill='both', expand=True)

        label_frame = ctk.CTkFrame(main_frame)
        label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        name_label = ctk.CTkLabel(label_frame, text='Cart', font=('Helvetica', 16, 'bold'))
        name_label.pack(padx=5, pady=10)

        left_frame = ctk.CTkFrame(main_frame)
        left_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkLabel(left_frame, text='').pack()
        price_label = ctk.CTkLabel(left_frame, text=f'Price:\n${self.product.price:.2f}', font=('Helvetica', 16))
        price_label.pack(padx=5, pady=10)

        seller_label = ctk.CTkLabel(left_frame, text=f'Seller:\n{self.product.owner['seller_info']['organization']}', font=('Helvetica', 16))
        seller_label.pack(padx=5, pady=10)

        print(self.product.owner)

        owner_avg_rating = self.product.owner['average_rating']
        if owner_avg_rating:
            rating = f'Seller rating: {owner_avg_rating:.1f}'
        else:
            rating = 'No Ratings'
        owner_avg_rating_label = ctk.CTkLabel(left_frame, text=f'Seller Rating:\n{rating}', font=('Helvetica', 16))
        owner_avg_rating_label.pack(padx=5, pady=10)

        items_available_label = ctk.CTkLabel(left_frame, text=f'Items Available:\n{self.product.items_available}', font=('Helvetica', 16))
        items_available_label.pack(padx=5, pady=10)

        right_frame = ctk.CTkFrame(main_frame)
        right_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        image_url = self.product.image
        image_data = urlopen(image_url).read()
        image_pil = Image.open(io.BytesIO(image_data))
        new_size = (450, 230)
        image_pil_resized = image_pil.resize(new_size, Image.LANCZOS)
        image_ctk = ctk.CTkImage(light_image=image_pil_resized, size=new_size)
        image_label = ctk.CTkLabel(right_frame, image=image_ctk, text='')
        image_label.pack(pady=10)

        description_textbox = ctk.CTkTextbox(right_frame, wrap='word', font=('Helvetica', 16), width=450, height=230)
        description_textbox.insert('1.0', self.product.description)
        description_textbox.configure(state='disabled')
        description_textbox.pack(padx=5, pady=10)

        ctk.CTkLabel(left_frame, text='').pack()
        ctk.CTkButton(left_frame, text='Add to cart', command=self.add_to_cart).pack(pady=10)
        ctk.CTkButton(left_frame, text='Back', command=master.create_client_main_frame).pack(pady=10)

        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=0)
        main_frame.rowconfigure(1, weight=1)

    def add_to_cart(self):
        try:
            quantity = utils.InputDialog(self, title='Add to cart', message='Enter the amount:').show()
            url = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/client/{self.master.user.id}/cart'
            data = {
                "orders": [
                    {
                        "product": self.product.id,
                        "quantity": quantity
                    }]
            }
            response = requests.post(url, json=data)

            if response.status_code == 200:
                utils.InfoDialog(self, title='Success', message='Product added to cart').show()
            elif response.status_code == 400:
                utils.ErrorDialog(self, message=response.json().get('error')).show()
            else:
                utils.ErrorDialog(self, message='Failed to add product to cart!').show()

        except Exception as err:
            utils.ErrorDialog(self, message=f'Error occurred: {err}').show()
