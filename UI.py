import tkinter as tk
import colour_scheme as c
import ctypes as ct
import sql_updated


def dark_title_bar(window):
    window.update()
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, 20, ct.byref(value),
                         4)


class UI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        sql_updated.initialize()
        self.signed_up = sql_updated.signed_in()

        def logged_in():
            if self.signed_up is False:
                self.switch_frame(Start)
            else:
                self.switch_frame(Authorization)

        logged_in()
        dark_title_bar(self)
        self.minsize(self.winfo_screenwidth()-300, self.winfo_screenheight()-200)
        self.maxsize(self.winfo_screenwidth()-300, self.winfo_screenheight()-200)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class Start(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(height=UI.winfo_screenheight(self), width=UI.winfo_screenwidth(self), bg=c.primary)
        TopBar().place(rely=0)
        tk.Label(text='''This is the sign up page.
Enter your username and password.''', fg=c.text, bg=c.secondary, width=40).place(rely=0.40, relx=0.395)
        username = tk.Entry(bg=c.secondary, fg=c.text, width=30)
        password = tk.Entry(bg=c.secondary, fg=c.text, width=30)
        username.place(relx=0.46, rely=0.48)
        password.place(relx=0.46, rely=0.52)
        tk.Label(text='Username:', bg=c.primary, fg=c.text, width=10).place(rely=0.48, relx=0.395)
        tk.Label(text='Password:', bg=c.primary, fg=c.text, width=10).place(rely=0.52, relx=0.395)

        def submit():
            u = username.get()
            p = password.get()
            sql_updated.sign_up(username=u, password=p)
            master.switch_frame(Authorization)

        submit = tk.Button(text='submit', command=submit)
        submit.place(rely=0.6, relx=0.5)


class Authorization(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(height=UI.winfo_screenheight(self), width=UI.winfo_screenwidth(self), bg=c.primary)
        TopBar().place(rely=0)
        username = tk.Entry(bg=c.secondary, fg=c.text, width=30)
        password = tk.Entry(bg=c.secondary, fg=c.text, width=30)
        username.place(relx=0.46, rely=0.48)
        password.place(relx=0.46, rely=0.52)
        tk.Label(text='Username:', bg=c.primary, fg=c.text, width=10).place(rely=0.48, relx=0.395)
        tk.Label(text='Password:', bg=c.primary, fg=c.text, width=10).place(rely=0.52, relx=0.395)
        label = tk.Label(text="This is the login page", fg=c.text, bg=c.secondary, width=40)
        label.place(rely=0.40, relx=0.395)

        def login():
            u = username.get()
            p = password.get()
            auth = sql_updated.login(username=u, password=p)
            if auth is True:
                master.switch_frame(Welcome)
            else:
                label.config(text="Authorization Failed. Please try again.")

        login = tk.Button(text='Login', command=login)
        login.place(rely=0.6, relx=0.5)


class Welcome(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(height=UI.winfo_screenheight(self), width=UI.winfo_screenwidth(self), bg=c.primary)
        TopBar().place(rely=0)
        a = tk.Label(text='WELCOMEEEE', width=UI.winfo_screenwidth(self)-2000, fg=c.text, bg=c.secondary)
        a.place(rely=0.4)
        tk.Button(text="Inventory", command=lambda: master.switch_frame(InventoryEntry)).place(relx=0.5, rely=0.5)
        tk.Button(text="Products", command=lambda: master.switch_frame(ProductEntry)).place(relx=0.5, rely=0.6)


class TopBar(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.config(width=UI.winfo_screenwidth(self), height=55, bg=c.primary)
        label1 = tk.Label(text='BILLING & INVENTORY', bg=c.primary, fg=c.text, highlightthickness=0)
        label1.place(relx=0.5, rely=0.03, anchor='center')
        label2 = tk.Label(
            text=''' Made by: 
                    EKLAVYA RAMAN &
                     AALAYA CHANDOLA''', bg=c.primary, fg=c.text)
        label2.place_configure(relx=0.80, rely=0)


class InventoryEntry(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(width=UI.winfo_screenwidth(self), height=UI.winfo_screenheight(self), bg=c.primary)
        self.i = 0
        self.values = []
        self.create()
        self.sub()
        self.warning = tk.Label(text='Enter Product ID and Quantity to add to inventory.', bg=c.primary, fg=c.text,
                                width=70)
        self.warning.place(rely=0.15, relx=0.305)
        TopBar().place(y=0)
        self.add_widget()
        tk.Label(text="Add to Inventory Page", bg=c.primary, fg=c.text).place(rely=0.1, relx=0.448)
        label1 = tk.Label(text='Product ID', width=40, bg=c.primary, fg=c.text, font=c.font)
        label2 = tk.Label(text='Quantity', width=40, bg=c.primary, fg=c.text, font=c.font)
        label1.place(relx=0.23, rely=0.2)
        label2.place(relx=0.45, rely=0.2)

    def create(self):
        self.add_button = tk.Button(self, text='Add more?', command=self.add_widget, bg=c.secondary, fg=c.text)
        self.add_button.place(relx=0.80, rely=0.20)

    def sub(self):
        self.submit_button = tk.Button(self, text='Submit?', command=self.submit, bg=c.secondary, fg=c.text)
        self.submit_button.place(relx=0.15, rely=0.2)

    def add_widget(self):
        if self.i < 21:
            globals()['Variable{}'.format(str(self.i))] = tk.Entry(bg=c.secondary, fg=c.text, width=40)
            globals()['Variable{}'.format(str(self.i))].place(relx=0.28, y=((self.i + 1) * 23)+150)
            globals()['variable{}'.format(str(self.i))] = tk.Entry(bg=c.secondary, fg=c.text, width=40)
            globals()['variable{}'.format(str(self.i))].place(relx=0.5, y=((self.i + 1) * 23)+150)
            self.i += 1
        else:
            self.warning.config(text='Max. number of entries obtained. For more submit again.')

    def submit(self):
        for i in range(self.i):
            try:
                globals()['Var{}'.format(str(i))] = int(globals()['Variable{}'.format(str(i))].get())
                globals()['var{}'.format(str(i))] = int(globals()['variable{}'.format(str(i))].get())
                self.values.append([globals()['Var{}'.format(str(i))], globals()['var{}'.format(str(i))]])
            except ValueError:
                self.warning.config(text='Please check your input. Invalid data types entered.')
                self.values = []

        a = sql_updated.check_data_integrity(self.values)
        if a is True:
            sql_updated.update_inventory(self.values)
            for i in range(len(self.values)):
                globals()['Variable{}'.format(str(i))].destroy()
                globals()['variable{}'.format(str(i))].destroy()
                self.values = []
                self.i = 0
        else:
            self.warning.config(text="There was a problem with the input. One or more Product ID's do not exist.")
        print(self.values)


class ProductEntry(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(width=UI.winfo_screenwidth(self), height=UI.winfo_screenheight(self), bg=c.primary)
        self.i = 0
        self.values = []
        self.create()
        self.sub()
        self.warning = tk.Label(text='Enter Product ID and Quantity to add to inventory.', bg=c.primary, fg=c.text,
                                width=70)
        self.warning.place(rely=0.15, relx=0.305)
        TopBar().place(y=0)
        self.add_widget()
        tk.Label(text="Add to Inventory Page", bg=c.primary, fg=c.text).place(rely=0.1, relx=0.448)
        label1 = tk.Label(text='Product Name', width=20, bg=c.primary, fg=c.text, font=c.font2)
        label2 = tk.Label(text='Product Type', width=20, bg=c.primary, fg=c.text, font=c.font2)
        label3 = tk.Label(text='Product Cost', width=20, bg=c.primary, fg=c.text, font=c.font2)
        label4 = tk.Label(text='Selling Price', width=20, bg=c.primary, fg=c.text, font=c.font2)
        label1.place(relx=0.27, rely=0.2)
        label2.place(relx=0.38, rely=0.2)
        label3.place(relx=0.49, rely=0.2)
        label4.place(relx=0.60, rely=0.2)

    def create(self):
        self.add_button = tk.Button(self, text='Add more?', command=self.add_widget, bg=c.secondary, fg=c.text)
        self.add_button.place(relx=0.80, rely=0.20)

    def sub(self):
        self.submit_button = tk.Button(self, text='Submit?', command=self.submit, bg=c.secondary, fg=c.text)
        self.submit_button.place(relx=0.15, rely=0.2)

    def add_widget(self):
        if self.i < 21:
            globals()['ProductName{}'.format(str(self.i))] = tk.Entry(bg=c.secondary, fg=c.text, width=20)
            globals()['ProductName{}'.format(str(self.i))].place(relx=0.28, y=((self.i + 1) * 23) + 150)
            globals()['ProductType{}'.format(str(self.i))] = tk.Entry(bg=c.secondary, fg=c.text, width=20)
            globals()['ProductType{}'.format(str(self.i))].place(relx=0.39, y=((self.i + 1) * 23) + 150)
            globals()['ProductCost{}'.format(str(self.i))] = tk.Entry(bg=c.secondary, fg=c.text, width=20)
            globals()['ProductCost{}'.format(str(self.i))].place(relx=0.50, y=((self.i + 1) * 23) + 150)
            globals()['ProductSellingPrice{}'.format(str(self.i))] = tk.Entry(bg=c.secondary, fg=c.text, width=20)
            globals()['ProductSellingPrice{}'.format(str(self.i))].place(relx=0.61, y=((self.i + 1) * 23) + 150)
            self.i += 1
        else:
            self.warning.config(text='Max. number of entries obtained. For more submit again.')

    def submit(self):
        for i in range(self.i):
            try:
                globals()['Name{}'.format(str(i))] = str(globals()['ProductName{}'.format(str(i))].get())
                globals()['Type{}'.format(str(i))] = str(globals()['ProductType{}'.format(str(i))].get())
                globals()['Cost{}'.format(str(i))] = int(globals()['ProductCost{}'.format(str(i))].get())
                globals()['SellingPrice{}'.format(str(i))] = int(globals()['ProductSellingPrice{}'.format(str(i))].get()
                                                                 )
                self.values.append([globals()['Name{}'.format(str(i))], globals()['Type{}'.format(str(i))],
                                    globals()['Cost{}'.format(str(i))], globals()['SellingPrice{}'.format(str(i))]])
            except ValueError:
                self.warning.config(text='Please check your input. Invalid data types entered.')
                self.values = []

        a = sql_updated.check_products(self.values)
        if a is True:
            sql_updated.enter_products(self.values)
            for i in range(len(self.values)):
                globals()['ProductName{}'.format(str(i))].destroy()
                globals()['ProductType{}'.format(str(i))].destroy()
                globals()['ProductCost{}'.format(str(i))].destroy()
                globals()['ProductSellingPrice{}'.format(str(i))].destroy()
                self.values = []
                self.i = 0
                self.add_widget()
        else:
            self.warning.config(text="There was a problem with the input. One or more of the Products already exist.")


app = UI()
app.mainloop()
