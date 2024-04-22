import gc
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import date, datetime
from Functions import Functions
from Static import Static
from Charts import Charts
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import customtkinter as ct
import os
import time
import numpy as np
import uuid

coins = ["ALL", "EUR", "USD", "GBP", "CHF", "AUD", "BRL", "CAD", "CNY", "INR", "JPY", "KRW", "MXN", "NOK", "NZD",
         "RUB", "SEK", "SGD", "ZAR"]

month_map = {
        '01': 'JAN', '02': 'FEB', '03': 'MAR', '04': 'APR',
        '05': 'MAY', '06': 'JUN', '07': 'JUL', '08': 'AUG',
        '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DEC'
    }
'''
ALL: Albanian Lek
EUR: Euro
USD: United States Dollar
GBP: British Pound Sterling
CHF: Swiss Franc
AUD: Australian Dollar
BRL: Brazilian Real
CAD: Canadian Dollar
CNY: Chinese Yuan
INR: Indian Rupee
JPY: Japanese Yen
KRW: South Korean Won
MXN: Mexican Peso
NOK: Norwegian Krone
NZD: New Zealand Dollar
RUB: Russian Ruble
SEK: Swedish Krona
SGD: Singapore Dollar
ZAR: South African Rand
'''

fonts = [
    "Arial", "Arial Black", "Arial Narrow", "Arial Rounded MT Bold", "Avant Garde", "Calibri",
    "Calisto MT", "Cambria", "Candara", "Century Gothic", "Century Schoolbook", "Comic Sans MS",
    "Consolas", "Courier", "Courier New", "DejaVu Sans", "DejaVu Sans Mono", "DejaVu Serif",
    "Dingbats", "Dotum", "FangSong", "Franklin Gothic Medium", "Gabriola", "Gadugi", "Geneva",
    "Georgia", "Gill Sans", "Gill Sans MT", "Goudy Old Style", "Gulim", "Gungsuh", "Helvetica",
    "Helvetica Neue", "Impact", "Javanese Text", "KaiTi", "Kalinga", "Lao UI", "Lucida Bright",
    "Lucida Calligraphy", "Lucida Console", "Lucida Grande", "Lucida Handwriting", "Lucida Sans",
    "Lucida Sans Typewriter", "Lucida Sans Unicode", "Malgun Gothic", "Meiryo", "Meiryo UI",
    "Microsoft Himalaya", "Microsoft JhengHei", "Microsoft New Tai Lue", "Microsoft PhagsPa",
    "Microsoft Sans Serif", "Microsoft Tai Le", "Microsoft YaHei", "Microsoft Yi Baiti",
    "MingLiU", "MingLiU-ExtB", "Minion", "Monaco", "Mongolian Baiti", "MS Gothic", "MS Outlook",
    "MS PGothic", "MS Sans Serif", "MS Serif", "MS UI Gothic", "Myanmar Text", "Narkisim",
    "New York", "Nirmala UI", "Palatino", "Palatino Linotype", "Papyrus", "Perpetua",
    "Playbill", "PMingLiU", "PMingLiU-ExtB", "Segoe MDL2 Assets", "Segoe Print", "Segoe Script",
    "Segoe UI", "Segoe UI Emoji", "Segoe UI Historic", "Segoe UI Symbol", "SimSun", "SimSun-ExtB",
    "Sitka", "Small Fonts", "Sylfaen", "Symbol", "Tahoma", "Times", "Times New Roman",
    "Trebuchet MS", "Verdana", "Webdings", "Wingdings", "Yu Gothic", "Yu Mincho"
]


