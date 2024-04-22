from Authenticate import *
from Signup import *
from tkinter import *
from PIL import Image, ImageTk
import customtkinter as ct


class Login:
    def __init__(self, master):
        current_appearance_mode = ct.get_appearance_mode()
        hover = {'blue': ("gray85", "gray16"), 'dark-blue': ("gray81", "gray20")}
        self.root = master
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        app_w = 600
        app_h = 400
        self.root.geometry(f'{app_w}x{app_h}+{(screen_w // 2) - (app_w // 2)}+{(screen_h // 2) - (app_h // 2)}')
        self.root.iconbitmap('icons/tools/wallet.ico')
        self.bg = '#404040'
        self.bg2 = '#606060'
        self.fg = '#ffffff'
        self.font = ('Arial', 18, 'bold')

        self.f_image = ct.CTkFrame(self.root, width=300, height=app_h)
        self.f_image.grid(row=0, column=0)
        self.f_image.grid_propagate(False)
        img = ct.CTkImage(Image.open('icons/tools/ic_login_3.png'), size=(300, app_h))
        l_img = ct.CTkLabel(self.f_image, image=img, text='')
        l_img.grid(row=0, column=0)
        l_img.image = img

        # MAIN LOGIN FRAME AND THE LOOP CONFIGURE OF THE COLUMNS AND THE ICONS------------------------------------------
        self.f_login = ct.CTkFrame(self.root, width=300, height=app_h)
        self.f_login.grid(row=0, column=1)
        self.f_login.grid_propagate(False)
        for i in range(6):
            self.f_login.rowconfigure(i, weight=1)
            self.f_login.columnconfigure(i, weight=1)

        # USERNAME LABELFRAME AND ENTRY---------------------------------------------------------------------------------
        self.e_username = ct.CTkEntry(self.f_login, font=self.font, placeholder_text='Username', width=200, height=40)
        self.e_username.grid(row=0, column=0, columnspan=6, pady=(60, 0))

        # PASSWORD LABELFRAME AND ENTRY--------------------------------------------------------------------------------
        self.e_password = ct.CTkEntry(self.f_login, font=self.font, placeholder_text='Password', width=200, height=40,
                                      show='*')
        self.e_password.grid(row=1, column=0, columnspan=6, pady=(25, 0))

        # SHOW AND HIDE PASSWORD BUTTON AND IMAGES----------------------------------------------------------------------
        self.show_pass = ct.CTkImage(Image.open('icons/tools/pass_shown.png'), size=(20, 20))
        self.hide_pass = ct.CTkImage(Image.open('icons/tools/pass_hidden.png'), size=(20, 20))
        self.show_hide = ct.CTkButton(self.f_login, text='', image=self.hide_pass, cursor='hand2', width=20, height=20,
                                      fg_color="transparent", hover_color=hover['blue'], command=self.password_view)
        self.show_hide.grid(row=1, column=5, padx=(50, 0),  pady=(25, 0))

        # LABEL FOR SHOWING ERRORS--------------------------------------------------------------------------------------
        self.l_message = ct.CTkLabel(self.f_login, text='', text_color='red', font=('Arial', 15))
        self.l_message.grid(row=2, column=0, columnspan=6, sticky='ew')

        # LOGIN AND SIGNUP BUTTONS WITH ICONS---------------------------------------------------------------------------
        self.bt_login = ct.CTkButton(self.f_login, text='Login', cursor="hand2", font=self.font, width=100,
                                     corner_radius=30, command=self.on_login_clicked)
        self.bt_login.grid(row=3, column=0, columnspan=3, padx=(20, 0))

        self.bt_sign = ct.CTkButton(self.f_login, text='Signup', cursor="hand2", font=self.font, width=100,
                                    corner_radius=30, command=self.on_signup_clicked)
        self.bt_sign.grid(row=3, column=3, columnspan=3, padx=(0, 20))

        self.r_var = IntVar()
        self.remember = ct.CTkCheckBox(self.f_login, text='Remember', variable=self.r_var, cursor='hand2',
                                       border_width=1, corner_radius=20, checkbox_width=12, checkbox_height=12)
        self.remember.grid(row=4, column=1, columnspan=2, padx=(15, 0), pady=14)
        self.root.mainloop()

    def password_view(self):
        if self.e_password.cget('show') == '':
            self.e_password.configure(show='*')
            self.show_hide.configure(image=self.hide_pass)
        else:
            self.e_password.configure(show='')
            self.show_hide.configure(image=self.show_pass)

    # FUNCTION THAT AUTHENTICATES THE USERNAME AND PASSWORD-------------------------------------------------------------
    def on_login_clicked(self):
        username = self.e_username.get()
        password = self.e_password.get()
        login_result = validate_login(username, password)

        if login_result == 'user not found':
            self.l_message.configure(text=login_result)
        elif login_result == 'invalid password':
            self.l_message.configure(text=login_result)
        else:
            from User import User
            from Static import Static
            from Functions import Functions
            Static.garbage_collect(self.f_login)
            Static.garbage_collect(self.f_image)
            self.f_login.grid_remove()
            self.f_image.grid_remove()
            if self.r_var.get() == 1:
                Functions.remember(username, value=1)
            User(role=login_result, username=username, master=self.root)

    # HIDE THE LOGIN WINDOW AND CALL THE SIGNUP WINDOW------------------------------------------------------------------
    def on_signup_clicked(self):
        # Static.garbage_collect(self.f_login)
        self.f_login.grid_remove()
        Signup(self.root, self.f_image, self.f_login, 'user')
