from datetime import datetime
import sqlite3
import os
import json
import requests
import pytz
# import datetime
API = "8d9740d7b76b17af76d8cec3"


class Functions:
    def __init__(self, username=None):
        self.username = username

    # FUNCTION TO RETRIEVE THE NAME AND SURNAME DATA FROM THE DATABASE--------------------------------------------------
    def name_surname(self):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = "SELECT * FROM account WHERE username = ?"
        cur.execute(query, (self.username,))
        data = cur.fetchone()
        conn.close()
        return data

    # FUNCTION TO RETRIEVE THE WALLETS DATA FROM THE DATABASE-----------------------------------------------------------
    def retrieve_wallets(self):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = "SELECT *, oid FROM wallet WHERE user = ?"
        cur.execute(query, (self.username,))
        data = cur.fetchall()
        conn.close()
        return data

    # FUNCTION TO RETRIEVE THE SELECTED WALLET DATA FROM THE DATABASE---------------------------------------------------
    def edit_wallet(self, wallet):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = "SELECT *, oid FROM wallet WHERE user = ? AND wallet_name = ?"
        cur.execute(query, (self.username, wallet))
        data = cur.fetchall()
        conn.close()
        return data[0]

    # FUNCTION TO CHECK IF A WALLET EXISTS IN THE DATABASE BEFORE INSERTING OR UPDATING---------------------------------
    def wallet_exist(self, name):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = "SELECT * FROM wallet WHERE user = ? AND wallet_name = ?"
        cur.execute(query, (self.username, name))
        data = cur.fetchone()
        conn.close()
        return data is not None

    # FUNCTION TO CREATE OR UPDATE THE WALLETS DATA IN THE DATABASE-----------------------------------------------------
    def create_update_wallet(self, action, name, start_sum, coin, start_date, icon, oid=None, og_name=None):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        if action == "INSERT":
            query = """INSERT INTO wallet (user, wallet_name, sum, coin, start_sum, start_date, icon) 
                SELECT ?, ?, ?, ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM wallet WHERE user = ? AND wallet_name = ?)"""
            cur.execute(query, (self.username, name, start_sum, coin, start_sum, start_date, icon, self.username, name))
        elif action == "UPDATE":
            query2 = "UPDATE wallet SET wallet_name=?, coin=?, start_sum=?, start_date=?, icon=? WHERE oid=?"
            cur.execute(query2, (name, coin, start_sum, start_date, icon, oid))
            update_movements = "UPDATE movements SET wallet = ? WHERE user = ? AND wallet = ?"
            cur.execute(update_movements, (name, self.username, og_name))

            updates = [{"query": "UPDATE categories SET category = ? WHERE category = ? AND user = ?",
                        "params": [(f"TO-{name}", f"TO-{og_name}", self.username),
                                   (f"FROM-{name}", f"FROM-{og_name}", self.username)]},

                       {"query": "UPDATE movements SET category = ? WHERE category = ? AND user = ?",
                        "params": [(f"TO-{name}", f"TO-{og_name}", self.username),
                                   (f"FROM-{name}", f"FROM-{og_name}", self.username)]}]
            for update in updates:
                for params in update["params"]:
                    cur.execute(update["query"], params)

        conn.commit()
        conn.close()

    # FUNCTION TO RETRIEVE THE TOTAL INCOME AND EXPENSE OF A WALLET-----------------------------------------------------
    def wallet_total(self, wallet):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = "SELECT SUM(sum) FROM movements WHERE user = ? AND wallet = ? AND type = 'income'"
        cur.execute(query, (self.username, wallet))
        income = cur.fetchone()[0]
        query = "SELECT SUM(sum) FROM movements WHERE user = ? AND wallet = ? AND type = 'expense'"
        cur.execute(query, (self.username, wallet))
        expense = cur.fetchone()[0]
        conn.close()
        return income, expense

    # FUNCTION TO CREATE THE TREEVIEW MOVEMENTS-------------------------------------------------------------------------
    def category_view(self, wallet):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = """SELECT c.category, c.type, c.icon, SUM(m.sum) AS total_sum, 
                   COUNT(m.category) AS category_usage_count
            FROM 
                categories c
            JOIN 
                movements m ON c.category = m.category AND c.user = m.user
            WHERE 
                m.user = ? AND m.wallet = ?
            GROUP BY 
                c.category, c.type, c.icon
            ORDER BY 
                CASE c.type
                    WHEN 'income' THEN 1
                    ELSE 2
                END,
                total_sum DESC
            """
        cur.execute(query, (self.username, wallet))
        data = cur.fetchall()
        conn.close()
        return data

    # FUNCTION TO CREATE THE TREEVIEW MOVEMENTS FOR THE CHILD TREEVIEW--------------------------------------------------
    def category_view2(self, wallet, category):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = "SELECT *, oid FROM movements WHERE user = ? AND wallet = ? AND category = ? ORDER BY date DESC"
        cur.execute(query, (self.username, wallet, category))
        data = cur.fetchall()
        conn.close()
        return data

    # FUNCTION TO CREATE THE DATE TREEVIEW MOVEMENTS--------------------------------------------------------------------
    def date_view(self, wallet, range='%Y-%m-%d'):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = f"""SELECT strftime('{range}', date) as period, COUNT(*) as count, 
        SUM(CASE WHEN type = 'income' THEN sum ELSE -sum END) as total_sum FROM movements WHERE user = ? AND wallet = ? 
        GROUP BY period ORDER BY period DESC"""
        cur.execute(query, (self.username, wallet))
        data = cur.fetchall()
        conn.close()
        return data

    # FUNCTION TO CREATE THE DATE TREEVIEW MOVEMENTS FOR THE CHILD TREEVIEW---------------------------------------------
    def date_view2(self, wallet, period):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()

        if len(period) == 10:
            date_comparison = "strftime('%Y-%m-%d', movements.date) = ?"
        elif len(period) == 7:
            date_comparison = "strftime('%Y-%m', movements.date) = ?"
        else:
            date_comparison = "strftime('%Y', movements.date) = ?"

        query = f"""SELECT movements.*, movements.oid, categories.icon FROM movements 
        JOIN categories ON movements.category = categories.category AND movements.user = categories.user 
        WHERE movements.user = ? AND movements.wallet = ? 
        AND {date_comparison}
        ORDER BY movements.date DESC"""

        cur.execute(query, (self.username, wallet, period))
        data = cur.fetchall()
        conn.close()
        return data

    # FUNCTION TO CREATE THE SEARCH TREEVIEW MOVEMENTS------------------------------------------------------------------
    def search_view(self, wallet, search):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = """SELECT m.*, m.oid, c.icon FROM movements m JOIN categories c ON m.category = c.category AND 
        m.user = c.user WHERE m.user = ? AND m.wallet = ? AND (m.category LIKE ? OR m.sum LIKE ? OR 
        (m.note LIKE ? AND m.note NOT LIKE 'UUID-%'))"""
        keyw = f'%{search}%'
        cur.execute(query, (self.username, wallet, keyw, keyw, keyw))
        data = cur.fetchall()
        conn.close()
        return data

    # FUNCTION TO INSERT AND UPDATE THE MOVEMENTS-----------------------------------------------------------------------
    def create_update_movement(self, action, wallet, oid=None, *data):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        if action == "INSERT":
            query = "INSERT INTO movements (user, wallet, category, sum, date, note, type) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cur.execute(query, (self.username, wallet, *data))
        elif action == "UPDATE":
            query = "UPDATE movements SET category = ?, sum = ?, date = ?, note = ?, type = ? WHERE oid = ?"
            cur.execute(query, (*data, oid))
        else:
            raise ValueError("Invalid action")
        conn.commit()
        conn.close()

    def autocomplete(self, text):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = "SELECT note FROM movements WHERE user = ? AND note LIKE ?"
        cur.execute(query, (self.username, f"%{text}%"))
        data = cur.fetchall()
        conn.close()
        return data

    # FUNCTION TO GET THE ICON WHEN INSERTING AND UPDATING A MOVEMENT---------------------------------------------------
    def get_icon(self, operation):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = "SELECT * FROM categories WHERE user = ? AND type = ?"
        cur.execute(query, (self.username, operation))
        data = cur.fetchall()
        conn.close()
        return data

    # FUNCTION TO SHOW ALL THE CREATED CATEGORIES-----------------------------------------------------------------------
    def get_categories(self):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = """
        SELECT c.*, c.oid, SUM(m.sum) AS total_sum 
        FROM categories c
        LEFT JOIN movements m ON c.category = m.category AND c.user = m.user
        WHERE c.user = ?
        GROUP BY c.oid
        ORDER BY c.type DESC, total_sum DESC
        """
        cur.execute(query, (self.username,))
        data = cur.fetchall()
        conn.close()
        return data

    # FUNCTION TO GET THE CATEGORIES FOR THE MERGE MENU-----------------------------------------------------------------
    def get_merge_categories(self, c1, c2):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = '''SELECT *, oid FROM categories WHERE user = ? AND type = ? AND category NOT LIKE 'TO-%' 
        AND category NOT LIKE 'FROM-%' AND category != ?'''
        cur.execute(query, (self.username, c2, c1))
        data = cur.fetchall()
        conn.close()
        return data

    def merge_categories(self, c1, c2):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = '''UPDATE movements SET category = ? WHERE user = ? AND category = ?'''
        cur.execute(query, (c1, self.username, c2))
        query2 = '''DELETE FROM categories WHERE user = ? AND category = ?'''
        cur.execute(query2, (self.username, c2))
        conn.commit()

    # FUNCTION TO SHOW ALL THE CREATED CATEGORIES WITH TOTAL SUM AND NUMBER OF MOVEMENTS ACROSS WALLETS-----------------
    def all_category_view(self):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = """SELECT c.category, c.type, c.icon, SUM(m.sum) AS total_sum, 
                           COUNT(m.category) AS category_usage_count
                    FROM 
                        categories c
                    JOIN 
                        movements m ON c.category = m.category AND c.user = m.user
                    WHERE 
                        m.user = ?
                    GROUP BY 
                        c.category, c.type, c.icon
                    ORDER BY 
                        CASE c.type
                            WHEN 'income' THEN 1
                            ELSE 2
                        END,
                        total_sum DESC
                    """
        cur.execute(query, (self.username, ))
        data = cur.fetchall()
        conn.close()
        return data

    # FUNCTION TO INSERT AND UPDATE THE CATEGORIES----------------------------------------------------------------------
    def create_update_category(self, category, type2, icon, action, oid=None):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        if action == "INSERT":
            query = """INSERT INTO categories (user, category, type, icon) SELECT ?, ?, ?, ? WHERE NOT EXISTS 
            (SELECT 1 FROM categories WHERE user = ? AND category = ?)"""
            cur.execute(query, (self.username, category, type2, icon, self.username, category))
        elif action == "UPDATE":
            query = "UPDATE categories SET user = ?, category = ?, type = ?, icon = ? WHERE oid = ?"
            cur.execute(query, (self.username, category, type2, icon, oid[4]))

            query = "UPDATE movements SET category = ? WHERE user = ? AND category = ?"
            cur.execute(query, (category, self.username, oid[1]))
        conn.commit()
        conn.close()

    # FUNCTION TO UPDATE THE BALANCE OF THE WALLETS---------------------------------------------------------------------
    def update_balance(self, wallet):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        balance_query = """ SELECT (SELECT start_sum FROM wallet WHERE user = ? AND wallet_name = ?), SUM(CASE WHEN 
        type = 'income' THEN sum ELSE 0 END) - SUM(CASE WHEN type = 'expense' THEN sum ELSE 0 END) FROM movements WHERE 
        user = ? AND wallet = ?"""
        cur.execute(balance_query, (self.username, wallet, self.username, wallet))
        start_sum, net_movement = cur.fetchone()
        total = start_sum + net_movement if net_movement is not None else start_sum

        update_query = "UPDATE wallet SET sum = ? WHERE user = ? AND wallet_name = ?"
        cur.execute(update_query, (total, self.username, wallet))
        conn.commit()

        data = """SELECT * FROM wallet WHERE user = ? AND wallet_name = ?"""
        cur.execute(data, (self.username, wallet))
        wallet_data = cur.fetchone()
        conn.close()
        return wallet_data

    # FUNCTION TO DELETE THE SELECTED WALLET DATA FROM THE DATABASE-----------------------------------------------------
    def delete_wallet(self, name, oid):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()

        query_uuid = "SELECT note FROM movements WHERE user = ? AND wallet = ? AND note LIKE 'UUID-%'"
        cur.execute(query_uuid, (self.username, name))
        uuid_movements = cur.fetchall()

        for uuid in uuid_movements:
            print(uuid)
            delete_uuid = "DELETE FROM movements WHERE note LIKE ?"
            cur.execute(delete_uuid, (uuid[0],))

        query_movements = "DELETE FROM movements WHERE user = ? AND wallet = ?"
        cur.execute(query_movements, (self.username, name))
        query = "DELETE FROM wallet WHERE oid = ?"
        cur.execute(query, (oid,))

        conn.commit()
        conn.close()
        self.clear_transfer_categories()

    # FUNCTION TO DELETE MOVEMENTS--------------------------------------------------------------------------------------
    def delete_movement(self, oid):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = "DELETE FROM movements WHERE oid = ? AND user = ?"
        cur.execute(query, (oid, self.username))
        conn.commit()
        conn.close()

    def delete_many_movements(self, oids):
        if not oids:
            return
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        placeholders = ','.join('?' for _ in oids)
        query = f"DELETE FROM movements WHERE oid IN ({placeholders}) AND user = ?"
        cur.execute(query, oids + [self.username])
        conn.commit()
        conn.close()

    # FUNCTION TO DELETE SELECTED CATEGORY------------------------------------------------------------------------------
    def delete_category(self, name, oid):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()

        query_movements = "DELETE FROM movements WHERE user = ? AND category = ?"
        cur.execute(query_movements, (self.username, name))

        query_category = "DELETE FROM categories WHERE oid = ?"
        cur.execute(query_category, (oid,))

        conn.commit()
        conn.close()

    # FUNCTION TO CHECK IF THE CATEGORY EXISTS--------------------------------------------------------------------------
    def category_exist(self, category):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = "SELECT * FROM categories WHERE user = ? AND category = ?"
        cur.execute(query, (self.username, category))
        data = cur.fetchone()
        conn.close()
        return data is not None

    def category_exists(self, conn, category_name, category_type):
        icon = "transfer-TO.png" if category_type == "expense" else "transfer-FROM.png"
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM categories WHERE user = ? AND category = ?", (self.username, category_name))
        exists = cur.fetchone()[0] > 0
        if not exists:
            cur.execute("INSERT INTO categories (user, category, type, icon) VALUES (?, ?, ?, ?)",
                        (self.username, category_name, category_type, f'icons/category/{icon}'))
            conn.commit()

        cur.close()

    def transfer(self, action, data, oid=None):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        if action == "INSERT":
            query = "INSERT INTO movements (user, wallet, category, sum, date, note, type) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cur.execute(query, data)
        elif action == "UPDATE":
            query = ("UPDATE movements SET user = ?, wallet = ?, category = ?, sum = ?, date = ?, note = ?, type = ? "
                     "WHERE oid = ?")
            cur.execute(query, (data[0], data[1], data[2], data[3], data[4], data[5], data[6], oid))

        category_name = data[2]
        category_type = "income" if category_name.startswith("FROM-") else "expense"
        self.category_exists(conn, category_name, category_type)
        conn.commit()
        conn.close()

    def get_transfer_data(self, oid):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = """SELECT m.*, m.oid, w.icon FROM movements m JOIN wallet w ON m.wallet = w.wallet_name AND 
        m.user = w.user WHERE m.note = ? AND m.user = ?"""
        cur.execute(query, (oid, self.username))
        data = cur.fetchall()
        conn.close()
        return data

    def delete_transfer(self, uuid):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query_movements = "DELETE FROM movements WHERE note = ?"
        cur.execute(query_movements, (uuid, ))
        conn.commit()
        conn.close()
        self.clear_transfer_categories()

    def bar_plot_day(self, wallet, offset):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        num = 10
        query = """
            SELECT strftime('%Y-%m-%d', date) AS exact_date, type, SUM(sum) as total
            FROM movements
            WHERE user = ? AND wallet = ? AND date IN (
                SELECT date
                FROM movements
                WHERE user = ? AND wallet = ?
                GROUP BY date
                ORDER BY date DESC
                LIMIT ?
                OFFSET ?
            )
            GROUP BY exact_date, type 
            ORDER BY exact_date ASC
        """
        cur.execute(query, (self.username, wallet, self.username, wallet, num, offset))
        data = cur.fetchall()
        conn.close()
        return data

    def bar_plot_month(self, wallet, offset):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        first = f"strftime('%Y-%m-01', 'now', '-{offset} month')"
        last = f"strftime('%Y-%m-%d', {first}, 'start of month', '+1 month', '-1 day')"
        query = f"""
            SELECT strftime('%Y-%m-%d', date) AS exact_date, type, SUM(sum) as total
            FROM movements
            WHERE user = ? AND wallet = ?
            AND date >= {first} AND date <= {last}
            GROUP BY exact_date, type
            ORDER BY exact_date
        """
        cur.execute(query, (self.username, wallet))
        data = cur.fetchall()
        if not data:
            first_day_of_month = cur.execute(f"SELECT {first}").fetchone()[0]
            data = [(first_day_of_month, 'expense', 0.0)]
        conn.close()
        return data

    def bar_plot_year(self, wallet, offset):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        cur.execute("SELECT strftime('%Y', 'now', ? || ' year')", (f"-{offset}",))
        target_year = cur.fetchone()[0]
        query = f"""
            SELECT strftime('%m', date) AS month, type, SUM(sum) as total
            FROM movements
            WHERE user = ? AND wallet = ? AND strftime('%Y', date) = ?
            GROUP BY month, type
            ORDER BY month, type
        """
        cur.execute(query, (self.username, wallet, target_year))
        data = cur.fetchall()
        result = []
        for month in range(1, 13):
            month_str = f"{int(month):02d}"
            expense = next((amount for m, t, amount in data if m == month_str and t == 'expense'), 0.0)
            income = next((amount for m, t, amount in data if m == month_str and t == 'income'), 0.0)
            result.extend([(f"{target_year}-{month_str}", 'expense', expense),
                           (f"{target_year}-{month_str}", 'income', income)])
        conn.close()
        return result

    @staticmethod
    def exchange_rate(coin1, coin2, summ, widget1, widget2=None):
        filename = f"coins/{coin1}.json"
        need_update = False
        data = None
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
            next_update_utc = datetime.fromtimestamp(data['time_next_update_unix'], tz=pytz.utc)
            now_utc = datetime.now(pytz.utc)
            if now_utc >= next_update_utc:
                need_update = True
        else:
            need_update = True

        if need_update:
            url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{coin1}"
            response = requests.get(url)
            data = response.json()
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(data, f)
        else:
            pass

        rate = data['conversion_rates'][coin2]
        calculated_result = rate * float(summ)
        if calculated_result.is_integer():
            result = "{:.0f}".format(calculated_result)
        else:
            result = "{:.2f}".format(calculated_result)
        if widget2:
            widget1.configure(text=result)
            widget2.configure(text=f'Rate:{rate}')
        else:
            widget1.configure(text=result)

    # FUNCTION TO CLEAR THE CATEGORIES THAT ARE NOT IN USE
    @staticmethod
    def clear_transfer_categories():
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        query = """DELETE FROM categories WHERE (category LIKE 'TO-%' OR category LIKE 'FROM-%') AND NOT EXISTS 
                (SELECT 1 FROM movements WHERE category = categories.category)"""
        cur.execute(query)
        conn.commit()
        conn.close()

    @staticmethod
    def remember(username, value=0):
        conn = sqlite3.connect('Wallet.db')
        cur = conn.cursor()
        reset_query = "UPDATE account SET remember = 0"
        cur.execute(reset_query)
        if value == 1:
            update_query = "UPDATE account SET remember = ? WHERE username = ?"
            cur.execute(update_query, (1, username))

        conn.commit()
        conn.close()