class Widgets:
    def __init__(self, role, username, frames):

        self.theme = ct.get_appearance_mode()
        self.c1 = {"Light": "#dbdbdb", "Dark": "#2b2b2b"}
        self.c2 = {"Light": '#cfcfcf', "Dark": '#333333'}
        self.c3 = {"Light": '#4d4d4d', "Dark": '#a0a0a0'}
        self.h1 = ("#dbdbdb", "#2b2b2b")
        self.h2 = ('#cfcfcf', '#333333')
        self.bg = {"Light": '#ffffff', "Dark": '#404040'}
        self.fg = {"Light": '#000000', "Dark": '#ffffff'}

        self.status = {'admin': 'disabled', 'user': 'active'}  # disables buttons if the user is admin
        self.exp_type = {'income': '+', 'expense': '-'}
        self.exp_type2 = {'+': 'income', '-': 'expense'}

        self.root = frames[0]
        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.f_main = frames[1]
        self.f_1 = frames[2]
        self.f_1A = frames[3]
        self.f_1B = frames[4]
        self.f_2 = frames[5]
        self.f_2A = frames[6]
        self.f_2B = frames[7]
        self.f_3 = frames[8]
        self.f_3A = frames[9]
        self.f_1.configure(bg=self.bg[self.theme])
        self.f_1A.configure(bg=self.bg[self.theme])
        self.f_main.configure(bg=self.bg[self.theme])
        self.username = username
        self.role = role

        self.settings_toggle = True  # toggle for the settings in the balance frame
        self.c_toggle = True  # toggle to switch between the category and date treeview
        self.pie_toggle = False  # toggle to switch between the wallet charts
        self.calendar_toggle = True

        self.wallet = ''  # current wallet name
        self.walled_oid = None  # current wallet oid
        self.days = 0

        self.wallet_list = []
        self.menu_list = []
        self.donut_list = []
        self.bar_list = []
        self.exchange_list = []
        self.settings_list = []
        self.calendar_list = []

        self.style_c = ttk.Style()
        self.style_c.theme_use('default')
        self.style_c.configure('Treeview', rowheight=40, font=('Arial', 13), relief='flat', borderwidth=0,
                               fieldbackground=self.c2[self.theme], background=self.c2[self.theme],
                               foreground=self.fg[self.theme])
        self.style_c.map("Treeview", background=[("selected", self.c3[self.theme])])

        self.style_c.configure('CustomTreeview.Treeview', background=self.c2[self.theme], rowheight=60,
                               fieldbackground=self.c2[self.theme], foreground=self.fg[self.theme],
                               font=('Arial', 14, 'bold'))
        self.style_c.map('CustomTreeview.Treeview', background=[("selected", self.c2[self.theme])])

        # ADD NEW WALLET BUTTON, IS DISABLED IF THE WALLET NUMBER IS 10 OR THE USER IS ADMIN----------------------------
        self.l_add_wallet = ct.CTkLabel(self.f_1, text='+', cursor='hand2', font=('Times New Roman', 70))
        self.l_add_wallet.bind("<Button-1>", lambda event: self.add_edit_wallet('INSERT'))
        self.l_add_wallet.configure(cursor='hand2')

        light_range = 'icons/tools/sort_by_range_light.png'
        dark_range = 'icons/tools/sort_by_range_dark.png'
        img_range = ct.CTkImage(light_image=Image.open(light_range), dark_image=Image.open(dark_range), size=(40, 40))
        self.l_range = ct.CTkLabel(self.f_3, text='Day', image=img_range, cursor='hand2', font=('Arial', 15, 'bold'))
        self.l_range.bind('<Button-1>', lambda e: self.calendar_range())
        self.l_range.grid(row=0, column=8, rowspan=2, columnspan=2, pady=15)

        self.functions = Functions(self.username)  # call the functions that handle the SQL queries
        self.static = Static()  # static functions

        self.wallets = self.functions.retrieve_wallets()  # list of wallets
        self.menu_frame()
        self.tree_menu_frame()
        self.name_surname_frame()
        self.wallets_frame()

    # FUNCTION THAT CREATES THE NAME AND SURNAME LABEL OF THE USER self.f_1A--------------------------------------------
    def name_surname_frame(self):
        self.static.garbage_collect(self.f_1A)
        user = self.functions.name_surname()
        font = self.static.calculate_font_size(f'{user[2]} {user[3]}', base_size=30, min_size=12, decrease_rate=1)
        l_name = ct.CTkLabel(self.f_1A, text=f'{user[2]} {user[3]}', font=('Arial', font))
        l_name.grid(row=0, column=0, rowspan=1, padx=10, columnspan=3)
        img_logout = ct.CTkImage(Image.open('icons/tools/logout.png'), size=(20, 20))
        btn_logout = ct.CTkButton(self.f_1A, image=img_logout, command=self.logout, cursor='hand2', text='',
                                  hover_color=('#ffffff', '#404040'), fg_color='transparent', width=1)
        btn_logout.grid(row=1, column=0, padx=10, pady=10)

        light_theme = 'icons/tools/theme_light.png'
        dark_theme = 'icons/tools/theme_dark.png'
        theme = ct.CTkImage(light_image=Image.open(light_theme), dark_image=Image.open(dark_theme), size=(40, 20))
        bt_theme = ct.CTkButton(self.f_1A, text='', image=theme, cursor='hand2', width=1, height=1,
                                fg_color="transparent", hover_color=('white', self.bg[self.theme]),
                                command=lambda: self.switch_theme(bt_theme))
        bt_theme.grid(row=1, column=1)
        from Signup import EditUser
        img_settings = ct.CTkImage(Image.open('icons/tools/settings.png'), size=(20, 20))
        bt_settings = ct.CTkButton(self.f_1A, text='', image=img_settings, cursor='hand2',
                                   hover_color=('#ffffff', '#404040'), fg_color='transparent', width=1)
        bt_settings.configure(command=lambda: EditUser(self.f_2A, user, lambda: self.selected_menu(0),
                                                       self.name_surname_frame))

        bt_settings.grid(row=1, column=2)

    # FUNCTION THAT CREATES THE WALLETS BUTTONS WITH THE COMMANDS TO SWITCH BETWEEN self.f_1B---------------------------
    def wallets_frame(self):
        self.static.garbage_collect(self.f_1B)
        self.f_2A.lift()
        column = 0
        self.root.update_idletasks()
        max_w = (900 - self.f_1A.winfo_width())
        width = len(self.wallets) * 90
        self.f_1B.configure(width=min(max_w, width))
        if self.wallets:
            self.wallet_list.clear()
            for w in self.wallets:
                font = self.static.calculate_font_size(w[1], base_size=14, min_size=8)
                photo = ct.CTkImage(Image.open(w[6]), size=(40, 40))
                btn = ct.CTkButton(self.f_1B, image=photo, cursor='hand2', text='', width=40, height=40,
                                   fg_color="transparent", hover_color=self.h2)
                btn.grid(row=0, column=column, padx=10, pady=(5, 0))
                btn.configure(command=lambda n=w[1], p=w[7], o=w[6], u=column: self.call_wallet(n, p, o, u))
                lbl = ct.CTkLabel(self.f_1B, text=w[1], height=10, font=('Arial', font, 'bold'))
                lbl.grid(row=1, column=column, padx=7, pady=(0, 6))
                self.wallet_list.append(btn)
                column += 1
            self.call_wallet(self.wallets[0][1], self.wallets[0][7], self.wallets[0][6], 0)
        else:
            self.call_wallet()
        if len(self.functions.retrieve_wallets()) >= 15:
            self.l_add_wallet.grid_remove()
        else:
            self.l_add_wallet.grid(row=0, column=2, rowspan=2, padx=10)

    # FUNCTION TO SWITCH TO THE SELECTED WALLET-------------------------------------------------------------------------
    def call_wallet(self, w_name=None, w_oid=None, w_img=None, w_btn=None):
        if self.wallets:
            self.wallet = w_name
            self.walled_oid = w_oid
            self.tree_toggle()
            self.selected_menu(0)
            self.settings_toggle = True
            new_img = ct.CTkImage(Image.open(w_img), size=(60, 60))
            self.menu_list[0].configure(image=new_img)
            for index, item in enumerate(self.wallet_list):
                if index != w_btn:
                    item.configure(fg_color='transparent', hover_color=self.h2, corner_radius=7)
            self.wallet_list[w_btn].configure(fg_color='gray', hover_color='gray', corner_radius=7)
        else:
            default_img = ct.CTkImage(Image.open('icons/tools/choose_category.png'), size=(60, 60))
            self.menu_list[0].configure(image=default_img)
        self.balance_frame()

    # FUNCTION TO CREATE AND EDIT WALLETS FOR THE USER self.f_2A7-------------------------------------------------------
    def add_edit_wallet(self, action, edit=None):

        def collect_data():
            name = e_name.get().capitalize()
            start_sum = e_start_sum.get().replace(',', '.').strip()
            if not start_sum:  # Check if start_sum is empty
                start_sum = '0'
            coin = om_coin.get()
            date_str = bt_calendar.cget('text')
            date_ob = datetime.strptime(date_str, "%d-%m-%Y")
            f_date = date_ob.strftime("%Y-%m-%d")
            icon = btn.cget('text')
            if name == '':
                messagebox.showerror("Error", "Please enter a name", parent=self.f_2A)
                return

            elif len(name) < 3 or len(name) > 12:
                messagebox.showerror("Error", "Name must be between 3 and 12 characters", parent=self.f_2A)
                return

            elif self.functions.wallet_exist(name) and (edit is None or edit[1].lower() != name.lower()):
                messagebox.showerror('Error', 'Name already exists', parent=self.f_2A)
                return

            if ' ' in start_sum:
                messagebox.showerror("Error", "Input should not contain spaces.", parent=self.f_2A)
                return
            try:
                start_sum = float(start_sum)
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a number.", parent=self.f_2A)
                return

            if icon == 'Select':
                messagebox.showerror("Error", "Select a category", parent=self.f_2A)
                return

            p = f'icons/wallet/{icon}'
            if action == 'INSERT':
                self.functions.create_update_wallet(action, name, start_sum, coin, f_date, p)
            else:
                self.functions.create_update_wallet(action, name, start_sum, coin, f_date, p, edit[7], self.wallet)

            self.wallets = self.functions.retrieve_wallets()
            self.wallets_frame()
            self.settings_toggle = True

        self.static.garbage_collect(self.f_2A)
        args = {'text': '', 'cursor': 'hand2', 'fg_color': "transparent", 'hover_color': self.h2, 'width': 1,
                'height': 1}
        size = (60, 60)

        current_date = date.today().strftime("%d-%m-%Y")
        img_calendar = ct.CTkImage(Image.open('icons/tools/calendar.png'), size=size)
        bt_calendar = ct.CTkLabel(self.f_2A, text=current_date, image=img_calendar, cursor='hand2', font=('Arial', 25),
                                  compound='left')
        bt_calendar.bind('<Button-1>', lambda event: self.static.grab_date(self.f_2A, bt_calendar))
        e_name = ct.CTkEntry(self.f_2A, font=('Arial', 25), width=200, height=50, placeholder_text='Wallet name')
        e_start_sum = ct.CTkEntry(self.f_2A, font=('Arial', 25), width=200, height=50,
                                  placeholder_text='Starting balance')
        om_coin = ct.CTkOptionMenu(self.f_2A, values=coins, width=70, font=('Arial', 25), fg_color=self.h2,
                                   text_color=('black', 'white'), button_color=self.h2, button_hover_color=self.h2)
        xy = 200
        img = ct.CTkImage(Image.open('icons/tools/choose_category.png'), size=(xy, xy))
        btn = ct.CTkButton(self.f_2A, image=img, text='Select', fg_color="transparent", cursor='hand2', compound='top',
                           hover_color=self.h2, width=1, height=1, text_color=('black', 'white'))
        btn.configure(command=lambda: self.category_icon('wallet', btn, xy, xy))

        img_confirm = ct.CTkImage(Image.open('icons/tools/action_confirm.png'), size=size)
        bt_confirm = ct.CTkButton(self.f_2A, image=img_confirm, **args)
        bt_confirm.configure(command=collect_data, state=self.status[self.role])

        img_cancel = ct.CTkImage(Image.open('icons/tools/action_cancel.png'), size=size)
        bt_cancel = ct.CTkButton(self.f_2A, image=img_cancel, **args)
        bt_cancel.configure(command=lambda: (self.selected_menu(0), setattr(self, 'settings_toggle', True)))

        bt_calendar.grid(row=0, column=0, rowspan=3, columnspan=3, padx=(10, 0), sticky='w')
        e_name.grid(row=3, column=0, rowspan=3, columnspan=3, padx=(15, 0), sticky='w')
        e_start_sum.grid(row=6, column=0, rowspan=4, columnspan=3, padx=(15, 0), sticky='w')
        om_coin.grid(row=6, column=2, rowspan=4, columnspan=3)
        btn.grid(row=0, column=3, rowspan=6, columnspan=7)
        bt_confirm.grid(row=6, column=4, rowspan=4, columnspan=3)
        bt_cancel.grid(row=6, column=7, rowspan=4, columnspan=3)

        if edit is not None:
            edit = self.functions.edit_wallet(self.wallet)

            path = os.path.basename(edit[6])
            e_name.insert(0, edit[1])
            e_start_sum.insert(0, edit[4])
            om_coin.set(edit[3])
            date_obj = datetime.strptime(edit[5], '%Y-%m-%d')
            new_date = date_obj.strftime('%d-%m-%Y')
            bt_calendar.configure(text=new_date)
            img = ct.CTkImage(Image.open(edit[6]), size=(xy, xy))
            btn.configure(text=path, image=img)
        self.f_2A.lift()

    def menu_frame(self):

        args = {'text': '', 'cursor': 'hand2', 'width': 40, 'height': 40, 'hover_color': self.h2,
                'fg_color': 'transparent', 'corner_radius': 10}
        size = (60, 60)

        img_wallet = ct.CTkImage(Image.open('icons/tools/choose_category.png'), size=size)
        bt_wallet = ct.CTkButton(self.f_2, image=img_wallet, **args, command=lambda: self.selected_menu(0))

        img_cat = ct.CTkImage(Image.open('icons/tools/categories_list.png'), size=size)
        bt_cat = ct.CTkButton(self.f_2, image=img_cat, **args, command=lambda: self.selected_menu(1))
        img_donut = ct.CTkImage(Image.open('icons/tools/donut_chart.png'), size=size)
        bt_donut = ct.CTkButton(self.f_2, image=img_donut, **args, command=lambda: self.selected_menu(2))
        img_bar = ct.CTkImage(Image.open('icons/tools/column_chart.png'), size=size)
        bt_bar = ct.CTkButton(self.f_2, image=img_bar, **args, command=lambda: self.selected_menu(3))
        img_exch = ct.CTkImage(Image.open('icons/tools/exchange.png'), size=size)
        bt_exch = ct.CTkButton(self.f_2, image=img_exch, **args, command=lambda: self.selected_menu(4))
        light_img = 'icons/tools/transfer light.png'
        dark_img = 'icons/tools/transfer dark.png'
        img_trans = ct.CTkImage(light_image=Image.open(light_img), dark_image=Image.open(dark_img), size=size)
        bt_trans = ct.CTkButton(self.f_2, image=img_trans, **args, command=lambda: self.selected_menu(5))

        bt_wallet.grid(row=0, column=0, columnspan=1, pady=(3, 0))
        bt_cat.grid(row=0, column=1, columnspan=1, pady=(3, 0))
        bt_donut.grid(row=0, column=2, columnspan=1, pady=(3, 0))
        bt_bar.grid(row=0, column=3, columnspan=1, pady=(3, 0))
        bt_exch.grid(row=0, column=4, columnspan=1, pady=(3, 0))
        bt_trans.grid(row=0, column=5, columnspan=1, pady=(3, 0))
        CreateToolTip(bt_wallet, 'The current selected wallet')
        CreateToolTip(bt_cat, 'Show all categories')
        CreateToolTip(bt_donut, 'Show a chart of the income or expense')
        CreateToolTip(bt_bar, 'Show a bar chart of the income or expense')
        CreateToolTip(bt_exch, 'Show exchange rates')
        CreateToolTip(bt_trans, 'Transfer money between wallets')
        self.menu_list.append(bt_wallet)
        self.menu_list.append(bt_cat)
        self.menu_list.append(bt_donut)
        self.menu_list.append(bt_bar)
        self.menu_list.append(bt_exch)
        self.menu_list.append(bt_trans)

    def selected_menu(self, col):
        charts = Charts(self.root, self.f_2A, self.username, self.wallet)
        self.f_2A.configure(fg_color=self.h2)
        self.static.garbage_collect(self.f_2A)
        for index, item in enumerate(self.menu_list):
            if index != col:
                item.configure(fg_color='transparent', hover_color=self.h2)
        self.menu_list[col].configure(fg_color='gray', hover_color='gray')
        funcs = {0: self.balance_frame, 1: self.show_category_frame, 2: charts.donut_chart_frame,
                 3: charts.bar_plot_frame,  4: self.exchange_frame, 5: lambda: self.transfer_frame("INSERT")}
        if self.wallets:
            plt.close('all')
            funcs[col]()
        self.bar_list = charts.bar_list

    # FUNCTIONS THAT CREATES THE WIDGETS IN THE TRANSFER FRAME self.f_left----------------------------------------------
    def balance_frame(self):
        args = {'text': '', 'cursor': 'hand2', 'fg_color': "transparent", 'hover_color': self.h2, 'width': 1,
                'height': 1}
        size = (30, 30)
        self.settings_list.clear()
        self.f_2A.lift()
        if self.wallets:
            self.settings_toggle = True
            img_sett = ct.CTkImage(Image.open('icons/tools/settings 2.png'), size=size)
            bt_sett = ct.CTkButton(self.f_2A, image=img_sett, **args, command=self.wallet_settings)
            bt_sett.grid(row=0, column=0, rowspan=2, pady=(10, 0))

            img_edit = ct.CTkImage(Image.open('icons/tools/edit.png'), size=size)
            bt_edit = ct.CTkButton(self.f_2A, image=img_edit, **args,
                                   command=lambda: self.add_edit_wallet('UPDATE', True))
            self.settings_list.append(bt_edit)

            img_del = ct.CTkImage(Image.open('icons/tools/delete.png'), size=size)
            bt_del = ct.CTkButton(self.f_2A, image=img_del, **args, command=self.delete_wallet)
            self.settings_list.append(bt_del)

            l_balance = ct.CTkLabel(self.f_2A, text='Balance:', font=('Courier New', 55))
            l_balance.grid(row=2, column=0, rowspan=2, columnspan=10)

            data = self.functions.update_balance(self.wallet)
            total = "{:,}".format(float(data[2]))
            l_total = ct.CTkLabel(self.f_2A, text=f'{total} {data[3]}', font=('Helvetica', 40), width=500)
            l_total.grid(row=4, column=0, rowspan=2, columnspan=10)

            img_income = ct.CTkImage(Image.open('icons/tools/add_income.png'), size=(120, 120))
            bt_income = ct.CTkButton(self.f_2A, image=img_income, **args,
                                     command=lambda: self.movement_frame('+', 'INSERT'))
            bt_income.grid(row=6, column=0, rowspan=4, columnspan=5)

            img_expense = ct.CTkImage(Image.open('icons/tools/add_expense.png'), size=(120, 120))
            bt_expense = ct.CTkButton(self.f_2A, image=img_expense, **args,
                                      command=lambda: self.movement_frame('-', 'INSERT'))
            bt_expense.grid(row=6, column=4, rowspan=4, columnspan=6)

    # FUNCTION TO OPEN OR CLOSE THE WALLET SETTINGS BUTTONS-------------------------------------------------------------
    def wallet_settings(self):
        if self.settings_toggle:
            self.settings_toggle = False
            self.settings_list[0].grid(row=0, column=1, rowspan=2, columnspan=2, pady=(10, 0))
            self.settings_list[1].grid(row=0, column=3, rowspan=2, columnspan=2, pady=(10, 0))
        else:
            self.settings_toggle = True
            self.settings_list[0].grid_remove()
            self.settings_list[1].grid_remove()

    # FUNCTION THAT CREATES THE BALANCE FRAME WIDGETS self.right--------------------------------------------------------
    def fonts_frame(self):
        self.static.garbage_collect(self.f_2A)
        self.f_2A.lift()
        frame = ct.CTkScrollableFrame(self.f_2A, width=588, height=400)
        frame.grid(row=0, column=0)
        for i in range(len(fonts)):
            (ct.CTkLabel(frame, text=f'{fonts[i]} Balance: 20,541,546.25 ALL', font=(fonts[i], 25))
             .grid(row=i, column=0, pady=5, sticky='w'))

    # FUNCTION TO SHOW ALL THE CATEGORIES FRAME-------------------------------------------------------------------------
    def show_category_frame(self):

        def change_cursor_to_hand(tree, *_):
            tree.config(cursor="hand2")

        def change_cursor_to_arrow(tree, *_):
            tree.config(cursor="arrow")

        def toggle_add(tree=None, *_):
            if tree is not None:
                self.settings_toggle = True
                item = tree.selection()
                data_c = tree.item(item)['values']
                bt_confirm.configure(command=lambda: confirm_new(data_c))
                p = data_c[3].replace("icons/category/", "").rstrip(".png")
                e_name.delete(0, END)
                e_name.insert(0, data_c[1])
                radio_var.set(data_c[2])
                if data_c[2] == 'income':
                    rb_income.select()
                else:
                    rb_expense.select()
                new_img = ct.CTkImage(Image.open(data_c[3]), size=(40, 40))
                bt_select.configure(text=p, image=new_img)
                bt_cancel.configure(command=toggle_add)
                rb_income.configure(state='disabled')
                rb_expense.configure(state='disabled')

            if self.settings_toggle:
                e_name.grid(row=0, column=0, rowspan=2, columnspan=3, padx=(30, 0))
                rb_income.grid(row=0, column=3, columnspan=2)
                rb_expense.grid(row=1, column=3, columnspan=2)
                bt_select.grid(row=0, column=5, rowspan=2, columnspan=3, sticky='w')
                bt_confirm.grid(row=0, column=8, rowspan=2)
                bt_cancel.grid(row=0, column=9, rowspan=2)
                self.settings_toggle = False
            else:
                e_name.grid_remove()
                rb_income.grid_remove()
                rb_expense.grid_remove()
                bt_select.grid_remove()
                bt_confirm.grid_remove()
                bt_cancel.grid_remove()

                e_name.delete(0, END)
                rb_income.select()
                rb_income.configure(state='normal')
                rb_expense.configure(state='normal')
                bt_select.configure(image=img_select, text='Select')
                self.settings_toggle = True

        def confirm_delete(tree):
            item = tree.selection()
            data_c = tree.item(item)['values']
            ask = messagebox.askquestion("Delete", f"Are you sure you want to delete {data_c[1]}?")
            if ask == 'yes':
                self.functions.delete_category(data_c[1], data_c[4])
                self.show_category_frame()
                self.tree_toggle()

        def confirm_new(edit=None):
            name = e_name.get()
            category = self.functions.get_categories()
            count = sum(1 for cat in category if not cat[1].startswith('TO-') and not cat[1].startswith('FROM-'))
            if name == '':
                messagebox.showerror('Error', 'Please enter a name', parent=self.f_2A)
                return

            elif len(name) < 3 or len(name) > 12:
                messagebox.showerror("Error", "Name must be between 3 and 12 characters", parent=self.f_2A)
                return

            elif name.startswith('TO-') or name.startswith('FROM-'):
                messagebox.showerror("Error", "Name cannot start with 'TO-' or 'FROM-'", parent=self.f_2A)
                return

            elif count >= 30:
                messagebox.showerror("Error", "You can only have 30 categories", parent=self.f_2A)
                return

            elif self.functions.category_exist(name.capitalize()) and (
                    edit is None or edit[1].lower() != name.lower()):
                messagebox.showerror('Error', 'Name already exists', parent=self.f_2A)
                return

            elif bt_select.cget('text') == '':
                messagebox.showerror('Error', 'Please select a type', parent=self.f_2A)
                return

            else:
                path = f'icons/category/{bt_select.cget('text')}'
                if edit is not None:
                    self.functions.create_update_category(name.capitalize(), radio_var.get(), path, 'UPDATE', edit)
                else:
                    self.functions.create_update_category(name.capitalize(), radio_var.get(), path, 'INSERT')
                self.show_category_frame()

        def tree3_disabled(tree, event):
            item = tree.identify_row(event.y)
            if 'disabled' in tree.item(item, 'tags'):
                return
            toggle_add(tree)

        def tree4_disabled(tree, event):
            item = tree.identify_row(event.y)
            if 'disabled' in tree.item(item, 'tags'):
                return
            self.show_merge_options(tree, event)

        def tree5_disabled(tree, event):
            item = tree.identify_row(event.y)
            if 'disabled' in tree.item(item, 'tags'):
                return
            confirm_delete(tree)

        self.static.garbage_collect(self.f_2A)
        self.settings_toggle = True
        hw = 13
        args1 = {'text': '', 'cursor': 'hand2', 'fg_color': "transparent", 'hover_color': self.h2,
                 'width': 1, 'height': 1}
        args2 = {'radiobutton_width': hw, 'radiobutton_height': hw, 'border_width_checked': 3,
                 'border_width_unchecked': 3}
        frame = ct.CTkScrollableFrame(self.f_2A, width=586, height=350, fg_color=self.h2)
        xy = 20
        img_edit = ImageTk.PhotoImage(Image.open('icons/tools/edit.png').resize((xy, xy)))
        img_merge = ImageTk.PhotoImage(Image.open('icons/tools/merge_categories.png').resize((xy, xy)))
        img_delete = ImageTk.PhotoImage(Image.open('icons/tools/delete.png').resize((xy, xy)))
        categories = self.functions.get_categories()
        data = self.functions.all_category_view()
        d1 = {item[0]: item[3] for item in data}
        d2 = {item[0]: item[4] for item in data}

        tree1 = ttk.Treeview(frame, style='CustomTreeview.Treeview', show='tree', height=len(categories))
        tree1.column('#0', width=80, minwidth=80)

        tree2 = ttk.Treeview(frame, style='CustomTreeview.Treeview', show='tree', height=len(categories))
        tree2["columns"] = ("name", "type", "total")
        tree2.column("#0", width=0, stretch=NO)
        tree2.column("name", width=120, anchor="w")
        tree2.column("type", width=30, anchor="center")
        tree2.column("total", width=220, anchor='w')

        tree3 = ttk.Treeview(frame, style='CustomTreeview.Treeview', show='tree', height=len(categories))
        tree3.column('#0', width=40, minwidth=40, anchor='e')
        tree4 = ttk.Treeview(frame, style='CustomTreeview.Treeview', show='tree', height=len(categories))
        tree4.column('#0', width=40, minwidth=40, anchor='e')
        tree5 = ttk.Treeview(frame, style='CustomTreeview.Treeview', show='tree', height=len(categories))
        tree5.column('#0', width=40, minwidth=40, anchor='e')

        tree1.images = {}
        tree3.img_edit = img_edit
        tree4.img_merge = img_merge
        tree5.img_delete = img_delete
        tree2.tag_configure('income', foreground='#7CB342')
        tree2.tag_configure('expense', foreground='#E53935')

        for c in categories:
            image_path = c[3]
            if image_path not in tree1.images:
                img = ImageTk.PhotoImage(Image.open(image_path).resize((40, 40)))
                tree1.images[image_path] = img
            else:
                img = tree1.images[image_path]
            ctype = self.exp_type[c[2]]
            total = d1.get(c[1], 0)
            num = d2.get(c[1], 0)
            if c[2] == 'income':
                color_tag = 'income'
            elif c[2] == 'expense':
                color_tag = 'expense'
            else:
                color_tag = ''

            if c[1].startswith('TO-') or c[1].startswith('FROM-'):
                tree2.insert('', 'end', text='', values=(c[1], ctype, f'{total} ({num})'),
                             tags=('disabled', color_tag))
                tree1.insert('', 'end', text='', image=img, tags=('disabled',))
                tree3.insert('', 'end', text='', image=tree3.img_edit, values=c, tags=('disabled',))
                tree4.insert('', 'end', text='', image=tree4.img_merge, values=c, tags=('disabled',))
                tree5.insert('', 'end', text='', image=tree5.img_delete, values=c, tags=('disabled',))
            else:
                tree1.insert('', 'end', text='', image=img)
                tree2.insert('', 'end', text='', values=(c[1], ctype, f'{total} ({num})'), tags=(color_tag,))
                tree3.insert('', 'end', text='', image=tree3.img_edit, values=c)
                tree4.insert('', 'end', text='', image=tree4.img_merge, values=c)
                tree5.insert('', 'end', text='', image=tree5.img_delete, values=c)

        # for c in categories:
        #     if c[2] == 'expense' and check:
        #         Frame(frame, width=585, height=1, bd=5, relief='sunken').grid(row=row, column=0, columnspan=10)
        #         check = False
        #         row += 1
        #     if c[1].startswith('TO-') or c[1].startswith('FROM-'):
        #         continue
        #     img_icon = ct.CTkImage(Image.open(c[3]), size=(40, 40))
        #     bt_icon = ct.CTkButton(frame, image=img_icon, **args1)
        #     font = self.static.calculate_font_size(c[1], base_size=25, min_size=14)
        #     l_name = ct.CTkLabel(frame, text=c[1], font=('Arial', font))
        #     l_type = ct.CTkLabel(frame, text=self.exp_type[c[2]], font=('Arial', 25, 'italic'))
        #     l_type.configure(text_color='green' if c[2] == 'income' else 'red')
        #     total = d1.get(c[1])
        #     num = d2.get(c[1])
        #     font = self.static.calculate_font_size(str(total), base_size=25, min_size=14)
        #     l_total = ct.CTkLabel(frame, text='', font=('Arial', font), width=150, anchor='w')
        #     if total is not None:
        #         l_total.configure(text=f'{total} ({num})')
        #     bt_edit = ct.CTkButton(frame, image=img_edit, **args1)
        #     bt_edit.configure(command=lambda n=c: (setattr(self, 'settings_toggle', True), toggle_add(n)))
        #     bt_merge = ct.CTkButton(frame, image=img_merge, **args1)
        #     bt_merge.configure(state=self.status[self.role])
        #     bt_merge.bind("<Button-1>", lambda event, c_data=c: self.show_merge_options(event, c_data))
        #     bt_delete = ct.CTkButton(frame, image=img_delete, **args1)
        #     bt_delete.configure(command=lambda n=c[1], m=c[4]: confirm_delete(n, m), state=self.status[self.role])
        #
        #     bt_icon.grid(row=row, column=0, pady=5)
        #     l_name.grid(row=row, column=1, sticky='w')
        #     l_type.grid(row=row, column=2)
        #     l_total.grid(row=row, column=3, sticky='w')
        #     bt_edit.grid(row=row, column=7, sticky='e')
        #     bt_merge.grid(row=row, column=8, sticky='e')
        #     bt_delete.grid(row=row, column=9, sticky='e')
        #     row += 1

        l_add = ct.CTkLabel(self.f_2A, text='+', cursor='hand2', font=('Times New Roman', 50))
        l_add.bind('<Button-1>', lambda e: toggle_add())
        e_name = ct.CTkEntry(self.f_2A, placeholder_text='New category name', font=('Arial', 12))
        radio_var = StringVar(value='income')
        rb_income = ct.CTkRadioButton(self.f_2A, text='Income', variable=radio_var, value='income', **args2)
        rb_expense = ct.CTkRadioButton(self.f_2A, text='Expense', variable=radio_var, value='expense', **args2)
        img_select = ct.CTkImage(Image.open('icons/tools/choose_category.png'), size=(40, 40))
        bt_select = ct.CTkButton(self.f_2A, image=img_select, text='Select', cursor='hand2', fg_color='transparent',
                                 hover_color=self.h2, text_color=('black', 'white'))
        bt_select.configure(command=lambda: self.category_icon('category', bt_select, 40, 40))
        img_confirm = ct.CTkImage(Image.open('icons/tools/action_confirm.png'), size=(20, 20))
        bt_confirm = ct.CTkButton(self.f_2A, image=img_confirm, **args1, command=confirm_new)
        img_cancel = ct.CTkImage(Image.open('icons/tools/action_cancel.png'), size=(20, 20))
        bt_cancel = ct.CTkButton(self.f_2A, image=img_cancel, **args1, command=toggle_add)
        CreateToolTip(l_add, 'Create a new category')
        CreateToolTip(bt_select, 'Select an icon for the category ooooo ooo ooooo oooooooo oooo oooo oo oo ooooooo')

        tree3.bind("<Enter>", lambda e: change_cursor_to_hand(tree3))
        tree3.bind("<Leave>", lambda e: change_cursor_to_arrow(tree3))
        # tree3.bind("<ButtonRelease-1>", lambda e: toggle_add(tree3))

        tree3.bind("<ButtonRelease-1>", lambda e: tree3_disabled(tree3, e))
        tree4.bind("<Enter>", lambda e: change_cursor_to_hand(tree4))
        tree4.bind("<Leave>", lambda e: change_cursor_to_arrow(tree4))
        tree4.bind("<ButtonRelease-1>", lambda e: tree4_disabled(tree4, e))
        # tree4.bind("<ButtonRelease-1>", lambda e: self.show_merge_options(tree4, e))

        tree5.bind("<Enter>", lambda e: change_cursor_to_hand(tree5))
        tree5.bind("<Leave>", lambda e: change_cursor_to_arrow(tree5))
        tree5.bind("<ButtonRelease-1>", lambda e: tree5_disabled(tree5, e))
        # tree5.bind("<ButtonRelease-1>", lambda e: confirm_delete(tree5))
        tree1.grid(row=0, column=0)
        tree2.grid(row=0, column=1)
        tree3.grid(row=0, column=2)
        tree4.grid(row=0, column=3)
        tree5.grid(row=0, column=4)
        frame.grid(row=2, column=0, columnspan=10, pady=(0, 7), sticky='s')
        l_add.grid(row=0, column=0, rowspan=2, sticky='w', padx=(10, 0))
        self.f_2A.lift()

    # FUNCTION TO SHOW THE OPTIONS TO MERGE TWO CATEGORIES--------------------------------------------------------------
    def show_merge_options(self, tree, event):
        def confirm_merge(c_data):
            ask = messagebox.askyesno("Confirm", f"Are you sure you want to merge {data[1]} with {c_data[1]}?")
            if ask:
                self.functions.merge_categories(c_data[1], data[1])
                self.show_category_frame()
                self.tree_toggle()

        item = tree.selection()
        data = tree.item(item)['values']
        merge_menu = Menu(None, tearoff=0, relief='sunken', bg=self.c1[self.theme], fg=self.fg[self.theme],
                          activebackground=self.c2[self.theme], activeforeground=self.fg[self.theme])
        merge_menu.add_command(label=f"Merge {data[1]} with:")
        categories = self.functions.get_merge_categories(data[1], data[2])
        for i in categories:
            merge_menu.add_command(label=i[1], command=lambda n=i: confirm_merge(n))
        merge_menu.post(event.x_root, event.y_root)

    # FUNCTIONS THAT CREATES THE WIDGETS IN THE INSERT TRANSFER FRAME self.f_2A8----------------------------------------
    def transfer_frame(self, action, edit=None):

        def confirm_transfer(id1=None, id2=None):
            amount = self.static.validate_input_number(e_sum, self.f_2A)
            if amount is None:
                return

            date_str = bt_calendar.cget('text')
            date_ob = datetime.strptime(date_str, "%d-%m-%Y")
            c_date = date_ob.strftime("%Y-%m-%d")
            wallet_1 = bt_1.cget('text')
            wallet_2 = bt_2.cget('text')
            if wallet_2 == 'Choose':
                messagebox.showerror("Error", "Select a wallet", parent=self.f_2A)
                return
            transfer_id = str(f'UUID-{uuid.uuid4()}')

            if edit is not None:
                transfer_id = edit

            data_1 = [self.username, wallet_1, f"TO-{wallet_2}", amount, c_date, transfer_id, "expense"]
            data_2 = [self.username, wallet_2, f"FROM-{wallet_1}", amount, c_date, transfer_id, "income"]
            self.functions.transfer(action, data_1, id1)
            self.functions.transfer(action, data_2, id2)

            self.tree_toggle()
            self.selected_menu(0)

        def delete_transfer():
            ask = messagebox.askyesno("Confirm", "Are you sure you want to delete this transfer?", parent=self.f_2A)
            if ask:
                self.functions.delete_transfer(edit)
                self.tree_toggle()
                self.f_2A.lift()
            else:
                pass
            self.selected_menu(0)

        data = self.functions.update_balance(self.wallet)
        args = {'text': '', 'cursor': 'hand2', 'fg_color': "transparent", 'hover_color': self.h2, 'width': 1,
                'height': 1}
        size = (130, 130)
        oid1, oid2 = None, None
        current_date = date.today().strftime("%d-%m-%Y")
        img_calendar = ct.CTkImage(Image.open('icons/tools/calendar.png'), size=(60, 60))
        bt_calendar = ct.CTkLabel(self.f_2A, text=current_date, image=img_calendar, cursor='hand2', font=('Arial', 27),
                                  compound='left')
        bt_calendar.bind('<Button-1>', lambda event: self.static.grab_date(self.f_2A, bt_calendar))

        img_delete = ct.CTkImage(Image.open('icons/tools/delete.png'), size=(25, 25))
        bt_delete = ct.CTkButton(self.f_2A, image=img_delete, command=delete_transfer, **args)

        # LEFT BUTTON THAT SHOWS THE WALLET FROM WHICH THE TRANSFER WILL BE DONE----------------------------------------
        l_from = ct.CTkLabel(self.f_2A, text="From", font=('Arial', 30, 'bold'))
        l_to = ct.CTkLabel(self.f_2A, text="To", font=('Arial', 30, 'bold'))
        img_1 = ct.CTkImage(Image.open(data[6]), size=size)
        bt_1 = ct.CTkLabel(self.f_2A, text=data[1], image=img_1, compound='top', cursor='hand2')
        img_2 = ct.CTkImage(Image.open('icons/tools/choose_category.png'), size=size)
        bt_2 = ct.CTkLabel(self.f_2A, image=img_2, text='Choose', compound='top', cursor='hand2')
        bt_1.bind('<Button-1>', lambda event: self.transfer_icon(bt_1, bt_2, data))
        bt_2.bind('<Button-1>', lambda event: self.transfer_icon(bt_2, bt_1, data))

        # ENTRY TO INSERT THE SUM TO BE TRANSFERRED AND THE COIN USED --------------------------------------------------
        img_arrow = ct.CTkImage(Image.open('icons/tools/transfer_arrow.png'), size=(220, 25))
        l_arrow = ct.CTkLabel(self.f_2A, image=img_arrow, text="")
        e_sum = ct.CTkEntry(self.f_2A, font=('Arial', 25), width=170, height=50, placeholder_text='Sum')
        l_coin = ct.CTkLabel(self.f_2A, text=data[3], font=('Arial', 25))

        # CONFIRM AND CANCEL BUTTON FOR THE TRANSACTION-----------------------------------------------------------------
        img_confirm = ct.CTkImage(Image.open('icons/tools/action_confirm.png'), size=(35, 35))
        bt_confirm = ct.CTkButton(self.f_2A, image=img_confirm, command=confirm_transfer, **args)
        img_cancel = ct.CTkImage(Image.open('icons/tools/action_cancel.png'), size=(35, 35))
        bt_cancel = ct.CTkButton(self.f_2A, image=img_cancel, command=self.balance_frame, **args)

        bt_calendar.grid(row=0, column=0, rowspan=2, columnspan=10)
        l_from.grid(row=0, column=0, rowspan=4, columnspan=3)
        l_to.grid(row=0, column=7, rowspan=4, columnspan=3)
        bt_1.grid(row=0, column=0, rowspan=10, columnspan=3)
        bt_2.grid(row=0, column=7, rowspan=10, columnspan=3)
        l_arrow.grid(row=3, column=0, rowspan=2, columnspan=10)
        e_sum.bind('<Control-BackSpace>', self.static.entry_ctrl_delete)
        # e_sum.grid(row=5, column=3, rowspan=3, columnspan=3)
        e_sum.place(x=195, y=238)
        l_coin.grid(row=5, column=6, rowspan=3, columnspan=2)
        bt_confirm.grid(row=8, column=3, rowspan=2, columnspan=2)
        bt_cancel.grid(row=8, column=5, rowspan=2, columnspan=2)

        # LOGIC TO CHECK IF THIS IS A NEW TRANSFER OR AN EDIT-----------------------------------------------------------
        if edit is not None:
            t_data = self.functions.get_transfer_data(edit)
            date_obj = datetime.strptime(t_data[0][4], '%Y-%m-%d')
            new_date = date_obj.strftime('%d-%m-%Y')
            bt_calendar.configure(text=new_date)

            img_1 = ct.CTkImage(Image.open(t_data[0][8]), size=size)
            bt_1.configure(text=t_data[0][1], image=img_1)
            e_sum.insert(0, t_data[0][3])

            img_2 = ct.CTkImage(Image.open(t_data[1][8]), size=size)
            bt_2.configure(text=t_data[1][1], image=img_2)
            oid1 = t_data[0][7]
            oid2 = t_data[1][7]
            bt_confirm.configure(command=lambda: confirm_transfer(oid1, oid2))
            bt_delete.grid(row=0, column=8, columnspan=2)

        self.f_2A.lift()

    # FUNCTION TO DELETE THE CURRENT SELECTED WALLET--------------------------------------------------------------------
    def delete_wallet(self):
        ask = messagebox.askyesno("Confirm", "Are you sure you want to delete this wallet?")
        if ask:
            self.functions.delete_wallet(self.wallet, self.walled_oid)
            self.settings_toggle = True
            self.wallets = self.functions.retrieve_wallets()
            self.wallets_frame()
            self.balance_frame()

    # FUNCTION THAT CREATES THE EXCHANGE FRAME self.f_2A2---------------------------------------------------------------
    def exchange_frame(self):

        self.f_2A.configure(fg_color=self.h1)
        args1 = {'corner_radius': 13, 'border_width': 2, 'fg_color': self.h2}
        args2 = {'values': coins, 'width': 67, 'font': ('Arial', 12, 'bold'), 'fg_color': self.h2, "anchor": "center",
                 'text_color': ('black', 'white'), 'button_color': self.h2, 'button_hover_color': self.h2}

        f_left = ct.CTkFrame(self.f_2A, width=297, height=194, **args1)
        f_left.grid_propagate(False)
        for i in range(6):
            f_left.rowconfigure(i, weight=1)

        f_right = ct.CTkFrame(self.f_2A, width=297, height=194, **args1)
        f_right.grid_propagate(False)
        for i in range(6):
            f_right.rowconfigure(i, weight=1)
            f_right.columnconfigure(i, weight=1)

        f_bot = ct.CTkFrame(self.f_2A, width=600, height=200, **args1)

        data_b = self.functions.update_balance(self.wallet)  # get the current coin
        font1 = ('Helvetica', 16, 'bold')
        font2 = ('Helvetica', 15, 'bold')
        l_income = ct.CTkLabel(f_left, text='Income:', font=font1)
        total_i = ct.CTkLabel(f_left, font=font2, text='')
        sv_income = StringVar(value=data_b[3])
        om_income = ct.CTkOptionMenu(f_left, variable=sv_income, **args2,
                                     command=lambda n=sv_income, m=0: self.update_exchange2(n, m))

        l_expense = ct.CTkLabel(f_left, text='Expense:', font=font1)
        total_e = ct.CTkLabel(f_left, font=font2, text='')
        sv_expense = StringVar(value=data_b[3])
        om_expense = ct.CTkOptionMenu(f_left, variable=sv_expense, **args2,
                                      command=lambda n=sv_expense, m=1: self.update_exchange2(n, m))

        l_balance = ct.CTkLabel(f_left, text='Balance:', font=font1)
        total_b = ct.CTkLabel(f_left, font=font2, text='')
        sv_balance = StringVar(value=data_b[3])
        om_balance = ct.CTkOptionMenu(f_left, variable=sv_balance, **args2,
                                      command=lambda n=sv_balance, m=2: self.update_exchange2(n, m))

        def on_click_convert():
            sum_value = self.static.validate_input_number(e_sum, self.f_2A)
            if sum_value is None:
                return
            self.functions.exchange_rate(sv_coin1.get(), sv_coin2.get(), sum_value, l_sum, l_rate)

        e_sum = ct.CTkEntry(f_right, font=('helvetica', 15), placeholder_text='convert sum')
        e_sum.grid(row=0, column=0, rowspan=2, columnspan=3)
        sv_coin1 = ct.StringVar(value=data_b[3])
        om_coin1 = ct.CTkOptionMenu(f_right, variable=sv_coin1, **args2)
        om_coin1.grid(row=0, column=3, rowspan=2, columnspan=3, sticky='w')

        bt_convert = ct.CTkButton(f_right, text='Convert', font=font1, width=30)
        bt_convert.grid(row=2, column=0, rowspan=2, columnspan=3)
        bt_convert.configure(command=on_click_convert)

        l_rate = ct.CTkLabel(f_right, text='Rate:', font=font1, anchor='w')
        l_rate.grid(row=2, column=2, rowspan=2, columnspan=4)

        l_sum = ct.CTkLabel(f_right, font=font1, text='', width=140, fg_color=self.h1, corner_radius=7, anchor='w')
        l_sum.grid(row=4, column=0, rowspan=2, columnspan=3)
        sv_coin2 = ct.StringVar(value=data_b[3])
        om_coin2 = ct.CTkOptionMenu(f_right, variable=sv_coin2, **args2)
        om_coin2.grid(row=4, column=3, rowspan=2, columnspan=3, sticky='w')

        # GRID FRAMES INSIDE THE EXCHANGE FRAME-------------------------------------------------------------------------
        f_left.grid(row=0, column=0, rowspan=5, columnspan=5, pady=(5, 0))
        f_right.grid(row=0, column=5, rowspan=5, columnspan=5, pady=(5, 0))
        f_bot.grid(row=5, column=0, columnspan=10, pady=(7, 0))

        # GRID WIDGETS INSIDE THE LEFT FRAME----------------------------------------------------------------------------
        l_income.grid(row=0, rowspan=2, column=0, padx=(5, 0), sticky='e')
        total_i.grid(row=0, rowspan=2, column=2, sticky='w')
        om_income.grid(row=0, rowspan=2, column=1)
        l_expense.grid(row=2, rowspan=2, column=0, padx=(5, 0), sticky='e')
        total_e.grid(row=2, rowspan=2, column=2, sticky='w')
        om_expense.grid(row=2, rowspan=2, column=1)
        l_balance.grid(row=4, rowspan=2, column=0, padx=(5, 0), sticky='e')
        total_b.grid(row=4, rowspan=2, column=2, sticky='w')
        om_balance.grid(row=4, rowspan=2, column=1)

        self.exchange_list.clear()
        self.exchange_list.append([total_i, total_e, total_b])
        self.exchange_list.append([sv_income, sv_expense, sv_balance])
        self.exchange_list.append([om_income, om_expense, om_balance])
        self.update_exchange()
        self.f_2A.lift()

    def update_exchange(self):
        total_income, total_expense = self.functions.wallet_total(self.wallet)  # get total income and expense
        total_income = 0 if total_income is None else total_income
        total_expense = 0 if total_expense is None else total_expense
        data_b = self.functions.update_balance(self.wallet)  # get the current balance
        if data_b is not None:
            if data_b[2].is_integer():
                balance = "{:.0f}".format(float(data_b[2]))  # convert the sum to a float with 2 decimals
            else:
                balance = "{:.2f}".format(float(data_b[2]))
        else:
            balance = 0

        self.exchange_list[0][0].configure(text=total_income)  # update the total income in the exchange
        self.exchange_list[0][1].configure(text=total_expense)  # update the total expense in the exchange
        self.exchange_list[0][2].configure(text=balance)  # update the current balance in the exchange

    def update_exchange2(self, var, index):
        total_income, total_expense = self.functions.wallet_total(self.wallet)  # get total income and expense
        total_income = 0 if total_income is None else total_income
        total_expense = 0 if total_expense is None else total_expense
        data_b = self.functions.update_balance(self.wallet)  # get the current balance
        balance = "{:.2f}".format(float(data_b[2]))  # convert the sum to a float with 2 decimals
        nums = [total_income, total_expense, balance]

        if var is not None:
            self.functions.exchange_rate(data_b[3], var, nums[index], self.exchange_list[0][index])
            self.exchange_list[1][index].set(var)

    # FUNCTION THAT CREATES THE MOVEMENTS FRAME WIDGETS self.f_2A3------------------------------------------------------
    def movement_frame(self, operation, action, edit=None, search=None, *_):
        def on_notes_click(*_):  # clear the 'Insert notes' when clicking inside the notes
            if notes.get(1.0, "end-1c") == 'Insert notes':
                notes.delete(1.0, "end-1c")

        def on_notes_focus_out(*_):  # insert 'Insert notes' when leaving the notes
            if not notes.get(1.0, "end-1c").strip():
                notes.insert(1.0, 'Insert notes')

        def click_on_widget():
            x, y = pyautogui.position()  # Get the current mouse position
            pyautogui.click(x, y)

        def autofill(*_):
            text = notes.get(1.0, "end-1c")
            if len(text) >= 3:
                data = self.functions.autocomplete(text)
                show_suggestions(data)

        def show_suggestions(suggestions):
            autocomplete_menu.delete(0, END)
            for suggestion in suggestions:
                autocomplete_menu.add_command(label=suggestion, command=lambda sug=suggestion: insert_suggestion(sug))
            try:
                autocomplete_menu.tk_popup(notes.winfo_pointerx() + 10, notes.winfo_pointery() + 10)
            except:
                pass

        def insert_suggestion(suggestion):
            notes.delete(1.0, "end-1c")
            notes.insert(INSERT, suggestion)
            autocomplete_menu.unpost()

        def collect_data():  # collect the data from the widgets and send it to the database
            sum_value = self.static.validate_input_number(e_sum, self.f_2A)
            if sum_value is None:
                return
            notes_text = str(notes.get(1.0, "end-1c")).strip()
            if notes_text == "Insert notes" or notes_text.startswith('UUID-'):
                notes_text = ""

            if btn.cget('text') == 'Select':
                messagebox.showerror("Error", "Select a category", parent=self.f_2A)
                return

            date_str = bt_calendar.cget('text')
            date_ob = datetime.strptime(date_str, "%d-%m-%Y")
            formatted_date = date_ob.strftime("%Y-%m-%d")
            data = [btn.cget('text'), sum_value, formatted_date, notes_text, self.exp_type2[operation]]
            if action == 'INSERT':
                self.functions.create_update_movement(action, self.wallet, None, *data)
            else:
                self.functions.create_update_movement(action, self.wallet, v[7], *data)

            if search is not None:
                self.tree_search_frame(search)
            else:
                self.tree_toggle()
            self.selected_menu(0)

        self.static.garbage_collect(self.f_2A)
        import pyautogui
        args = {'text': '', 'cursor': 'hand2', 'fg_color': "transparent", 'hover_color': self.h2, 'width': 1,
                'height': 1}
        size = (60, 60)
        current_date = date.today().strftime("%d-%m-%Y")
        img_calendar = ct.CTkImage(Image.open('icons/tools/calendar.png'), size=size)
        bt_calendar = ct.CTkLabel(self.f_2A, text=current_date, image=img_calendar, cursor='hand2', font=('Arial', 27),
                                  compound='left')
        bt_calendar.bind('<Button-1>', lambda event: self.static.grab_date(self.f_2A, bt_calendar))
        l_operation = ct.CTkLabel(self.f_2A, text=operation, font=('Arial', 30), width=1, height=1)
        e_sum = ct.CTkEntry(self.f_2A, font=('Arial', 25), width=170, height=50, placeholder_text='Sum')
        e_sum.bind('<Control-BackSpace>', self.static.entry_ctrl_delete)
        notes = ct.CTkTextbox(self.f_2A, font=('Arial', 22), width=220, height=160)
        notes.insert(1.0, 'Insert notes')
        notes.bind("<Button-1>", on_notes_click)
        notes.bind("<FocusOut>", on_notes_focus_out)
        notes.bind('<Control-BackSpace>', self.static.entry_ctrl_delete)
        notes.bind('<KeyRelease>', autofill)
        autocomplete_menu = Menu(notes, tearoff=0, font=('Arial', 18))

        xy = 200
        img = ct.CTkImage(Image.open('icons/tools/choose_category.png'), size=(xy, xy))
        btn = ct.CTkButton(self.f_2A, image=img, text='Select', fg_color="transparent", cursor='hand2', compound='top',
                           hover_color=self.h2, width=1, height=1, text_color=('black', 'white'))
        btn.configure(command=lambda: self.movement_icon(btn, operation))
        img_delete = ct.CTkImage(Image.open('icons/tools/delete.png'), size=(25, 25))
        bt_delete = ct.CTkButton(self.f_2A, image=img_delete, **args)
        bt_delete.configure(state=self.status[self.role])
        img_confirm = ct.CTkImage(Image.open('icons/tools/action_confirm.png'), size=size)
        bt_confirm = ct.CTkButton(self.f_2A, image=img_confirm, **args)
        bt_confirm.configure(command=collect_data, state=self.status[self.role])
        img_cancel = ct.CTkImage(Image.open('icons/tools/action_cancel.png'), size=size)
        bt_cancel = ct.CTkButton(self.f_2A, image=img_cancel, **args)
        bt_cancel.configure(command=lambda: (self.selected_menu(0), setattr(self, 'settings_toggle', True)))

        bt_calendar.grid(row=0, column=0, rowspan=2, columnspan=3, padx=(15, 0), sticky='w')
        l_operation.grid(row=2, column=0, rowspan=3, columnspan=1, sticky='w', padx=(15, 0))
        e_sum.grid(row=2, column=0, rowspan=3, columnspan=3, padx=(50, 0), sticky='w')
        notes.grid(row=5, column=0, rowspan=5, columnspan=3, padx=(10, 0), pady=(0, 15), sticky='w')
        btn.grid(row=0, column=3, rowspan=6, columnspan=7)
        bt_confirm.grid(row=6, column=4, rowspan=4, columnspan=3)
        bt_cancel.grid(row=6, column=7, rowspan=4, columnspan=3)

        if edit is not None:
            selected = edit.focus()
            v = edit.item(selected, 'values')
            date_obj = datetime.strptime(v[4], '%Y-%m-%d')
            new_date = date_obj.strftime('%d-%m-%Y')
            bt_calendar.configure(text=new_date)
            l_operation.configure(text=self.exp_type[v[6]])
            e_sum.insert(0, v[3])
            notes.delete("1.0", "end")
            notes.insert("1.0", v[5])
            new_image = ct.CTkImage(Image.open(v[8]), size=(xy, xy))
            btn.configure(image=new_image, text=v[2])
            bt_delete.configure(command=lambda n=v[7]: self.delete_movement(n, search))
            bt_delete.grid(row=0, column=8, rowspan=2, columnspan=2, padx=(0, 10), sticky='e')

    def delete_movement(self, oid, search):  # delete the movement from the database
        ask = messagebox.askyesno("Confirm", "Are you sure you want to delete this movement?",
                                  parent=self.f_2A)
        if ask:
            self.functions.delete_movement(oid)
            if search is not None:
                self.tree_search_frame(search)
            else:
                self.tree_toggle()
            self.selected_menu(0)

    # FUNCTION TO CREATE THE WIDGETS FOR THE TREE MENU FRAME self.f_2B1-------------------------------------------------
    def tree_menu_frame(self):

        def change(string):
            self.l_range.configure(text=string)
            months = {'Day': '%Y-%m-%d', 'Mon': '%Y-%m', 'Year': '%Y'}
            self.c_toggle = False
            self.tree_date_frame(months[string])

        args = {'text': '', 'cursor': 'hand2', 'fg_color': "transparent", 'hover_color': self.h1, 'width': 1,
                'height': 1}
        args2 = {'cursor': 'hand2', 'bg_color': self.h2, 'font': ('Arial', 17, 'bold')}

        xy = 40
        e_src = ct.CTkEntry(self.f_3, placeholder_text='Search', font=('Arial', 20), width=180, height=40)
        e_src.bind('<Control-BackSpace>', self.static.entry_ctrl_delete)
        e_src.bind('<KeyRelease>', lambda e: self.tree_search_frame(e_src.get()))
        e_src.grid(row=0, column=0, rowspan=2, columnspan=6, pady=15)

        light_sort = 'icons/tools/sort_by_category_light.png'
        dark_sort = 'icons/tools/sort_by_category_dark.png'
        img_sort = ct.CTkImage(light_image=Image.open(light_sort), dark_image=Image.open(dark_sort), size=(xy, xy))
        bt_sort = ct.CTkButton(self.f_3, image=img_sort, **args)
        bt_sort.configure(command=lambda: (self.switch_tree(bt_sort), e_src.delete(0, END)))
        bt_sort.grid(row=0, column=6, rowspan=2, columnspan=2, pady=15)

        bt_day = ct.CTkLabel(self.f_3, text='Day', **args2, fg_color='transparent')
        bt_day.bind('<Button-1>', lambda e: (change('Day'), self.calendar_range()))
        bt_month = ct.CTkLabel(self.f_3, text='Mon', **args2, fg_color='transparent')
        bt_month.bind('<Button-1>', lambda e: (change('Mon'), self.calendar_range()))
        bt_year = ct.CTkLabel(self.f_3, text='Year', **args2, fg_color='transparent')
        bt_year.bind('<Button-1>', lambda e: (change('Year'), self.calendar_range()))
        self.calendar_list.append(bt_day)
        self.calendar_list.append(bt_month)
        self.calendar_list.append(bt_year)

    def calendar_range(self):
        if self.calendar_toggle:
            self.calendar_toggle = False
            self.calendar_list[0].grid(row=1, column=8, rowspan=2, columnspan=2, pady=(20, 0))
            self.calendar_list[1].grid(row=2, column=8, rowspan=2, columnspan=2, pady=(10, 0))
            self.calendar_list[2].grid(row=3, column=8, rowspan=2, columnspan=2)
        else:
            self.calendar_toggle = True
            self.calendar_list[0].grid_forget()
            self.calendar_list[1].grid_forget()
            self.calendar_list[2].grid_forget()

    # FUNCTION TO CREATE A TREEVIEW OF THE WALLET MOVEMENTS-------------------------------------------------------------
    def tree_category_frame(self):

        self.static.garbage_collect(self.f_3A)
        data_c = self.functions.category_view(self.wallet)
        tree = ttk.Treeview(self.f_3A, show='tree', selectmode='extended', height=len(data_c))
        tree.column('#0', width=310, minwidth=310)
        tree.images = {}
        for c1 in data_c:
            image_path = c1[2]
            if image_path not in tree.images:
                img = ImageTk.PhotoImage(Image.open(image_path).resize((33, 33)))
                tree.images[image_path] = img
            else:
                img = tree.images[image_path]
            parent_id = tree.insert('', 'end', text=f'{c1[0]}  ({c1[4]})  {self.exp_type[c1[1]]} {c1[3]}', image=img,
                                    tags=(c1[4],))
            data_d = self.functions.category_view2(self.wallet, c1[0])
            for c2 in data_d:
                date_obj = datetime.strptime(c2[4], '%Y-%m-%d')
                new_date = date_obj.strftime('%d-%m-%Y')
                if c2[5] != '':
                    text = f'{new_date}  {self.exp_type[c2[6]]}{c2[3]} \n# {c2[5]}'
                    if c2[5].startswith('UUID-'):
                        text = f'{c2[4]}  {self.exp_type[c2[6]]}{c2[3]}'
                    tree.insert(parent_id, 'end', text=text, values=c2 + (c1[2],))
                else:
                    text = f'{new_date}  {self.exp_type[c2[6]]}{c2[3]}'
                    tree.insert(parent_id, 'end', text=text, values=c2 + (c1[2],))

        tree.bind("<Double-1>", lambda e: self.selected_treeview(tree))
        tree.bind('<<TreeviewOpen>>', lambda e: self.on_tree_expand(tree))
        tree.bind('<<TreeviewClose>>', lambda e: self.on_tree_collapse(tree))
        tree.bind("<Delete>", lambda e: self.delete_selected_treeview(tree))
        tree.bind("<Control-a>", lambda e: [tree.selection_add(item) for item in tree.get_children(tree.focus())])
        tree.grid(row=0, column=0)

    # FUNCTION TO CREATE TREEVIEW ORGANIZED BY DATE---------------------------------------------------------------------
    def tree_date_frame(self, period='%Y-%m-%d'):

        self.static.garbage_collect(self.f_3A)
        data_c = self.functions.date_view(self.wallet, period)
        tree = ttk.Treeview(self.f_3A, show='tree', selectmode='extended', height=len(data_c))
        tree.column('#0', width=310, minwidth=310)
        tree.images = {}
        for c1 in data_c:
            sign = '+' if c1[2] >= 0 else ''
            if len(c1[0]) == 4:
                new_date = c1[0]
            elif len(c1[0]) == 7:
                new_date = datetime.strptime(c1[0], '%Y-%m').strftime('%m-%Y')
            else:
                new_date = datetime.strptime(c1[0], '%Y-%m-%d').strftime('%d-%m-%Y')

            parent_id = tree.insert('', 'end', text=f'{new_date} ({c1[1]})  {sign}{round(c1[2], 2)}', tags=(c1[1],))
            data_d = self.functions.date_view2(self.wallet, c1[0])
            for c2 in data_d:
                image_path = c2[8]
                if image_path not in tree.images:
                    img = ImageTk.PhotoImage(Image.open(image_path).resize((33, 33)))
                    tree.images[image_path] = img
                else:
                    img = tree.images[image_path]
                if c2[5] != '':
                    text = f'{self.exp_type[c2[6]]}{c2[3]}  {c2[2]}\n# {c2[5]}'
                    if c2[5].startswith('UUID-'):
                        text = f'{self.exp_type[c2[6]]}{c2[3]}  {c2[2]}'
                    tree.insert(parent_id, 'end', text=text, values=c2 + (c1[2],), image=img)
                else:
                    text = f'  {self.exp_type[c2[6]]}{c2[3]}  {c2[2]}   '
                    tree.insert(parent_id, 'end', text=text, values=c2 + (c1[2],), image=img)

        tree.bind("<Double-1>", lambda e: self.selected_treeview(tree))
        tree.bind('<<TreeviewOpen>>', lambda e: self.on_tree_expand(tree))
        tree.bind('<<TreeviewClose>>', lambda e: self.on_tree_collapse(tree))
        tree.bind("<Delete>", lambda e: self.delete_selected_treeview(tree))
        tree.bind("<Control-a>", lambda e: [tree.selection_add(item) for item in tree.get_children(tree.focus())])
        tree.grid(row=0, column=0)

    # FUNCTION TO CREATE A TREEVIEW OF THE WALLET MOVEMENT BY SEARCH----------------------------------------------------
    def tree_search_frame(self, search, *_):

        if search.strip() == '':
            self.tree_toggle()
        else:
            self.static.garbage_collect(self.f_3A)
            data_c = self.functions.search_view(self.wallet, search)
            tree = ttk.Treeview(self.f_3A, show='tree', selectmode='extended', height=min(len(data_c), 500))
            tree.column('#0', width=310, minwidth=280)
            tree.images = {}
            for c in data_c:
                image_path = c[8]
                if image_path not in tree.images:
                    img = ImageTk.PhotoImage(Image.open(image_path).resize((33, 33)))
                    tree.images[image_path] = img
                else:
                    img = tree.images[image_path]
                date_obj = datetime.strptime(c[4], '%Y-%m-%d')
                new_date = date_obj.strftime('%d-%m-%Y')

                if c[5] != '':
                    text = f'{c[2]} ({new_date}) {self.exp_type[c[6]]} {c[3]}\n {c[5]}'
                    if c[5].startswith('UUID-'):
                        text = f'{c[2]} ({c[4]}) {self.exp_type[c[6]]} {c[3]}'
                    tree.insert('', 'end', text=text, values=c, image=img)
                else:
                    text = f'{c[2]}  ({new_date})  {self.exp_type[c[6]]} {c[3]}'
                    tree.insert('', 'end', text=text, values=c, image=img)

            tree.bind("<Double-1>", lambda e: self.selected_treeview(tree, search=search))
            tree.bind("<Delete>", lambda e: self.delete_selected_treeview(tree, search=search))
            tree.bind("<Control-a>", lambda e: [tree.selection_add(item) for item in tree.get_children()])

            tree.grid(row=0, column=0)

    # FUNCTION TO OPEN THE SELECTED TREE ITEM IN THE MOVEMENT FRAME-----------------------------------------------------
    def selected_treeview(self, tree, search=None, *_):
        item = tree.selection()[0]
        item_type = tree.parent(item)
        if item_type != "" or search is not None:  # checks if there is a comment in the selected item
            if str(tree.item(item)['values'][5]).startswith('UUID-'):  # if is transfer calls transfer_frame2
                self.transfer_frame('UPDATE', tree.item(item)['values'][5])
            else:  # else calls add_remove_frame
                if search is not None:
                    self.movement_frame(self.exp_type[tree.item(item)["values"][6]], 'UPDATE', tree, search)
                else:
                    self.movement_frame(self.exp_type[tree.item(item)["values"][6]], 'UPDATE', tree)
                self.f_2A.lift()
        else:
            pass

    # FUNCTION TO DELETE THE SELECTED TREE ITEMS IN THE MOVEMENT TREE---------------------------------------------------
    def delete_selected_treeview(self, tree, search=None, *_):
        selected_items = tree.selection()
        items_without_children = [item for item in selected_items if not tree.get_children(item)]
        oids = [tree.item(item)['values'][7] for item in items_without_children]
        if not oids:
            messagebox.showinfo("Info", "No movements selected", parent=self.f_2A)
            return
        ask = messagebox.askyesno("Confirm", "Are you sure you want to delete these movements?", parent=self.f_2A)
        if ask:
            self.functions.delete_many_movements(oids)

            if search is not None:
                self.tree_search_frame(search)
            else:
                self.tree_toggle()
            self.balance_frame()
            self.selected_menu(0)

    # FUNCTION TO EXPAND THE TREEVIEW HEIGHT BASED ON THE NUMBER OF MOVEMENTS INSIDE A PARENT ITEM----------------------
    @staticmethod
    def on_tree_expand(tree, search=None, *_):
        if search is not None:
            tree.configure(height=tree.cget('height') - search)
        else:
            item_id = tree.focus()
            tags = tree.item(item_id, 'tags')
            if tree.cget('height') + int(tags[0]) > 50:
                tree.configure(height=50)
            else:
                tree.configure(height=tree.cget('height') + int(tags[0]))

    # FUNCTION TO COLLAPSE THE TREEVIEW HEIGHT BASED ON THE NUMBER OF MOVEMENTS INSIDE A PARENT ITEM--------------------
    def on_tree_collapse(self, tree, search=None, *_):
        if search is not None:
            tree.configure(height=tree.cget('height') - search)
        else:
            item_id = tree.focus()
            tags = tree.item(item_id, 'tags')
            if tree.cget('height') >= 50:
                self.tree_toggle()
            else:
                tree.configure(height=tree.cget('height') - int(tags[0]))

    # FUNCTION TO KEEP OPEN THE CURRENT TREEVIEW------------------------------------------------------------------------
    def tree_toggle(self):
        if self.c_toggle:
            self.tree_category_frame()
        else:
            self.tree_date_frame()

    # FUNCTION TO SWITCH BETWEEN THE DATE AND CATEGORY TREEVIEW---------------------------------------------------------
    def switch_tree(self, btn):
        self.l_range.configure(text='Day')
        if self.c_toggle:
            self.c_toggle = False
            self.tree_toggle()
            xy = 40
            img_light = 'icons/tools/sort_by_date_light.png'
            img_dark = 'icons/tools/sort_by_date_dark.png'
            img_date = ct.CTkImage(light_image=Image.open(img_light), dark_image=Image.open(img_dark), size=(xy, xy))
            btn.configure(image=img_date)
        else:
            self.c_toggle = True
            self.tree_toggle()
            xy = 40
            img_light = 'icons/tools/sort_by_category_light.png'
            img_dark = 'icons/tools/sort_by_category_dark.png'
            img_date = ct.CTkImage(light_image=Image.open(img_light), dark_image=Image.open(img_dark), size=(xy, xy))
            btn.configure(image=img_date)

    # FUNCTION TO SELECT THE ICON FOR THE MOVEMENT self.f_2A4-----------------------------------------------------------
    def movement_icon(self, icon, operation):

        def confirm_icon(img_path, category):
            new_img = ct.CTkImage(Image.open(img_path), size=(200, 200))
            icon.configure(image=new_img, text=category)
            self.f_2A.lift()

        self.static.garbage_collect(self.f_2B)
        self.f_2B.lift()
        args = {'cursor': 'hand2', 'fg_color': "transparent", 'hover_color': self.h1, 'width': 70, 'height': 70,
                'text_color': ('black', 'white'), 'corner_radius': 8, 'compound': 'top'}
        frame = ct.CTkScrollableFrame(self.f_2B, width=585, height=400, fg_color=self.h2, corner_radius=0)
        frame.grid(row=0, column=0, sticky='nsew', padx=(4, 0), pady=(4, 0))
        back_btn = ct.CTkLabel(self.f_2B, text='X', cursor='hand2', bg_color=self.h2, font=('Javanese Text', 15),
                               text_color='red')
        back_btn.bind('<Button-1>', lambda e: self.f_2A.lift())
        back_btn.grid(row=0, column=0, sticky='ne', padx=(0, 20))
        row = 0
        col = 0
        for icons in self.functions.get_icon(self.exp_type2[operation]):
            if icons[3] == 'icons/category/transfer-TO.png' or icons[3] == 'icons/category/transfer-FROM.png':
                continue
            else:
                font = self.static.calculate_font_size(icons[1])
                img = ct.CTkImage(Image.open(icons[3]), size=(65, 65))
                bt = ct.CTkButton(frame, image=img, **args, text=icons[1], font=('Arial', font, 'bold'))
                bt.configure(command=lambda i=icons[3], category=icons[1]: confirm_icon(i, category))
                bt.grid(row=row, column=col, sticky='nsew', padx=5, pady=10)

                if col == 5:
                    col = 0
                    row += 1
                else:
                    col += 1
        # self.balance_frame()

    # FUNCTION TO SELECT THE ICON FOR THE TRANSFER self.f_2A4-----------------------------------------------------------
    def transfer_icon(self, button1, button2, data):

        def confirm_icon(i, n):
            new_img = ct.CTkImage(Image.open(i), size=(130, 130))
            button1.configure(text=n, image=new_img)
            self.f_2A.lift()

        self.static.garbage_collect(self.f_2B)
        args = {'cursor': 'hand2', 'fg_color': "transparent", 'hover_color': self.h1, 'width': 60, 'height': 60,
                'compound': 'top', 'corner_radius': 10, 'text_color': ('black', 'white')}
        # frame = self.static.create_canvas(self.f_2B)
        back_btn = ct.CTkButton(self.f_2B, text='X', text_color='red', cursor='hand2', fg_color='transparent',
                                hover_color=self.h2, font=('Javanese Text', 15, 'bold'), width=10, height=10)
        back_btn.configure(command=lambda: self.f_2A.lift())
        back_btn.grid(row=0, column=10, sticky='ne', pady=20)

        row = 0
        col = 0
        wallets = self.functions.retrieve_wallets()
        for wallet in wallets:
            if wallet[1] == button2.cget('text'):
                continue
            elif wallet[3] != data[3]:
                continue
            font = self.static.calculate_font_size(wallet[1], base_size=14, min_size=8, decrease_rate=1)
            img = ct.CTkImage(Image.open(wallet[6]), size=(82, 82))
            btn = ct.CTkButton(self.f_2B, text=wallet[1], image=img, **args, font=('Arial', font))
            btn.configure(command=lambda i=wallet[6], n=wallet[1]: confirm_icon(i, n))
            btn.grid(row=row, column=col, columnspan=2, padx=4, pady=7)
            if col == 8:
                col = 0
                row += 1
            else:
                col += 2
        self.f_2B.lift()

    # FUNCTION TO SELECT ICON FOR CATEGORY AND WALLETS self.f_2A4-------------------------------------------------------
    def category_icon(self, path, widget, x, y):

        # FUNCTION TO CONFIRM AND VALIDATE THE DATA FOR THE NEW CATEGORY------------------------------------------------
        def confirm_icon(img_path, category):
            new_img = ct.CTkImage(Image.open(img_path), size=(x, y))
            widget.configure(image=new_img, text=category)
            self.f_2A.lift()

        self.static.garbage_collect(self.f_2B)
        self.f_2B.lift()
        args = {'cursor': 'hand2', 'fg_color': "transparent", 'hover_color': self.h1, 'width': 70, 'height': 70,
                'corner_radius': 8}
        frame = ct.CTkScrollableFrame(self.f_2B, width=585, height=400, fg_color=self.h2, corner_radius=0)
        frame.grid(row=0, column=0, sticky='nsew', padx=(4, 0), pady=(4, 0))
        back_btn = ct.CTkLabel(self.f_2B, text='X', cursor='hand2', bg_color='transparent', font=('Javanese Text', 13),
                               text_color='red', height=1, width=1)
        back_btn.bind('<Button-1>', lambda e: self.f_2A.lift())
        back_btn.grid(row=0, column=0, sticky='ne', padx=(0, 20))

        row = 1
        col = 0
        for filename in os.listdir(f'icons/{path}'):
            if filename.endswith(".png"):
                if filename == 'transfer-TO.png' or filename == 'transfer-FROM.png':
                    continue
                else:
                    img = ct.CTkImage(Image.open(f'icons/{path}/{filename}'), size=(62, 62))
                    btn = ct.CTkButton(frame, text='', image=img, **args)
                    btn.configure(command=lambda i=f'icons/{path}/{filename}', n=filename: confirm_icon(i, n))
                    btn.grid(row=row, column=col, sticky='nsew', padx=7, pady=10)
                    if col == 5:
                        col = 0
                        row += 1
                    else:
                        col += 1

    def logout(self):
        ask = messagebox.askokcancel("Logout", "Are you sure you want to logout?")
        if ask:
            from Login import Login
            from Static import Static
            from Functions import Functions
            Functions.remember(self.username)
            Static.garbage_collect(self.f_main)
            self.f_main.grid_remove()
            Login(self.root)

    def switch_theme(self, button):
        if self.theme == 'Dark':
            self.theme = 'Light'
            ct.set_appearance_mode('light')
            # self.style_c.configure('Treeview', fieldbackground=self.h2[0], background=self.h2[0], foreground='black')
            # self.style_c.map("Treeview", background=[("selected", "#a0a0a0")])
        else:
            self.theme = 'Dark'
            ct.set_appearance_mode('dark')
            # self.style_c.configure('Treeview', fieldbackground=self.h2[1], background=self.h2[1], foreground='white')
            # self.style_c.map("Treeview", background=[("selected", "#4d4d4d")])

        image_path = {'Dark': 'icons/tools/theme_dark.png', 'Light': 'icons/tools/theme_light.png'}
        img = ct.CTkImage(Image.open(image_path[self.theme]), size=(40, 20))
        button.configure(image=img, hover_color=self.bg[self.theme])
        self.f_1.configure(bg=self.bg[self.theme])
        self.f_1A.configure(bg=self.bg[self.theme])
        self.f_main.configure(bg=self.bg[self.theme])
        self.style_c.configure('Treeview', fieldbackground=self.c2[self.theme], background=self.c2[self.theme],
                               foreground=self.fg[self.theme])
        self.style_c.map("Treeview", background=[("selected", self.c3[self.theme])])

        self.style_c.configure('CustomTreeview.Treeview', background=self.c2[self.theme],
                               fieldbackground=self.c2[self.theme], foreground=self.fg[self.theme])
        self.style_c.map('CustomTreeview.Treeview',
                         background=[("selected", self.c2[self.theme])], foreground=[("selected", self.fg[self.theme])])

        try:  # CHANGES THE COLOR FO THE DONUT CHART IF IT IS OPEN
            self.donut_list[0].set_facecolor(self.c2[self.theme])
            for wedge in self.donut_list[1]:
                wedge.set_edgecolor(self.c2[self.theme])
            for text in self.donut_list[2]:
                text.set_color(self.fg[self.theme])
            self.donut_list[3].draw()
        except IndexError:
            pass

        try:  # CHANGES THE COLOR FO THE BAR CHART IF IT IS OPEN
            self.bar_list[0].set_facecolor(self.c2[self.theme])
            ax = self.bar_list[1]
            ax.set_facecolor(self.c2[self.theme])
            for spine in ax.spines.values():
                spine.set_color(self.fg[self.theme])
            ax.tick_params(colors=self.fg[self.theme], which='both')
            ax.grid(True, color=self.fg[self.theme], linestyle='--', linewidth=0.5, axis='y')
            self.bar_list[-1].draw()
        except IndexError:
            pass


class CreateToolTip(object):

    def __init__(self, widget, text='widget info'):
        self.wait_time = 2000
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.schedule)
        self.widget.bind("<Leave>", self.hidetip)
        self.id = None
        self.tw = None

    def schedule(self, *_):
        self.unschedule()
        self.id = self.widget.after(self.wait_time, self.showtip)

    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def showtip(self, *_):
        self.unschedule()
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = Label(self.tw, text=self.text, background="lightyellow", relief="solid", borderwidth=1, wraplength=200)
        label.pack()

    def hidetip(self, *_):
        self.unschedule()
        if self.tw:
            self.tw.destroy()
            self.tw = None
