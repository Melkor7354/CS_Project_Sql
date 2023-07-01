import tkinter as tk
import colour_scheme as c
import ctypes as ct
import sql


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
        self.sign_up = False

        def logged_in():
            if self.sign_up is False:
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
        TopBar().pack()
        tk.Label(text='This is the signup page. Enter the username and password for future use.', bg=c.primary, fg=c.text).pack()
        username = tk.Entry(bg=c.secondary, fg=c.text)
        password = tk.Entry(bg=c.secondary, fg=c.text)
        username.pack()
        password.pack()

        def submit():
            u = username.get()
            p = password.get()
            sql.sign_up(username=u, password=p)
            UI.sign_up = True
            master.switch_frame(Authorization)

        submit = tk.Button(text='submit', command=submit)
        submit.pack()


class Authorization(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(height=UI.winfo_screenheight(self), width=UI.winfo_screenwidth(self), bg=c.primary)
        TopBar().pack()
        username = tk.Entry(bg=c.secondary, fg=c.text)
        password = tk.Entry(bg=c.secondary, fg=c.text)
        username.pack()
        password.pack()

        def login():
            u = username.get()
            p = password.get()
            auth = sql.login(username=u, password=p)
            if auth is True:
                master.switch_frame(Welcome)

        login = tk.Button(text='Login', command=login)
        login.pack()


class Welcome(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        TopBar().pack()
        a = tk.Label(text='Nothing', width=UI.winfo_screenwidth(self), fg=c.text, bg=c.primary)
        a.pack()


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
