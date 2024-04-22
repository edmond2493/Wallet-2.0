from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import bcrypt
import re
from Static import Static
import customtkinter as ct


class Signup:
    def __init__(self, master, frame1, frame2, role):

        self.root = master
        self.frame1 = frame1
        self.frame2 = frame2
        self.role = role
        self.font2 = ('Arial', 18, 'bold')
        hover = {'blue': ("gray85", "gray16"), 'dark-blue': ("gray81", "gray20")}

        self.f_signup = ct.CTkFrame(self.root, width=300, height=400)
        self.f_signup.grid(row=0, column=1)
        self.f_signup.grid_propagate(False)

        # NAME LABELFRAME AND ENTRY-------------------------------------------------------------------------------------
        self.e_name = ct.CTkEntry(self.f_signup, placeholder_text='Name', font=self.font2, width=200, height=40)
        self.e_name.grid(row=0, column=0, columnspan=2, padx=(40, 0), pady=20)

        # SURNAME LABELFRAME AND ENTRY----------------------------------------------------------------------------------
        self.e_surname = ct.CTkEntry(self.f_signup, placeholder_text='Surname', font=self.font2, width=200, height=40)
        self.e_surname.grid(row=1, column=0, columnspan=2, padx=(40, 0), pady=20)

        # USERNAME LABELFRAME AND ENTRY---------------------------------------------------------------------------------
        self.e_username = ct.CTkEntry(self.f_signup, placeholder_text='Username', font=self.font2, width=200, height=40)
        self.e_username.grid(row=2, column=0, columnspan=2, padx=(40, 0), pady=20)

        # PASSWORD LABELFRAME AND ENTRY--------------------------------------------------------------------------------
        self.e_password = ct.CTkEntry(self.f_signup, placeholder_text='Password', font=self.font2, width=200, height=40,
                                      show='*')
        self.e_password.grid(row=3, column=0, columnspan=2, padx=(40, 0), pady=20)

        # SHOW AND HIDE PASSWORD BUTTON AND IMAGES----------------------------------------------------------------------
        self.show_pass = ct.CTkImage(Image.open('icons/tools/pass_shown.png'), size=(20, 20))
        self.hide_pass = ct.CTkImage(Image.open('icons/tools/pass_hidden.png'), size=(20, 20))
        self.show_hide = ct.CTkButton(self.f_signup, text='', image=self.hide_pass, cursor='hand2', width=20, height=20,
                                      fg_color="transparent", hover_color=hover['blue'], command=self.password_view)
        self.show_hide.grid(row=3, column=2, sticky='w')

        # CONFIRM AND CANCEL BUTTONS WITH IMAGES FOR THE NEW SIGNUP-----------------------------------------------------

        self.bt_confirm = ct.CTkButton(self.f_signup, text='Confirm', cursor="hand2", width=100, corner_radius=30)
        self.bt_confirm.grid(row=4, column=0, padx=(40, 15), pady=10)

        self.bt_cancel = ct.CTkButton(self.f_signup, text='Cancel', cursor="hand2", command=self.cancel, width=100,
                                      corner_radius=30)
        self.bt_cancel.grid(row=4, column=1, pady=10)

        self.r_var = IntVar()
        self.remember = ct.CTkCheckBox(self.f_signup, text='Remember', variable=self.r_var, cursor='hand2',
                                       border_width=1, corner_radius=20, checkbox_width=12, checkbox_height=12)
        self.remember.grid(row=5, column=0, padx=(40, 0))
        self.bt_confirm.configure(command=lambda: Confirm(self.e_name.get(), self.e_surname.get(),
                                                          self.e_username.get(), self.e_password.get(),
                                                          self.role, self.r_var.get(), self.f_signup, self.frame1,
                                                          self.root))
        self.root.mainloop()

    def password_view(self):
        if self.e_password.cget('show') == '*':
            self.e_password.configure(show='')
            self.show_hide.configure(image=self.show_pass)
        else:
            self.e_password.configure(show='*')
            self.show_hide.configure(image=self.hide_pass)

    def cancel(self):
        Static.garbage_collect(self.f_signup)
        self.f_signup.grid_remove()
        self.frame2.grid(row=0, column=1)


