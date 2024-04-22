from Functions import Functions
from Static import Static
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date, datetime
import matplotlib.pyplot as plt
import customtkinter as ct
import numpy as np

month_map = {
        '01': 'JAN', '02': 'FEB', '03': 'MAR', '04': 'APR',
        '05': 'MAY', '06': 'JUN', '07': 'JUL', '08': 'AUG',
        '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DEC'
    }


class Charts:
    def __init__(self, root=None, f_2A=None, username=None, wallet=None):

        self.theme = ct.get_appearance_mode()
        self.c1 = {"Light": "#dbdbdb", "Dark": "#2b2b2b"}
        self.c2 = {"Light": '#cfcfcf', "Dark": '#333333'}
        self.c3 = {"Light": '#4d4d4d', "Dark": '#a0a0a0'}
        self.h1 = ("#dbdbdb", "#2b2b2b")
        self.h2 = ('#cfcfcf', '#333333')
        self.bg = {"Light": '#ffffff', "Dark": '#404040'}
        self.fg = {"Light": '#000000', "Dark": '#ffffff'}
        self.root = root

        self.f_2A = f_2A
        self.wallet = wallet
        self.functions = Functions(username)
        self.static = Static()
        self.donut_list = []
        self.bar_list = []

    def donut_chart_frame(self, types='expense'):
        self.static.garbage_collect(self.f_2A)

        data = [item for item in self.functions.category_view(self.wallet) if item[1].lower() == types]
        data = sorted(data, key=lambda n: n[3], reverse=True)

        data = data[:13]
        categories = [item[0] for item in data]
        values = [item[3] for item in data]
        icon_paths = [item[2] for item in data]

        hex_colors = []
        for icon_path in icon_paths:
            img = Image.open(icon_path)
            rgb = img.quantize(colors=2, method=2)
            hex_color = '#%02x%02x%02x' % tuple(rgb.getpalette()[3:6])
            hex_colors.append(hex_color)

        fig = Figure(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor(self.c2[self.theme])

        ax = fig.add_subplot(111)
        ax.set_facecolor(self.c2[self.theme])
        fig.subplots_adjust(left=0.01, right=0.75, top=0.95, bottom=0.05)

        wedge_properties = {"width": 0.3, "edgecolor": self.c2[self.theme], 'linewidth': 1}
        wedges, texts, autotexts = ax.pie(values, startangle=90, colors=hex_colors, wedgeprops=wedge_properties,
                                          autopct='%1.1f%%')
        ax.axis('equal')

        for i, autotext in enumerate(autotexts):
            autotext.set_fontsize(9)
            theta = (wedges[i].theta1 + wedges[i].theta2) / 2
            theta_rad = np.deg2rad(theta)
            x = 1.1 * np.cos(theta_rad)
            y = 1.1 * np.sin(theta_rad)
            autotext.set_position((x, y))
            autotext.set_horizontalalignment('center')
            autotext.set_verticalalignment('center')
            autotext.set_color(self.fg[self.theme])

        chart = FigureCanvasTkAgg(fig, self.f_2A)
        chart.draw()

        center_x = 0
        center_y = 0
        data_b = self.functions.update_balance(self.wallet)
        income, expense = self.functions.wallet_total(self.wallet)
        income = 0 if income is None else income
        expense = 0 if expense is None else expense
        f_income = f"{income:,.2f} {data_b[3]}"
        f_expense = f"{expense:,.2f} {data_b[3]}"
        vertical_offset = 0.1

        # Add the first label at the center
        ax.text(center_x, center_y + vertical_offset, f_income, ha='center', va='center', fontsize=10, color='#4CAF50',
                weight='bold')

        # Add the second label below the first one
        ax.text(center_x, center_y - vertical_offset, f_expense, ha='center', va='center', fontsize=10, color='#F44336',
                weight='bold')

        ax.legend(wedges, categories, title="Categories", loc="center left", bbox_to_anchor=(0.97, 0.55),
                  facecolor='#F5F5F5', prop={'size': 9})
        chart.draw()
        chart.get_tk_widget().grid(row=0, column=0, padx=4, pady=4, sticky="nsew")
        args = {'cursor': 'hand2', 'fg_color': self.h2, "bg_color": self.h2, 'hover_color': self.h2, 'width': 20,
                'height': 20, 'font': ('Arial', 15, 'bold'), 'text_color': ('black', 'white'), 'corner_radius': 10}
        bt_expense = ct.CTkButton(self.f_2A, text="Expense", **args, command=lambda: self.donut_chart_frame('expense'))
        bt_income = ct.CTkButton(self.f_2A, text="Income", **args,  command=lambda: self.donut_chart_frame('income'))
        bt_expense.place(x=400, y=20)
        bt_income.place(x=500, y=20)
        if types == 'expense':
            bt_expense.configure(fg_color=self.h1, hover_color=self.h1)
        else:
            bt_income.configure(fg_color=self.h1, hover_color=self.h1)
        self.donut_list.clear()
        self.donut_list.append(fig)
        self.donut_list.append(wedges)
        self.donut_list.append(autotexts)
        self.donut_list.append(chart)
        self.f_2A.lift()

    def bar_plot_frame(self):
        self.static.garbage_collect(self.f_2A)
        args = {'cursor': 'hand2', 'fg_color': self.h2, "bg_color": self.h2, 'hover_color': self.h2, 'height': 20,
                'width': 1, 'font': ('Arial', 15, 'bold'), 'text_color': ('black', 'white'), 'corner_radius': 10}
        frame1 = ct.CTkFrame(self.f_2A, width=610, fg_color=self.h2)


        def create_bar_chart(dmy, x=None):
            self.static.garbage_collect(frame1)
            self.close_bar_chart()
            if hasattr(self, 'canvas') and hasattr(self.canvas, 'get_tk_widget'):
                self.canvas.get_tk_widget().destroy()
            if x == 'up':
                self.days += 1
            elif x == 'down' and self.days > 0:
                self.days -= 1
            else:
                self.days = 0

            if dmy == 'day':
                data = self.functions.bar_plot_day(self.wallet, self.days)
            elif dmy == 'month':
                data = self.functions.bar_plot_month(self.wallet, self.days)
            elif dmy == 'year':
                data = self.functions.bar_plot_year(self.wallet, self.days)
            else:
                raise ValueError("Invalid range specified")

            periods = []
            [periods.append(item[0]) for item in data if item[0] not in periods]
            expenses = [sum(item[2] for item in data if item[0] == p and item[1] == 'expense') for p in periods]
            incomes = [sum(item[2] for item in data if item[0] == p and item[1] == 'income') for p in periods]
            fig, ax = plt.subplots(figsize=(6.1, 3.7))

            if dmy == 'day':
                p_day.grid(row=0, column=0, pady=5)
                bt_day.configure(fg_color=self.h1, hover_color=self.h1)
                n_day.grid(row=0, column=2, pady=5)
                p_month.grid_forget()
                bt_month.configure(text=current_month, fg_color=self.h2, hover_color=self.h2)
                n_month.grid_forget()
                p_year.grid_forget()
                bt_year.configure(text=current_year, fg_color=self.h2, hover_color=self.h2)
                n_year.grid_forget()
                periods = [f"{d.split('-')[2]}-{d.split('-')[1]}" for d in periods]
            elif dmy == 'month':
                p_day.grid_forget()
                bt_day.configure(fg_color=self.h2, hover_color=self.h2)
                n_day.grid_forget()
                p_month.grid(row=0, column=3, pady=5)
                bt_month.configure(text=month_map[periods[0].split('-')[1]], fg_color=self.h1, hover_color=self.h1)
                n_month.grid(row=0, column=5, pady=5)
                p_year.grid_forget()
                bt_year.configure(text=periods[0].split('-')[0], fg_color=self.h2, hover_color=self.h2)
                n_year.grid_forget()
                periods = [f"{d.split('-')[2]}" for d in periods]
            elif dmy == 'year':
                p_day.grid_forget()
                bt_day.configure(fg_color=self.h2, hover_color=self.h2)
                n_day.grid_forget()
                p_month.grid_forget()
                bt_month.configure(text=current_month, fg_color=self.h2, hover_color=self.h2)
                n_month.grid_forget()
                p_year.grid(row=0, column=6, pady=5)
                bt_year.configure(text=periods[0].split('-')[0], fg_color=self.h1, hover_color=self.h1)
                n_year.grid(row=0, column=8, pady=5)
                periods = [f"{d.split('-')[1]}" for d in periods]

            width = 0.35
            x_positions = range(len(periods))
            ax.bar([pos - width / 2 for pos in x_positions], incomes, width=width, color='#7CB342', label='Income')
            ax.bar([pos + width / 2 for pos in x_positions], expenses, width=width, color='#E53935', label='Expense')

            fig.patch.set_facecolor(self.c2[self.theme])
            ax.set_facecolor(self.c2[self.theme])
            for spine in ax.spines.values():
                spine.set_color(self.fg[self.theme])
            ax.tick_params(colors=self.fg[self.theme], which='both')
            ax.grid(True, color=self.fg[self.theme], linestyle='--', linewidth=0.5, axis='y')

            ax.set_xticks(x_positions)
            ax.set_xticklabels(periods)

            fig.subplots_adjust(left=0.1, right=0.97, top=0.97, bottom=0.1)

            canvas = FigureCanvasTkAgg(fig, master=frame1)
            canvas.draw()
            widget = canvas.get_tk_widget()
            widget.grid(row=0, column=0, columnspan=3)

            self.bar_list.clear()
            self.bar_list.append(fig)
            self.bar_list.append(ax)
            self.bar_list.append(canvas)

        current_month = datetime.now().strftime('%b').upper()
        current_year = datetime.now().strftime('%Y')
        p_day = ct.CTkButton(self.f_2A, text='<', **args, command=lambda: create_bar_chart('day', 'up'))
        bt_day = ct.CTkButton(self.f_2A, text='Days', **args, command=lambda: create_bar_chart('day'))
        n_day = ct.CTkButton(self.f_2A, text='>', **args, command=lambda: create_bar_chart('day', 'down'))

        p_month = ct.CTkButton(self.f_2A, text='<', **args, command=lambda: create_bar_chart('month', 'up'))
        bt_month = ct.CTkButton(self.f_2A, text='', **args, command=lambda: create_bar_chart('month'))
        n_month = ct.CTkButton(self.f_2A, text='>', **args, command=lambda: create_bar_chart('month', 'down'))

        p_year = ct.CTkButton(self.f_2A, text='<', **args, command=lambda: create_bar_chart('year', 'up'))
        bt_year = ct.CTkButton(self.f_2A, text='', **args, command=lambda: create_bar_chart('year'))
        n_year = ct.CTkButton(self.f_2A, text='>', **args, command=lambda: create_bar_chart('year', 'down'))

        bt_day.grid(row=0, column=0, columnspan=3, pady=5)
        bt_month.grid(row=0, column=3, columnspan=3, pady=5)
        bt_year.grid(row=0, column=6, columnspan=3, pady=5)

        frame1.grid(row=1, column=0, columnspan=9, padx=5, pady=5)
        create_bar_chart('day')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.f_2A.lift()

    def close_bar_chart(self):
        plt.close('all')
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()  # Destroy the Tkinter canvas widget
            del self.canvas  # Delete the canvas object

    def on_closing(self):
        self.close_bar_chart()
        self.root.after(150, self.root.destroy)
