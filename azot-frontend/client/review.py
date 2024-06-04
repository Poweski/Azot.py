import requests
import customtkinter as ctk
from shared import utils, ErrorDialog, InfoDialog
from app_settings import *


class ReviewFrame(ctk.CTkFrame):
    def __init__(self, master, product_id, review_type):
        super().__init__(master)
        self.master = master
        self.product_id = product_id
        self.review_type = review_type

        self.setup_window()
        self.create_main_frame()
        self.create_label_frame()
        self.create_review_frame()

        self.rating = 0

    def setup_window(self):
        window_size = utils.adjust_window(800, 600, self.master)
        self.master.geometry(window_size)

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, fg_color='#1c1c1c')
        self.main_frame.pack(fill='both', expand=True)
        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

    def create_label_frame(self):
        if self.review_type == 'product':
            reviews_type = 'Product Reviews'
        elif self.review_type == 'seller':
            reviews_type = 'Seller Reviews'
        else:
            raise ValueError('Invalid review type')

        label_frame = ctk.CTkFrame(self.main_frame)
        label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        name_label = ctk.CTkLabel(label_frame, text=reviews_type, font=('Helvetica', 16, 'bold'))
        name_label.pack()

    def create_review_frame(self):
        review_frame = ctk.CTkFrame(self.main_frame)
        review_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        self.rating_label = ctk.CTkLabel(review_frame, text='Rating', font=('Helvetica', 14))
        self.rating_label.pack(pady=10)

        self.rating_combobox = ctk.CTkComboBox(review_frame, font=('Helvetica', 14), values=['0', '1', '2', '3', '4', '5'], command=self.combobox_callback)
        self.rating_combobox.set("0")
        self.rating_combobox.pack(pady=10)

        self.review_label = ctk.CTkLabel(review_frame, text='Review', font=('Helvetica', 14))
        self.review_label.pack(pady=10)

        self.review_textbox = ctk.CTkTextbox(review_frame, height=250, width=300)
        self.review_textbox.pack(padx=10, pady=5)

        submit_button = ctk.CTkButton(review_frame, text='Submit Review', command=self.submit_review)
        submit_button.pack(pady=10)

        return_button = ctk.CTkButton(review_frame, text='Return to Product',
                                      command=lambda: self.master.create_product_frame(self.product_id))
        return_button.pack(pady=10)

    def combobox_callback(self, choice):
        self.rating = int(choice)

    def submit_review(self):
        review = self.review_textbox.get("1.0", "end-1c")
        rating = self.rating

        if not review or not rating:
            self.show_error_dialog("Review and rating are required.")
            return

        data = {
            "rating": rating,
            "text": review
        }
        response = requests.post(
            f"http://{SERVER_HOST_NAME}:{SERVER_PORT}/api/client/{self.master.user.id}/review/{self.review_type}/{self.product_id}",
            json=data)
        print(response.json())

        if response.status_code == 200:
            self.show_success_dialog()
        elif response.status_code == 400:
            self.show_error_dialog(response.json().get('error'))
        else:
            self.show_error_dialog("Failed to submit review.")

    def show_error_dialog(self, message):
        error = ErrorDialog(self, message=message)
        error.show()

    def show_success_dialog(self):
        success = InfoDialog(self, message='Review submitted successfully.')
        success.show()