class EditUser:
    def __init__(self, f_2a, edit, cancel, update):
        self.f_2A = f_2a
        Static.garbage_collect(self.f_2A)
        self.edit = edit
        print(edit)

        self.font = ('Helvetica', 22, 'italic')
        self.font2 = ('Arial', 18, 'bold')
        self.font3 = ('Arial', 23, 'bold')
        args = {'font': self.font, 'text_color': ('#333333', '#cccccc')}
        args2 = {'font': self.font2, 'width': 200, 'height': 40}
        args3 = {'font': self.font3, 'text_color': ('#333333', '#dddddd'), 'fg_color': ('#cccccc', '#4d4d4d'),
                 'hover_color': ('#dddddd', '#666666'), 'border_width': 2, 'border_color': ('#dddddd', '#666666'),
                 'cursor': "hand2", 'width': 150, 'height': 40, 'corner_radius': 20}
        hover = {'blue': ("gray85", "gray16"), 'dark-blue': ("gray81", "gray20")}

        self.l_name = ct.CTkLabel(self.f_2A, text='New Name', **args)
        self.l_name.grid(row=0, column=0, columnspan=5, rowspan=1, pady=(30, 0), padx=30, sticky='w')
        self.e_name = ct.CTkEntry(self.f_2A, placeholder_text='Name', **args2)
        self.e_name.grid(row=1, column=0, columnspan=6, rowspan=1, pady=10)
        self.e_name.insert(0, edit[2])

        # SURNAME LABELFRAME AND ENTRY----------------------------------------------------------------------------------
        self.l_surname = ct.CTkLabel(self.f_2A, text='New Surname', **args)
        self.l_surname.grid(row=0, column=5, columnspan=5, rowspan=1, pady=(30, 0), padx=(35, 0), sticky='w')
        self.e_surname = ct.CTkEntry(self.f_2A, placeholder_text='Surname', **args2)
        self.e_surname.grid(row=1, column=5, columnspan=5, rowspan=1, pady=10)
        self.e_surname.insert(0, edit[3])
        Frame(self.f_2A, height=2, width=500, bg='gray').grid(row=2, column=0, columnspan=10, rowspan=1, pady=30)
        # USERNAME LABELFRAME AND ENTRY---------------------------------------------------------------------------------
        self.l_username = ct.CTkLabel(self.f_2A, text='New Username', **args)
        self.l_username.grid(row=3, column=0, columnspan=5, rowspan=1, pady=(10, 0), padx=30, sticky='w')
        self.e_username = ct.CTkEntry(self.f_2A, placeholder_text='Username', **args2)
        self.e_username.grid(row=4, column=0, columnspan=6, rowspan=1, pady=10)
        self.e_username.insert(0, edit[0])

        # PASSWORD LABELFRAME AND ENTRY--------------------------------------------------------------------------------
        self.l_password = ct.CTkLabel(self.f_2A, text='New Password', **args)
        self.l_password.grid(row=3, column=5, columnspan=5, rowspan=1, pady=(10, 0), padx=(35, 0), sticky='w')
        self.e_password = ct.CTkEntry(self.f_2A, placeholder_text='New Password', **args2, show='*')
        self.e_password.grid(row=4, column=5, columnspan=5, rowspan=1, pady=10)

        # SHOW AND HIDE PASSWORD BUTTON AND IMAGES----------------------------------------------------------------------
        self.show_pass = ct.CTkImage(Image.open('icons/tools/pass_shown.png'), size=(20, 20))
        self.hide_pass = ct.CTkImage(Image.open('icons/tools/pass_hidden.png'), size=(20, 20))
        self.show_hide = ct.CTkButton(self.f_2A, text='', image=self.hide_pass, cursor='hand2', width=20, height=20,
                                      fg_color="transparent", hover_color=hover['blue'], command=self.password_view)
        self.show_hide.grid(row=4, column=9, rowspan=2, pady=10, padx=30, sticky='e')

        # CONFIRM AND CANCEL BUTTONS WITH IMAGES FOR THE NEW SIGNUP-----------------------------------------------------
        self.bt_confirm = ct.CTkButton(self.f_2A, text='Confirm', **args3)
        self.bt_confirm.grid(row=6, column=1, columnspan=6, rowspan=2, pady=20)

        self.bt_cancel = ct.CTkButton(self.f_2A, text='Cancel', **args3)
        self.bt_cancel.configure(command=cancel)
        self.bt_cancel.grid(row=6, column=4, columnspan=6, rowspan=2, pady=20)

        self.r_var = IntVar()
        self.r_var.set(edit[5])
        self.remember = ct.CTkCheckBox(self.f_2A, text='Remember', variable=self.r_var, cursor='hand2',
                                       border_width=2, corner_radius=20, checkbox_width=16, checkbox_height=16,
                                       font=('Arial', 17))
        self.remember.grid(row=8, column=2, columnspan=4, rowspan=2)
        self.bt_confirm.configure(command=lambda: Confirm(self.e_name.get(), self.e_surname.get(),
                                                          self.e_username.get(), self.e_password.get(), edit[4],
                                                          self.r_var.get(), self.f_2A, edit=[edit[0], cancel, update]))

    def password_view(self):
        if self.e_password.cget('show') == '*':
            self.e_password.configure(show='')
            self.show_hide.configure(image=self.show_pass)
        else:
            self.e_password.configure(show='*')
            self.show_hide.configure(image=self.hide_pass)


