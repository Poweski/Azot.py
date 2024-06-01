import requests
import customtkinter as ctk
from shared import utils
from urllib.request import urlopen
from PIL import Image
import io


class EditProductView(ctk.CTkFrame):
    def __init__(self, master, product):
        super().__init__(master)
        self.master = master
        self.product = product

        window_size = utils.adjust_window(800, 600, master)
        master.geometry(window_size)

        main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        main_frame.pack(fill='both', expand=True)

        label_frame = ctk.CTkFrame(main_frame)
        label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        name_label = ctk.CTkLabel(label_frame, text=f'Product Name:', font=('Helvetica', 16, 'bold'))
        name_label.pack()
        self.name_entry = ctk.CTkEntry(label_frame, font=('Helvetica', 16, 'bold'))
        self.name_entry.pack(padx=5, pady=10)

        left_frame = ctk.CTkFrame(main_frame)
        left_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkLabel(left_frame, text='').pack()
        price_label = ctk.CTkLabel(left_frame, text=f'Price:', font=('Helvetica', 16))
        price_label.pack(padx=5, pady=10)
        self.price_entry = ctk.CTkEntry(left_frame, font=('Helvetica', 16))
        self.price_entry.pack(padx=5, pady=10)

        items_available_label = ctk.CTkLabel(left_frame, text=f'Items Available:', font=('Helvetica', 16))
        items_available_label.pack(padx=5, pady=10)
        self.items_available_entry = ctk.CTkEntry(left_frame, font=('Helvetica', 16))
        self.items_available_entry.pack(padx=5, pady=10)

        self.tags_textbox = ctk.CTkTextbox(left_frame, wrap='word', font=('Helvetica', 16), width=100, height=100)
        self.tags_textbox.pack(padx=5, pady=10)

        right_frame = ctk.CTkFrame(main_frame)
        right_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        self.image_url = self.product.image
        image_data = urlopen(self.image_url).read()
        image_pil = Image.open(io.BytesIO(image_data))
        new_size = (450, 230)
        image_pil_resized = image_pil.resize(new_size, Image.LANCZOS)
        self.image_ctk = ctk.CTkImage(light_image=image_pil_resized, size=new_size)
        self.image_label = ctk.CTkLabel(right_frame, image=self.image_ctk, text='')
        self.image_label.pack(pady=10)

        self.image_url_label = ctk.CTkLabel(right_frame, text='Image URL:', font=('Helvetica', 16))
        self.image_url_entry = ctk.CTkEntry(right_frame, font=('Helvetica', 16), width=450)

        self.description_textbox = ctk.CTkTextbox(right_frame, wrap='word', font=('Helvetica', 16), width=450, height=230)
        self.description_textbox.pack(padx=5, pady=10)

        ctk.CTkLabel(left_frame, text='').pack()
        self.edit_button = ctk.CTkButton(left_frame, text='Edit', command=self.toggle_edit_mode, fg_color='red', hover_color='#8B0000')
        self.edit_button.pack(pady=10)
        self.back_button = ctk.CTkButton(left_frame, text='Back', command=master.create_seller_main_frame)
        self.back_button.pack(pady=10)

        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=0)
        main_frame.rowconfigure(1, weight=1)

        self.load_product()
        self.edit_mode = False
        self.enable_buttons(False)

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.enable_buttons(self.edit_mode)
        if self.edit_mode:
            self.edit_button.configure(text='Submit')
            self.back_button.configure(state='disabled')

            self.image_label.pack_forget()
            self.image_url_label.pack(pady=10)
            self.image_url_entry.pack(padx=5, pady=10)
            self.image_url_entry.insert(0, self.image_url)
        else:
            self.save_profile()
            self.edit_button.configure(text='Edit')
            self.back_button.configure(state='normal')

            self.image_url_label.pack_forget()
            self.image_url_entry.pack_forget()
            self.image_label.pack(pady=10)

    def enable_buttons(self, state):
        state = 'normal' if state else 'disabled'
        self.name_entry.configure(state=state)
        self.price_entry.configure(state=state)
        self.items_available_entry.configure(state=state)
        self.tags_textbox.configure(state=state)
        self.description_textbox.configure(state=state)
        if not state:
            self.image_url_entry.configure(state=state)

    def load_product(self):
        self.name_entry.insert(0, f'{self.product.name}')
        self.price_entry.insert(0, f'{self.product.price}')
        self.items_available_entry.insert(0, f'{self.product.items_available}')
        self.tags_textbox.insert('1.0', self.product.tags)
        self.description_textbox.insert('1.0', self.product.description)

        self.name_entry.configure(state='disabled')
        self.price_entry.configure(state='disabled')
        self.items_available_entry.configure(state='disabled')
        self.tags_textbox.configure(state='disabled')
        self.description_textbox.configure(state='disabled')

    def save_profile(self):
        product_id = self.product.id
        name = self.name_entry.get()
        price = self.price_entry.get()
        items_available = int(self.items_available_entry.get())
        tags = self.tags_textbox.get('1.0', ctk.END).strip()
        description = self.description_textbox.get('1.0', ctk.END).strip()
        image_url = self.image_url_entry.get().strip()

        data = {
            "name": name,
            "price": price,
            "description": description,
            "image": image_url,
            "tags": tags,
            "items_available": items_available
        }

        url = f'http://localhost:8080/api/seller/{self.master.user.id}/product/{product_id}'
        response = requests.put(url, json=data)

        if response.status_code == 200:
            self.image_url = image_url
            image_data = urlopen(self.image_url).read()
            image_pil = Image.open(io.BytesIO(image_data))
            new_size = (450, 230)
            image_pil_resized = image_pil.resize(new_size, Image.LANCZOS)
            self.image_ctk = ctk.CTkImage(light_image=image_pil_resized, size=new_size)
            self.image_label.configure(image=self.image_ctk)
            utils.InfoDialog(self, title='Success', message='Product data updated successfully').show()
        else:
            utils.ErrorDialog(self, message='Failed to update product data!').show()

        self.load_product()

