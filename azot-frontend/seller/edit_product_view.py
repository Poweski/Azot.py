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

        self.main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        self.main_frame.pack(fill='both', expand=True)

        self.create_top_frame()
        self.create_left_frame()
        self.create_right_frame()

        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

        self.load_product()
        self.edit_mode = False
        self.enable_buttons(False)

    def create_top_frame(self):
        label_frame = ctk.CTkFrame(self.main_frame)
        label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        name_label = ctk.CTkLabel(label_frame, text=f'Product Name:', font=('Helvetica', 16, 'bold'))
        name_label.pack()
        self.name_entry = ctk.CTkEntry(label_frame, font=('Helvetica', 16, 'bold'))
        self.name_entry.pack(padx=5, pady=10)

    def create_left_frame(self):
        left_frame = ctk.CTkFrame(self.main_frame)
        left_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkLabel(left_frame, text='').pack()
        price_label = ctk.CTkLabel(left_frame, text=f'Price', font=('Helvetica', 14))
        price_label.pack(padx=5)
        self.price_entry = ctk.CTkEntry(left_frame, font=('Helvetica', 14))
        self.price_entry.pack(padx=5)

        ctk.CTkLabel(left_frame, text='').pack()
        items_available_label = ctk.CTkLabel(left_frame, text=f'Items Available', font=('Helvetica', 14))
        items_available_label.pack(padx=5)
        self.items_available_entry = ctk.CTkEntry(left_frame, font=('Helvetica', 14))
        self.items_available_entry.pack(padx=5)

        ctk.CTkLabel(left_frame, text='').pack()
        items_available_label = ctk.CTkLabel(left_frame, text=f'Tags', font=('Helvetica', 14))
        items_available_label.pack(padx=5)
        self.tags_textbox = ctk.CTkTextbox(left_frame, wrap='word', font=('Helvetica', 14), width=150, height=100)
        self.tags_textbox.pack(padx=5)

        ctk.CTkLabel(left_frame, text='').pack()
        self.edit_button = ctk.CTkButton(left_frame, text='Edit', command=self.toggle_edit_mode)
        self.edit_button.pack(pady=5)
        self.delete_button = ctk.CTkButton(left_frame, text='Delete', command=self.delete_product)
        self.delete_button.pack(pady=5)
        self.back_button = ctk.CTkButton(left_frame, text='Back', command=self.master.create_seller_main_frame)
        self.back_button.pack(pady=5)

    def create_right_frame(self):
        right_frame = ctk.CTkFrame(self.main_frame)
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

    def delete_product(self):
        dialog = utils.ConfirmDialog(self, title='Delete', message='Are you sure you want to delete this product?')
        if dialog.show():
            url = f'http://localhost:8080/api/seller/{self.master.user.id}/product/{self.product.id}'
            response = requests.delete(url)

            if response.status_code == 200:
                self.master.user.products = [product for product in self.master.user.products if product.id != self.product.id]
                utils.InfoDialog(self, title='Success', message='Product deleted successfully').show()
                self.master.create_seller_main_frame()
            else:
                utils.ErrorDialog(self, message='Failed to delete product!').show()

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.enable_buttons(self.edit_mode)
        if self.edit_mode:
            self.edit_button.configure(text='Submit', fg_color='red', hover_color='#8B0000')
            self.back_button.configure(state='disabled')
            self.delete_button.configure(state='disabled')

            self.image_label.pack_forget()
            self.description_textbox.pack_forget()
            self.image_url_label.pack(pady=10)
            self.image_url_entry.pack(padx=5, pady=10)
            self.description_textbox.pack(padx=5, pady=10)
        else:
            self.save_product()
            self.edit_button.configure(text='Edit', fg_color='#1f538d', hover_color='#14375e')
            self.back_button.configure(state='normal')
            self.delete_button.configure(state='normal')

            self.description_textbox.pack_forget()
            self.image_url_label.pack_forget()
            self.image_url_entry.pack_forget()
            self.image_label.pack(pady=10)
            self.description_textbox.pack(padx=5, pady=10)

    def enable_buttons(self, state):
        state = 'normal' if state else 'disabled'
        self.name_entry.configure(state=state)
        self.price_entry.configure(state=state)
        self.items_available_entry.configure(state=state)
        self.tags_textbox.configure(state=state)
        self.description_textbox.configure(state=state)
        self.image_url_entry.configure(state=state)

    def load_product(self):
        self.enable_buttons(True)
        self.name_entry.delete(0, ctk.END)
        self.name_entry.insert(0, f'{self.product.name}')
        self.price_entry.delete(0, ctk.END)
        self.price_entry.insert(0, f'{self.product.price}')
        self.items_available_entry.delete(0, ctk.END)
        self.items_available_entry.insert(0, f'{self.product.items_available}')
        self.tags_textbox.delete('1.0', 'end')
        self.tags_textbox.insert('1.0', self.product.tags)
        self.description_textbox.delete('1.0', 'end')
        self.description_textbox.insert('1.0', self.product.description)
        self.image_url_entry.delete(0, ctk.END)
        self.image_url_entry.insert(0, f'{self.image_url}')
        self.enable_buttons(False)

    def save_product(self):
        product_id = self.product.id
        name = self.name_entry.get()
        price = float(self.price_entry.get())
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
            for product in self.master.user.products:
                if product.id == self.product.id:
                    product.name = name
                    product.price = price
                    product.description = description
                    product.image = image_url
                    product.items_available = items_available
                    product.tags = tags

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