class Confirm:
    def __init__(self, name, surname, username, password, role, remember, frame1, frame2=None, root=None, edit=None):
        conn = sqlite3.connect("Wallet.db")
        cur = conn.cursor()

        # CHECK IF NAME AND SURNAME ARE NOT EMPTY-----------------------------------------------------------------------
        if not name or not surname:
            messagebox.showwarning("Warning", "Name and surname cannot be empty")
            return

        # CHECK USERNAME LENGTH-----------------------------------------------------------------------------------------
        if not (4 <= len(username) <= 30):
            messagebox.showwarning("Warning", "Username must be between 4 and 30 characters")
            return

        # CHECK PASSWORD REQUIREMENTS-----------------------------------------------------------------------------------
        if not (6 <= len(password) <= 20) or not re.search("[a-zA-Z]", password) or \
           not re.search("[A-Z]", password) or not re.search("[0-9]", password):
            messagebox.showwarning("Warning", "Password must be between 6 and 20 characters and include at least one "
                                              "letter, one capital letter, and a number")
            return

        # CHECK IF USERNAME ALREADY EXISTS------------------------------------------------------------------------------
        if edit is not None:
            print(edit[0])
            cur.execute("SELECT * FROM account WHERE username=? AND username!=?", (username, edit[0]))
        else:
            cur.execute("SELECT * FROM account WHERE username=?", (username,))

        if cur.fetchone():
            messagebox.showwarning("Warning", "Username already taken")
            return

        # HASH THE PASSWORD---------------------------------------------------------------------------------------------
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # INSERT OR UPDATE THE NEW USER---------------------------------------------------------------------------------
        try:
            if edit is not None:
                cur.execute(
                    "UPDATE account SET name=?, surname=?, username=?, password=?, role=?, remember=? WHERE username=?",
                    (name, surname, username, hashed_password.decode('utf-8'), role, remember, edit[0]))
                conn.commit()

                if callable(edit[1]):
                    edit[2]()
                    edit[1]()

            else:
                cur.execute("INSERT INTO account (name, surname, username, password, role, remember) "
                            "VALUES (?, ?, ?, ?, ?, ?)",
                            (name, surname, username, hashed_password.decode('utf-8'), role, remember))
                conn.commit()
                Static.garbage_collect(frame1)
                Static.garbage_collect(frame2)
                frame1.grid_remove()
                frame2.grid_remove()
                from User import User
                User('user', username, root)

        except Exception as e:
            messagebox.showwarning("Warning", f"Error: {e}")
        finally:
            conn.close()
