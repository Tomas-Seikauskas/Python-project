'''
    This script was written in python 3.x.
    In order to run this script, please make sure your python version is 3.x or above.

    How to run:
        python App.py

    or if it doesn't work use this one:
        python3 App.py

    Author: Udin <just.udin@yahoo.com>
'''

from tkinter import *
import tkinter.messagebox
from tkinter.ttk import Frame, Label, Entry


class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Calculator by Udin")
        self.pack(fill=BOTH, expand=True)
        
        global equation
        equation = StringVar()
        global res
        res = StringVar()
        global history
        history = []
        global equationEntry
        global equalsButton
        global historyList

        # Lygties ivesties laukas
        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="Lygtis :", width=15)
        lbl1.pack(side=LEFT, padx=5, pady=5)

        equationEntry = Entry(frame1, textvariable=equation)
        equationEntry.pack(fill=X, padx=5, expand=True)

        # Mygtuku frame
        frame2 = Frame(self)
        frame2.pack(fill=X)

        btnplus = Button(frame2, text="+", width=8, command=self.plus)
        btnplus.pack(side=LEFT, anchor=N, padx=5, pady=5)

        btnminus = Button(frame2, text="-", width=8, command=self.minus)
        btnminus.pack(side=LEFT, anchor=N, padx=5, pady=5)

        btnmul = Button(frame2, text="*", width=8, command=self.mul)
        btnmul.pack(side=LEFT, anchor=N, padx=5, pady=5)

        btndiv = Button(frame2, text="/", width=8, command=self.div)
        btndiv.pack(side=LEFT, anchor=N, padx=5, pady=5)

        equalsButton = Button(frame2, text="=", width=8, command=self.calculate)
        equalsButton.pack(side=LEFT, anchor=N, padx=5, pady=5)

        # Rezultato laukas
        frame3 = Frame(self)
        frame3.pack(fill=X)

        lbl3 = Label(frame3, text="Rezultatas :", width=15)
        lbl3.pack(side=LEFT, padx=5, pady=5)

        result = Entry(frame3, textvariable=res)
        result.pack(fill=X, padx=5, expand=True)

        # Istorijos laukas
        frame4 = Frame(self)
        frame4.pack(fill=X)

        lbl4 = Label(frame4, text="Istorija :", width=15)
        lbl4.pack(side=LEFT, padx=5, pady=5)

        historyList = Listbox(frame4, height=6)
        historyList.pack(side=LEFT, fill=X, padx=5, pady=(5, 8), expand=True)
        historyList.bind('<<ListboxSelect>>', self.chooseHistory)

    def errorMsg(self, msg):
        if msg == 'error':
            tkinter.messagebox.showerror('Klaida!', 'Patikrinkite ivesta lygti')
        elif msg == 'divisionerror':
            tkinter.messagebox.showerror('Dalybos klaida', 'Negalima dalinti is 0')

    def plus(self):
        self.addToEquation('+')

    def minus(self):
        self.addToEquation('-')

    def mul(self):
        self.addToEquation('*')

    def div(self):
        self.addToEquation('/')

    def addToEquation(self, sign):
        place = equationEntry.index(INSERT)
        equationEntry.insert(place, sign)
        equationEntry.icursor(place + 1)
        equationEntry.focus_set()

    def calculate(self):
        try:
            text = equation.get()
            value = eval(text)
            res.set(self.makeAsItIs(value))
            self.addToHistory(text, self.makeAsItIs(value))
        except ZeroDivisionError:
            self.errorMsg('divisionerror')
        except:
            self.errorMsg('error')

    def addToHistory(self, text, value):
        historyText = text + ' = ' + str(value)
        history.append(historyText)
        historyList.insert(END, historyText)

    def chooseHistory(self, event):
        choice = historyList.curselection()
        if len(choice) > 0:
            text = history[choice[0]].split(' = ')[0]
            equation.set(text)

    def makeAsItIs(self, value):
        if value == int(value):
            value = int(value)
        return value


