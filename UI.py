import tkinter as tk
from PIL import ImageTk, Image
import colour_scheme as c
import backend
type_options = ('Vegetable', 'Cleaning', 'Entertainment', 'Beverage', 'Pulses', 'Fruit', 'Dairy')


class UI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        backend.initialize()
        self.signed_up = backend.signed_in()
        self.title("Computer Science Project")
        photo = ImageTk.PhotoImage(Image.open('sql-icon.jpeg'))
        self.iconphoto(False, photo)

        def logged_in():
            if self.signed_up is False:
                self.switch_frame(Start)
            else:
                self.switch_frame(Authorization)

        logged_in()
        backend.dark_title_bar(self)
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
            backend.sign_up(username=u, password=p)
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
            auth = backend.login(username=u, password=p)
            if auth is True:
                master.switch_frame(Welcome)
            else:
                label.config(text="Authorization Failed. Please try again.")

        login = MenuButton(text='Login', command=login)
        login.place(rely=0.6, relx=0.47)


class MenuButton(tk.Button):
    def __init__(self, text, command):
        tk.Button.__init__(self)
        self.config(width=15, bg=c.secondary, fg=c.text)
        self.text = text
        self.command = command
        self['command'] = self.command
        self['text'] = self.text


class HomeButton(tk.Button):
    def __init__(self, command):
        tk.Button.__init__(self)
        self.command = command
        self['command'] = self.command
        self.config(bg=c.primary, fg=c.text, text="Return to home page", font=c.font)


