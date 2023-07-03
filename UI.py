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

        login = tk.Button(text='Login', command=login,)
        login.place(rely=0.6, relx=0.5)


class Welcome(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(height=UI.winfo_screenheight(self), width=UI.winfo_screenwidth(self), bg=c.primary)
        TopBar().place(rely=0)
        a = tk.Label(text='WELCOMEEEE', width=UI.winfo_screenwidth(self)-2000, fg=c.text, bg=c.secondary)
        a.place(rely=0.4)


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
        label2.place_configure(relx=0.85, rely=0)


app = UI()
app.mainloop()