class EnhancedApp(App):
    def initUI(self):
        super().initUI()
        self._font_family = "Segoe UI"
        self._font_size = 11
        self._theme_style = None
        self._apply_window_shell()
        self._build_menu()
        self._apply_smooth_style()
        self._decorate_original_widgets()
        self._install_shortcuts()

    def _apply_window_shell(self):
        self.parent.geometry("470x310")
        self.parent.resizable(True, True)

    def _build_menu(self):
        menubar = Menu(self.parent, tearoff=0)
        font_menu = Menu(menubar, tearoff=0)

        families = ["Segoe UI", "Arial", "Calibri", "Tahoma", "Verdana", "Courier New"]
        for family in families:
            font_menu.add_command(label=family, command=lambda f=family: self.set_font_family(f))

        size_menu = Menu(menubar, tearoff=0)
        for size in [9, 10, 11, 12, 13, 14, 16, 18]:
            size_menu.add_command(label=str(size), command=lambda s=size: self.set_font_size(s))

        menubar.add_cascade(label="Font", menu=font_menu)
        menubar.add_cascade(label="Size", menu=size_menu)
        self.parent.config(menu=menubar)

    def _apply_smooth_style(self):
        style = self._ensure_style()
        font_spec = (self._font_family, self._font_size)
        self.parent.option_add("*Font", font_spec)
        self.parent.option_add("*Listbox.Font", font_spec)
        style.configure("TFrame", background="#ececec")
        style.configure("TLabel", background="#ececec", foreground="#222222", font=font_spec)
        style.configure("TEntry", font=font_spec, padding=4)
        style.configure("TLabelframe", background="#ececec", relief="groove", borderwidth=2)
        style.configure("TLabelframe.Label", background="#ececec", foreground="#222222", font=font_spec)
        style.configure("TButton", font=font_spec)
        self.parent.configure(bg="#ececec")
        self._style_original_frames()

    def _style_original_frames(self):
        for child in self.winfo_children():
            try:
                child.configure(relief=GROOVE, borderwidth=1, bg="#ececec")
            except:
                pass
            for sub in child.winfo_children():
                self._style_widget(sub)

    def _style_widget(self, widget):
        wtype = widget.winfo_class()
        try:
            if wtype in ("Button", "TButton"):
                widget.configure(
                    font=(self._font_family, self._font_size),
                    relief=RAISED,
                    borderwidth=3,
                    padx=8,
                    pady=3,
                    highlightthickness=0,
                    takefocus=0,
                )
            elif wtype in ("Entry", "TEntry"):
                widget.configure(
                    font=(self._font_family, self._font_size),
                    relief=SUNKEN,
                    borderwidth=3,
                    insertwidth=2,
                )
            elif wtype in ("Label", "TLabel"):
                widget.configure(font=(self._font_family, self._font_size))
            elif wtype == "Listbox":
                widget.configure(font=(self._font_family, self._font_size))
            elif wtype in ("Frame", "TFrame", "Labelframe", "TLabelframe"):
                widget.configure(bg="#ececec", relief=GROOVE, borderwidth=1)
        except:
            pass

        for child in widget.winfo_children():
            self._style_widget(child)

    def _ensure_style(self):
        if self._theme_style is None:
            try:
                from tkinter.ttk import Style
                self._theme_style = Style(self.parent)
                try:
                    self._theme_style.theme_use("clam")
                except:
                    pass
            except:
                self._theme_style = None
        return self._theme_style

    def _decorate_original_widgets(self):
        self._style_original_frames()
        try:
            equationEntry.focus_set()
        except:
            pass
        self._lock_minimum_size()

    def _lock_minimum_size(self):
        try:
            self.parent.update_idletasks()
            req_width = self.parent.winfo_reqwidth()
            req_height = self.parent.winfo_reqheight()
            self.parent.minsize(req_width, req_height)
        except:
            self.parent.minsize(470, 310)

    def _install_shortcuts(self):
        self.parent.bind("<Return>", lambda event: self.calculate())
        self.parent.bind("<Escape>", lambda event: self.clear_all())
        self.parent.bind("<BackSpace>", lambda event: self.backspace())

    def clear_all(self):
        equation.set("")
        res.set("")
        historyList.delete(0, END)
        history.clear()
        try:
            equationEntry.focus_set()
        except:
            pass

    def backspace(self):
        try:
            current = equation.get()
            place = equationEntry.index(INSERT)
            if place > 0:
                equation.set(current[:place - 1] + current[place:])
                equationEntry.icursor(place - 1)
            elif len(current) > 0:
                equation.set(current[:-1])
                equationEntry.icursor(len(current) - 1)
            equationEntry.focus_set()
        except:
            pass

    def set_font_family(self, family):
        self._font_family = family
        self._apply_smooth_style()
        self._fit_window_to_content()

    def set_font_size(self, size):
        self._font_size = size
        self._apply_smooth_style()
        self._fit_window_to_content()

    def _fit_window_to_content(self):
        try:
            self.parent.update_idletasks()
            req_width = self.parent.winfo_reqwidth()
            req_height = self.parent.winfo_reqheight()
            self.parent.geometry(f"{req_width}x{req_height}")
            self.parent.minsize(req_width, req_height)
        except:
            pass


App = EnhancedApp


def main():
    root = Tk()
    root.geometry("470x310")
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