class Welcome(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(height=UI.winfo_screenheight(self), width=UI.winfo_screenwidth(self), bg=c.primary)
        TopBar().place(rely=0)
        tk.Label(text='Inventory: ', fg=c.text, font=c.font, bg=c.primary).place(relx=0.1, y=115)
        tk.Label(text='Product Entry: ', fg=c.text, font=c.font, bg=c.primary).place(relx=0.1, y=225)
        tk.Label(text='Billing: ', fg=c.text, font=c.font, bg=c.primary).place(relx=0.1, y=285)
        MenuButton(text="Inventory Entry", command=lambda: master.switch_frame(InventoryEntry)).place(relx=0.1,
                                                                                                      y=145)
        MenuButton(text="View Inventory", command=lambda: master.switch_frame(Inventory)).place(relx=0.1, y=180)

        MenuButton(text="Product Entry", command=lambda: master.switch_frame(ProductEntry)).place(relx=0.1, y=255)
        MenuButton(text="Billing", command=lambda: master.switch_frame(Billing)).place(relx=0.1, y=315)


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
        self.values2 = backend.display_inventory()
        self.number = 0
        self.number2 = 21
        if len(self.values2) < 21:
            self.number2 = len(self.values2)
        else:
            self.number2 = 21
        self.create()
        self.sub()
        self.warning = tk.Label(text='Enter Product ID and Quantity to add to inventory.', bg=c.primary, fg=c.text,
                                width=70)
        self.warning.place(rely=0.15, relx=0.305)
        TopBar().place(y=0)
        HomeButton(command=lambda: master.switch_frame(Welcome)).place(relx=0.05, rely=0.05)
        self.add_widget()
        tk.Label(text="Add to Inventory Page", bg=c.primary, fg=c.text).place(rely=0.1, relx=0.448)
        label1 = tk.Label(text='Product ID', width=20, bg=c.primary, fg=c.text, font=c.font)
        label2 = tk.Label(text='Quantity', width=20, bg=c.primary, fg=c.text, font=c.font)
        label1.place(relx=0.165, rely=0.2)
        label2.place(relx=0.315, rely=0.2)
        self.display()
        self.search_b()

    def create(self):
        self.add_button = tk.Button(self, text='Add more?', command=self.add_widget, bg=c.secondary, fg=c.text)
        self.add_button.place(relx=0.50, rely=0.20)

    def sub(self):
        self.submit_button = tk.Button(self, text='Submit?', command=self.submit, bg=c.secondary, fg=c.text)
        self.submit_button.place(relx=0.12, rely=0.2)

    def display(self):
        for j in range(self.number, self.number2):
            globals()['Product_ID1{}'.format(j)] = DisplayField(width=5)
            globals()['Product_Name1{}'.format(j)] = DisplayField(width=30)
            globals()['Product_ID1{}'.format(j)].place(relx=0.615, y=((j + 1) * 24) + 150)
            globals()['Product_Name1{}'.format(j)].place(relx=0.656, y=((j + 1) * 24) + 150)
            globals()['Product_ID1{}'.format(j)].insert(0, str(self.values2[j][0]))
            globals()['Product_Name1{}'.format(j)].insert(0, str(self.values2[j][1]))
            globals()['Product_ID1{}'.format(j)].config(state='disabled')
            globals()['Product_Name1{}'.format(j)].config(state='disabled')

    def search_b(self):
        def search():
            val = backend.search(a.get())
            for j in range(self.number, self.number2):
                globals()['Product_ID1{}'.format(j)].destroy()
                globals()['Product_Name1{}'.format(j)].destroy()
            self.values2 = val
            if len(self.values2) < 21:
                self.number2 = len(self.values2)
            else:
                self.number2 = 21
            self.display()

        a = tk.Entry(bg='red', fg='white', width=15)
        a.place(relx=0.7, rely=0.2)
        b = tk.Button(bg='red', fg='white', text='Submit', command=search)
        b.place(relx=0.8, rely=0.2)

    def add_widget(self):
        if self.i < 21:
            globals()['Variable{}'.format(str(self.i))] = tk.Entry(bg=c.secondary, fg=c.text, width=20)
            globals()['Variable{}'.format(str(self.i))].place(relx=0.2, y=((self.i + 1) * 23)+150)
            globals()['variable{}'.format(str(self.i))] = tk.Entry(bg=c.secondary, fg=c.text, width=20)
            globals()['variable{}'.format(str(self.i))].place(relx=0.35, y=((self.i + 1) * 23)+150)
            self.i += 1
        else:
            self.warning.config(text='Max. number of entries obtained. For more submit again.')

    def submit(self):
        for i in range(self.i):
            try:
                globals()['Var{}'.format(str(i))] = int(globals()['Variable{}'.format(str(i))].get())
                globals()['var{}'.format(str(i))] = int(globals()['variable{}'.format(str(i))].get())
                self.values.append([globals()['var{}'.format(str(i))], globals()['Var{}'.format(str(i))]])
            except ValueError:
                self.warning.config(text='Please check your input. Invalid data types entered.')
                self.values = []

        a = backend.check_data_integrity(self.values)
        if a is True:
            backend.update_inventory(self.values)
            for i in range(len(self.values)):
                globals()['Variable{}'.format(str(i))].destroy()
                globals()['variable{}'.format(str(i))].destroy()
                self.values = []
                self.i = 0
            self.add_widget()
        else:
            self.warning.config(text="There was a problem with the input. One or more Product ID's do not exist.")


class ProductEntry(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(width=UI.winfo_screenwidth(self), height=UI.winfo_screenheight(self), bg=c.primary)
        self.i = 0
        self.values = []
        self.create()
        self.delete()
        self.sub()
        self.warning = tk.Label(text='Enter products to be added to product list.', bg=c.primary, fg=c.text,
                                width=70)
        self.warning.place(rely=0.15, relx=0.305)
        TopBar().place(y=0)
        HomeButton(command=lambda: master.switch_frame(Welcome)).place(relx=0.05, rely=0.05)
        self.add_widget()
        tk.Label(text="Add to Product List", bg=c.primary, fg=c.text).place(rely=0.1, relx=0.448)
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

    def delete(self):
        self.delete_button = tk.Button(self, text='Add less?', command=self.remove_widget, bg=c.secondary, fg=c.text)
        self.delete_button.place(relx=0.80, rely=0.25)

    def sub(self):
        self.submit_button = tk.Button(self, text='Submit?', command=self.submit, bg=c.secondary, fg=c.text)
        self.submit_button.place(relx=0.15, rely=0.2)

    def add_widget(self):
        if self.i < 17:
            globals()['ProductName{}'.format(str(self.i))] = tk.Entry(bg=c.secondary, fg=c.text, width=20)
            globals()['ProductName{}'.format(str(self.i))].place(relx=0.28, y=((self.i + 1) * 28) + 150)
            globals()['ProductTypeVar{}'.format(str(self.i))] = tk.StringVar()
            globals()['ProductTypeVar{}'.format(str(self.i))].set("Food")
            globals()['ProductType{}'.format(str(self.i))] = tk.OptionMenu(self.master,
                                                                           globals()['ProductTypeVar{}'.format(str(self.i))],
                                                                           *type_options)
            globals()['ProductType{}'.format(str(self.i))].config(width=12, height=0, bg=c.secondary, fg=c.text,
                                                                  font=c.font2)
            globals()['ProductType{}'.format(str(self.i))].place(relx=0.39, y=((self.i + 1) * 28) + 150)
            globals()['ProductCost{}'.format(str(self.i))] = tk.Entry(bg=c.secondary, fg=c.text, width=20)
            globals()['ProductCost{}'.format(str(self.i))].place(relx=0.50, y=((self.i + 1) * 28) + 150)
            globals()['ProductSellingPrice{}'.format(str(self.i))] = tk.Entry(bg=c.secondary, fg=c.text, width=20)
            globals()['ProductSellingPrice{}'.format(str(self.i))].place(relx=0.61, y=((self.i + 1) * 28) + 150)
            self.i += 1
        else:
            self.warning.config(text='Max. number of entries obtained. For more submit again.')

    def remove_widget(self):
        if self.i > 1:
            globals()['ProductName{}'.format(str(self.i-1))].destroy()
            globals()['ProductType{}'.format(str(self.i-1))].destroy()
            globals()['ProductCost{}'.format(str(self.i-1))].destroy()
            globals()['ProductSellingPrice{}'.format(str(self.i-1))].destroy()
            self.i -= 1
        else:
            pass

    def submit(self):
        for i in range(self.i):
            try:
                globals()['Name{}'.format(str(i))] = str(globals()['ProductName{}'.format(str(i))].get())
                globals()['Type{}'.format(str(i))] = str(globals()['ProductTypeVar{}'.format(str(i))].get())
                globals()['Cost{}'.format(str(i))] = int(globals()['ProductCost{}'.format(str(i))].get())
                globals()['SellingPrice{}'.format(str(i))] = int(globals()['ProductSellingPrice{}'.format(str(i))].get()
                                                                 )
                self.values.append([globals()['Name{}'.format(str(i))], globals()['Type{}'.format(str(i))],
                                    globals()['Cost{}'.format(str(i))], globals()['SellingPrice{}'.format(str(i))]])
            except ValueError:
                self.warning.config(text='Please check your input. Invalid data types entered.')
                self.values = []

        a = backend.check_products(self.values)
        if a is True:
            backend.enter_products(self.values)
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


class DisplayField(tk.Entry):
    def __init__(self, width):
        tk.Entry.__init__(self)
        self.width = width
        self['width'] = self.width
        self.config(font=c.font, disabledforeground=c.text, disabledbackground=c.secondary,
                    selectforeground='black', selectbackground='red', justify='center', highlightthickness=2,
                    highlightbackground=c.tertiary, highlightcolor=c.tertiary)


class Inventory(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(width=UI.winfo_screenwidth(self), height=UI.winfo_screenheight(self), bg=c.primary)
        self.values = backend.display_inventory()
        self.number = 0
        self.number2 = 21
        if len(self.values) < 21:
            self.number2 = len(self.values)
        else:
           self.number2 = 21
        TopBar().place(y=0)
        HomeButton(command=lambda: master.switch_frame(Welcome)).place(relx=0.05, rely=0.05)
        self.display()
        self.next_b()
        self.search_b()

    def display(self):
        self.values = backend.display_inventory()
        for j in range(self.number, self.number2):
            globals()['Product_ID{}'.format(j)] = DisplayField(width=5)
            globals()['Product_Name{}'.format(j)] = DisplayField(width=30)
            globals()['Quantity{}'.format(j)] = DisplayField(width=7)
            globals()['Product_ID{}'.format(j)].place(relx=0.315, y=((j + 1) * 24)+150)
            globals()['Product_Name{}'.format(j)].place(relx=0.356, y=((j + 1)*24)+150)
            globals()['Quantity{}'.format(j)].place(relx=0.603, y=((j + 1)*24)+150)
            globals()['Product_ID{}'.format(j)].insert(0, str(self.values[j][0]))
            globals()['Product_Name{}'.format(j)].insert(0, str(self.values[j][1]))
            globals()['Quantity{}'.format(j)].insert(0, str(self.values[j][2]))
            globals()['Product_ID{}'.format(j)].config(state='disabled')
            globals()['Product_Name{}'.format(j)].config(state='disabled')
            globals()['Quantity{}'.format(j)].config(state='disabled')

    def next_b(self):
        self.next_button = tk.Button(self, text='Next Page', command=self.next, bg=c.secondary, fg=c.text)
        self.next_button.place(relx=0.80, rely=0.25)

    def next(self):
        if len(self.values) > 21:
            for j in range(self.number, self.number2):
                globals()['Product_ID{}'.format(self.number)].destroy()
                globals()['Product_Name{}'.format(self.number)].destroy()
                globals()['Quantity{}'.format(self.number)].destroy()
            self.number = self.number2
            if len(self.values) > (self.number2 + 21):
                self.number2 += 21
            else:
                self.number2 = len(self.values)
        else:
            pass

    def search_b(self):
        def search():
            val = backend.search(a.get())
            for j in range(self.number, self.number2):
                globals()['Product_ID{}'.format(j)].destroy()
                globals()['Product_Name{}'.format(j)].destroy()
                globals()['Quantity{}'.format(j)].destroy()
            self.values = val
            if len(self.values) < 21:
                self.number2 = len(self.values)
            else:
                self.number2 = 21
            self.display()

        a = tk.Entry(bg='red', fg='white', width=15)
        a.place(relx=0.7, rely=0.2)
        b = tk.Button(bg='red', fg='white', text='Submit', command=search)
        b.place(relx=0.8, rely=0.2)


class Billing(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(width=UI.winfo_screenwidth(self), height=UI.winfo_screenheight(self), bg=c.primary)
        TopBar().place(y=0)
        self.values = backend.display_inventory()
        self.number = 0
        self.number2 = 21
        self.i = 0
        if len(self.values) < 21:
            self.number2 = len(self.values)
        else:
            self.number2 = 21
        self.warning = tk.Label(text='Enter Product ID for billing.', bg=c.primary, fg=c.text,
                                width=70)
        self.warning.place(rely=0.08, relx=0.305)
        self.display()
        self.search_b()
        self.customer_name = tk.Entry(bg=c.secondary, fg=c.text, width=25)
        self.lab1 = tk.Label(text="Customer Name: ", bg=c.primary, fg=c.text)
        self.discount = tk.Entry(bg=c.secondary, fg=c.text, width=10)
        self.lab2 = tk.Label(text="Discount: ", bg=c.primary, fg=c.text)
        self.customer_name.place(relx=0.1, y=115)
        self.lab1.place(relx=0.1, y=90)
        self.discount.place(relx=0.3, y=115)
        self.lab2.place(relx=0.3, y=90)
        self.prod_ID = tk.Label(text="Prod. ID: ", bg=c.primary, fg=c.text)
        self.quant = tk.Label(text="Quantity: ", bg=c.primary, fg=c.text)
        self.prod_Name = tk.Label(text="Prod. Name: ", bg=c.primary, fg=c.text)
        self.selling_price = tk.Label(text="Selling Price: ", bg=c.primary, fg=c.text)
        self.prod_ID.place(relx=0.1, y=145)
        self.quant.place(relx=0.2, y=145)
        self.prod_Name.place(relx=0.3, y=145)
        self.selling_price.place(relx=0.42, y=145)
        self.add_widget()
        self.create()
        self.confirm_b()
        self.submit_b()
        HomeButton(command=lambda: master.switch_frame(Welcome)).place(relx=0.05, rely=0.05)

    def display(self):
        for j in range(self.number, self.number2):
            globals()['Product_ID1{}'.format(j)] = DisplayField(width=5)
            globals()['Product_Name1{}'.format(j)] = DisplayField(width=30)
            globals()['Product_ID1{}'.format(j)].place(relx=0.615, y=((j + 1) * 24) + 150)
            globals()['Product_Name1{}'.format(j)].place(relx=0.656, y=((j + 1) * 24) + 150)
            globals()['Product_ID1{}'.format(j)].insert(0, str(self.values[j][0]))
            globals()['Product_Name1{}'.format(j)].insert(0, str(self.values[j][1]))
            globals()['Product_ID1{}'.format(j)].config(state='disabled')
            globals()['Product_Name1{}'.format(j)].config(state='disabled')

    def search_b(self):
        def search():
            val = backend.search(a.get())
            for j in range(self.number, self.number2):
                globals()['Product_ID1{}'.format(j)].destroy()
                globals()['Product_Name1{}'.format(j)].destroy()
            self.values = val
            if len(self.values) < 21:
                self.number2 = len(self.values)
            else:
                self.number2 = 21
            self.display()

        a = tk.Entry(bg='red', fg='white', width=15)
        a.place(relx=0.7, rely=0.2)
        b = tk.Button(bg='red', fg='white', text='Submit', command=search)
        b.place(relx=0.8, rely=0.2)

    def confirm_b(self):
        def confirm():
            s = 0
            for i in range(self.i):
                data = backend.fetch_data(globals()['ProductId{}'.format(i)].get())
                globals()['Product_Name{}'.format(i)].insert(0, str(data[0][0]))
                globals()['SellingPrice{}'.format(i)].insert(0, str(data[0][1]))
                globals()['Product_Name{}'.format(i)].config(state='disabled')
                globals()['SellingPrice{}'.format(i)].config(state='disabled')
                a = globals()['Quantity{}'.format(i)].get()
                s += int(a)*(int(data[0][1]))
            b = int(self.discount.get())
            if b == '' or b is None:
                b = 0
            payable = (s*1.18)*((100-b)/100)
            self.warning.config(text="Net Payable Amount: {}".format(payable))

        self.confirm_button = tk.Button(self, text="Confirm Bill?", command=confirm, bg=c.secondary, fg=c.text)
        self.confirm_button.place(relx=0.38, y=115)

    def create(self):
        self.add_button = tk.Button(self, text='Add more?', command=self.add_widget, bg=c.secondary, fg=c.text)
        self.add_button.place(relx=0.465, y=115)

    def add_widget(self):
        if self.i < 21:
            globals()['ProductId{}'.format(self.i)] = tk.Entry(bg=c.secondary, fg=c.text, width=15)
            globals()['Quantity{}'.format(self.i)] = tk.Entry(bg=c.secondary, fg=c.text, width=15)
            globals()['Product_Name{}'.format(self.i)] = tk.Entry(bg=c.secondary, fg=c.text,
                                                                  disabledbackground=c.secondary,
                                                                  disabledforeground=c.text, width=20)
            globals()['SellingPrice{}'.format(self.i)] = tk.Entry(bg=c.secondary, fg=c.text,
                                                                  disabledbackground=c.secondary,
                                                                  disabledforeground=c.text, width=20)
            globals()['ProductId{}'.format(self.i)].place(relx=0.1, y=((self.i + 1) * 23)+150)
            globals()['Quantity{}'.format(self.i)].place(relx=0.2, y=((self.i + 1) * 23)+150)
            globals()['Product_Name{}'.format(self.i)].place(relx=0.3, y=((self.i + 1) * 23)+150)
            globals()['SellingPrice{}'.format(self.i)].place(relx=0.42, y=((self.i + 1) * 23)+150)
            self.i += 1
        else:
            self.warning.config(text='Too many items added. Add more in second bill.')

    def submit_b(self):
        self.submit_button = tk.Button(fg=c.text, bg=c.secondary, command=self.submit, text="Create Bill?")
        self.submit_button.place(relx=0.54, y=115)

    def submit(self):
        customer_name = self.customer_name.get()
        discount = int(self.discount.get())
        data = []
        for i in range(self.i):
            prod_id = (globals()['ProductId{}'.format(i)].get())
            quant = int(globals()['Quantity{}'.format(i)].get())
            prod_name = globals()['Product_Name{}'.format(i)].get()
            selling_price = int(globals()['SellingPrice{}'.format(i)].get())
            data.append((prod_id, quant, prod_name, selling_price))
        backend.create_bill(data, customer_name, discount)
        backend.reduce_inventory(data)


app = UI()
app.mainloop()
