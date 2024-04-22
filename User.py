from tkinter import *
from Admin import Admin
from Widgets import Widgets
from PIL import Image, ImageTk
from tkinter import messagebox
import customtkinter as ct
import gc


class User:
    def __init__(self, role, username, master):

        self.root = master
        children = self.root.winfo_children()
        for child in children:
            grand_children = child.winfo_children()
            if grand_children:
                for grandchild in grand_children:
                    gg_children = grandchild.winfo_children()
                    if gg_children:
                        for gg_child in gg_children:
                            gg_child.destroy()
                    grandchild.destroy()
            child.destroy()
        gc.collect()
        app_w = 1000
        app_h = 625
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.root.geometry(f'{app_w}x{app_h}+{(screen_w // 2) - (app_w // 2)}+{(screen_h // 2) - (app_h // 2)}')
        # CHECK IF THE USER IS ADMIN OR NOT, THEN CHANGES THE SIZE OF THE APP ADDING A SIDE PANEL FOR THE ADMIN---------
        if role == 'admin':
            Admin(self.root)

        for i in range(2):
            self.root.rowconfigure(i, weight=1)
            self.root.columnconfigure(i, weight=1)

        self.bg = '#404040'
        self.bg2 = '#606060'
        self.bg3 = '#40464D'
        self.fg = '#ffffff'
        # MAIN FRAME FOR THE USER WINDOW--------------------------------------------------------------------------------
        self.f_main = Frame(self.root, width=app_w, height=app_h, bg=self.bg)
        self.f_main.grid(row=0, column=1)
        self.f_main.grid_propagate(False)

        # TOP FRAME FOR NAME AND THE WALLETS AND FRAME SEPARATOR WITH THE BOT FRAMES------------------------------------
        self.f_1 = Frame(self.f_main, width=app_w, height=125, bg=self.bg)  # frame for name and wallets
        self.f_1.grid(row=0, column=0, columnspan=2)
        self.f_1.rowconfigure(index=1, weight=1)
        self.f_1.grid_propagate(False)

        self.f_1A = Frame(self.f_1, bg=self.bg)  # frame for name
        self.f_1A.grid(row=0, column=0, pady=12)
        self.f_1A.rowconfigure(index=1, weight=1)

        self.f_1B = ct.CTkScrollableFrame(self.f_1, corner_radius=12, height=80, orientation='horizontal')
        self.f_1B.grid(row=0, column=1, padx=(10, 5),  pady=9)
        self.f_1B.rowconfigure(index=1, weight=1)

        # BOT LEFT AND RIGHT FRAME THAT CONTAINS THE BALANCE AND EXCHANGE FRAMES, AND THE MOVEMENTS FRAME---------------
        self.f_2 = ct.CTkFrame(self.f_main, width=620, height=490, corner_radius=15)
        self.f_2.grid(row=1, column=0, padx=(4, 0))
        self.f_2.grid_propagate(False)

        self.f_2A = ct.CTkFrame(self.f_2, width=610, height=410, corner_radius=15)
        self.f_2A.grid(row=1, column=0, rowspan=3, columnspan=6, padx=5, pady=(3, 3), sticky='s')
        self.f_2A.grid_propagate(False)
        self.f_2A.lift()
        for i in range(10):
            self.f_2A.columnconfigure(i, weight=1)
            self.f_2A.rowconfigure(i, weight=1)

        self.f_2B = ct.CTkFrame(self.f_2, width=610, height=410, corner_radius=15)
        self.f_2B.grid(row=1, column=0, columnspan=6, rowspan=3, padx=5, pady=(3, 3), sticky='s')
        self.f_2B.grid_propagate(False)

        self.f_3 = ct.CTkFrame(self.f_main, width=350, height=490, corner_radius=15)
        self.f_3.grid(row=1, column=1, padx=(0, 4))
        self.f_3.grid_propagate(False)
        for i in range(10):
            self.f_3.columnconfigure(i, weight=1)
            self.f_3.rowconfigure(i, weight=1)

        self.f_3A = ct.CTkScrollableFrame(self.f_3,  width=310, height=410, corner_radius=15)
        self.f_3A.grid(row=2, column=0, rowspan=8, columnspan=10, pady=(0, 6))

        frames = [self.root, self.f_main, self.f_1, self.f_1A, self.f_1B, self.f_2, self.f_2A, self.f_2B, self.f_3,
                  self.f_3A]

        self.widgets = Widgets(role, username, frames)
