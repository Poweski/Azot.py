import customtkinter as ctk
from shared import utils


class ReviewReadFrame(ctk.CTkFrame):
    def __init__(self, master, product, review_type):
        super().__init__(master)
        self.master = master
        self.product = product
        self.review_type = review_type

        self.setup_window()
        self.create_main_frame()
        self.create_label_frame()
        self.create_reviews_frame()
        self.create_bottom_frame()

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
        ctk.CTkLabel(label_frame, text='').pack()
        name_label = ctk.CTkLabel(label_frame, text=reviews_type, font=('Helvetica', 16, 'bold'))
        name_label.pack()
        ctk.CTkLabel(label_frame, text='').pack()

    def create_reviews_frame(self):
        reviews_frame = ctk.CTkScrollableFrame(self.main_frame)
        reviews_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        if self.review_type == 'product':
            if not self.product.reviews:
                ctk.CTkLabel(reviews_frame, text='No reviews yet', font=('Helvetica', 14)).pack(pady=10)
                return

            for review in self.product.reviews:
                self.create_review(reviews_frame, review)

        else:
            if not self.product.owner['reviews']:
                ctk.CTkLabel(reviews_frame, text='No reviews yet', font=('Helvetica', 14)).pack(pady=10)
                return

            for review in self.product.owner['reviews']:
                self.create_review(reviews_frame, review)

    def create_review(self, parent, review):
        review_frame = ctk.CTkFrame(parent)
        review_frame.pack(padx=10, pady=10, fill='x')

        ctk.CTkLabel(review_frame, text=f"Rating: {review['rating']}", font=('Helvetica', 14)).pack(pady=5)
        description_textbox = ctk.CTkTextbox(review_frame, wrap='word', font=('Helvetica', 16), width=450, height=130)
        description_textbox.insert('1.0', review['text'])
        description_textbox.configure(state='disabled')
        description_textbox.pack(padx=5, pady=10)

        author = review['client']

        if author['name'] and author['surname']:
            ctk.CTkLabel(review_frame, text=f"By: {author['name'] + ' ' + author['surname']}", font=('Helvetica', 12)).pack(pady=5)
        else:
            ctk.CTkLabel(review_frame, text='By: Anonymous', font=('Helvetica', 12)).pack(pady=5)
        return review_frame

    def create_bottom_frame(self):
        bottom_frame = ctk.CTkFrame(self.main_frame)
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        ctk.CTkLabel(bottom_frame, text='').pack()
        return_button = ctk.CTkButton(bottom_frame, text='Return to Product',
                                      command=lambda: self.master.create_product_frame(self.product.id))
        return_button.pack(pady=10)
        ctk.CTkLabel(bottom_frame, text='').pack()
