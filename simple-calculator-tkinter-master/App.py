'''
    This script was written in python 3.x.
    In order to run this script, please make sure your python version is 3.x or above.

    How to run:
        python App.py

    or if it doesn't work use this one:
        python3 App.py

    Author: Udin <just.udin@yahoo.com>

'''

from math import sqrt
import tkinter as tk
from tkinter import *
import tkinter.messagebox
from tkinter.ttk import Frame, Label, Entry, Combobox, Style


class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def makeAsItIs(self, value):
        if (value == int(value)):
            value = int(value)
        return value

    def initUI(self):
        self.parent.title("Calculator by Udin")
        self.pack(fill=BOTH, expand=True)
        global value
        value = 0
        global num1
        num1 = StringVar()
        global num2
        num2 = StringVar()
        global res
        res = StringVar()
        # Justas
        global equation
        equation = StringVar()
        global history
        history = []
        global equationEntry
        global equalsButton
        global historyList
        global dec_spin

        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="Input Number 1 :", width=15)
        lbl1.pack(side=LEFT, padx=5, pady=5)

        entry1 = Entry(frame1, textvariable=num1)
        entry1.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="Input Number 2 :", width=15)
        lbl2.pack(side=LEFT, padx=5, pady=5)

        entry2 = Entry(frame2, textvariable=num2)
        entry2.pack(fill=X, padx=5, expand=True)

        # Justas
        frame_eq = Frame(self)
        frame_eq.pack(fill=X)

        lbl_eq = Label(frame_eq, text="Equation :", width=15)
        lbl_eq.pack(side=LEFT, padx=5, pady=5)

        # Tadas
        self._bg_main = "#eef2f7"
        self._bg_display = "#ffffff"
        self._btn_num = {"bg": "#89c4f4", "fg": "#153047", "activebackground": "#6eb0ef"}
        self._btn_fn = {"bg": "#b8e0c8", "fg": "#153047", "activebackground": "#9fd4b3"}
        self._btn_op = {"bg": "#ffd699", "fg": "#4a3200", "activebackground": "#ffc266"}
        self._btn_eq = {"bg": "#6eb5ff", "fg": "#ffffff", "activebackground": "#4da3ff"}
        self._keypad_buttons = []

        equationEntry = tk.Entry(
            frame_eq, textvariable=equation, bg=self._bg_display, relief=SUNKEN, borderwidth=2
        )
        equationEntry.pack(fill=X, padx=5, expand=True)

        # Tadas
        frame_keypad = tk.Frame(self, bg=self._bg_main)
        frame_keypad.pack(fill=X, padx=8, pady=4)
        for col in range(4):
            frame_keypad.columnconfigure(col, weight=1, uniform="key")

        def key_btn(text, cmd, row, col, style, colspan=1):
            b = tk.Button(
                frame_keypad,
                text=text,
                command=cmd,
                width=4,
                height=1,
                relief=RAISED,
                borderwidth=2,
                font=("Segoe UI", 11),
                takefocus=0,
                **style,
            )
            b.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)
            b._colored = True
            self._keypad_buttons.append(b)
            return b

        key_btn("%", self.mod, 0, 0, self._btn_fn)
        key_btn("|x|", self.insert_abs, 0, 1, self._btn_fn)
        key_btn("√()", self.insert_sqrt, 0, 2, self._btn_fn)
        key_btn("/", self.div, 0, 3, self._btn_op)

        keypad_rows = [
            (("7", "8", "9"), "*", self.mul),
            (("4", "5", "6"), "-", self.minus),
            (("1", "2", "3"), "+", self.plus),
        ]
        for r, (row_digits, op_text, op_cmd) in enumerate(keypad_rows, start=1):
            for c, digit in enumerate(row_digits):
                key_btn(
                    digit,
                    lambda d=digit: self.insert_to_equation(d),
                    r,
                    c,
                    self._btn_num,
                )
            key_btn(op_text, op_cmd, r, 3, self._btn_op)

        key_btn("(", lambda: self.insert_to_equation("("), 4, 0, self._btn_fn)
        key_btn("0", lambda: self.insert_to_equation("0"), 4, 1, self._btn_num)
        key_btn(")", lambda: self.insert_to_equation(")"), 4, 2, self._btn_fn)
        equalsButton = key_btn("=", self.calculate, 4, 3, self._btn_eq)

        key_btn(".", lambda: self.insert_to_equation("."), 5, 0, self._btn_num)
        key_btn("^", self.power, 5, 1, self._btn_fn, colspan=3)

        for row in range(6):
            frame_keypad.rowconfigure(row, weight=1, uniform="key")

        frame4 = Frame(self)
        frame4.pack(fill=X)

        lbl3 = Label(frame4, text="Result :", width=10)
        lbl3.pack(side=LEFT, padx=5, pady=5)

        result = tk.Entry(frame4, textvariable=res, bg=self._bg_display, relief=SUNKEN, borderwidth=2)
        result.pack(fill=X, padx=5, expand=True)

        # Tomas
        global result_format
        result_format = StringVar(value="Decimal")
        global decimal_places
        decimal_places = IntVar(value=4)

        frame_fmt = Frame(self)
        frame_fmt.pack(fill=X)

        lbl_fmt = Label(frame_fmt, text="Format :", width=15)
        lbl_fmt.pack(side=LEFT, padx=5, pady=3)

        fmt_combo = Combobox(
            frame_fmt,
            textvariable=result_format,
            values=["Decimal", "Scientific"],
            state="readonly",
            width=18,
        )
        fmt_combo.pack(side=LEFT, padx=5, pady=3)
        fmt_combo.bind("<<ComboboxSelected>>", lambda e: self._reformat_result())

        lbl_dec = Label(frame_fmt, text="  Digits:", width=13)
        lbl_dec.pack(side=LEFT, padx=(10, 2), pady=3)

        dec_spin = Spinbox(
            frame_fmt,
            from_=0,
            to=15,
            textvariable=decimal_places,
            width=4,
            command=self._on_digits_change,
        )
        dec_spin.pack(side=LEFT, padx=2, pady=3)
        dec_spin.bind("<ButtonRelease-1>", lambda e: self._on_digits_change())
        dec_spin.bind("<KeyRelease>", lambda e: self._on_digits_change())
        decimal_places.trace_add("write", lambda *args: self._on_digits_change())

        # Justas
        frame5 = Frame(self)
        frame5.pack(fill=X)

        lbl4 = Label(frame5, text="History :", width=15)
        lbl4.pack(side=LEFT, padx=5, pady=5)

        historyList = Listbox(frame5, height=5)
        historyList.pack(side=LEFT, fill=X, padx=5, pady=(5, 8), expand=True)
        historyList.bind('<<ListboxSelect>>', self.chooseHistory)

        # Tomas
        self._last_raw_value = None

        # Tadas
        self._font_family = "Segoe UI"
        self._font_size = 11
        self._theme_style = None
        self._apply_window_shell()
        self._build_menu()
        self._apply_smooth_style()
        self._decorate_original_widgets()
        self._install_shortcuts()

    # Justas
    def plus(self):
        self.addToEquation('+')

    def minus(self):
        self.addToEquation('-')

    def mul(self):
        self.addToEquation('*')

    def div(self):
        self.addToEquation('/')

    def insert_to_equation(self, text):
        place = equationEntry.index(INSERT)
        equationEntry.insert(place, text)
        equationEntry.icursor(place + len(text))
        equationEntry.focus_set()

    def addToEquation(self, sign):
        if sign in "+-*/%^" and not equation.get().strip():
            if num1.get().strip():
                equation.set(num1.get().strip())
            if num2.get().strip() and equation.get().strip():
                equation.set(equation.get() + sign + num2.get().strip())
                equationEntry.icursor(END)
                equationEntry.focus_set()
                return
        self.insert_to_equation(sign)

    def disableEqualsButton(self):
        equalsButton.config(state=DISABLED)

    def enableEqualsButton(self):
        equalsButton.config(state=NORMAL)

    def addToHistory(self, text, value):
        historyText = text + ' = ' + str(value)
        history.append(historyText)
        historyList.insert(END, historyText)

    def chooseHistory(self, event):
        choice = historyList.curselection()
        if len(choice) > 0:
            text = history[choice[0]].split(' = ')[0]
            equation.set(text)

    # Tomas
    def errorMsg(self, msg):
        if msg == 'sqrterror':
            tkinter.messagebox.showerror(
                'Root Error', 'Cannot take the square root of a negative number'
            )
        elif msg == 'error':
            tkinter.messagebox.showerror('Error!', 'Something went wrong! Maybe invalid entries')
        elif msg == 'divisionerror':
            tkinter.messagebox.showerror('Division Error', 'The value of input number 2 is 0. No dividing by 0')

    def mod(self):
        self.addToEquation('%')

    def insert_abs(self):
        place = equationEntry.index(INSERT)
        equationEntry.insert(place, '|()|')
        equationEntry.focus_set()

    def insert_sqrt(self):
        place = equationEntry.index(INSERT)
        equationEntry.insert(place, '√()')
        equationEntry.focus_set()

    def power(self):
        self.addToEquation('^')

    def preprocess(self, text):
        result = text.strip()
        result = self._replace_sqrt(result)
        result = result.replace('^', '**')
        result = self._replace_abs(result)
        return result

    def _replace_sqrt(self, text):
        out = []
        i = 0
        while i < len(text):
            if text[i] == '√':
                i += 1

                if i < len(text) and text[i] == '(':
                    depth = 0
                    start = i
                    j = i
                    while j < len(text):
                        if text[j] == '(':
                            depth += 1
                        elif text[j] == ')':
                            depth -= 1
                            if depth == 0:
                                break
                        j += 1
                    inner = text[start:j + 1]
                    j += 1

                    if j < len(text) and text[j] == '^':
                        j += 1
                        if j < len(text) and text[j] == '(':
                            depth2 = 0
                            k = j
                            while k < len(text):
                                if text[k] == '(':
                                    depth2 += 1
                                elif text[k] == ')':
                                    depth2 -= 1
                                    if depth2 == 0:
                                        break
                                k += 1
                            exp_part = text[j:k + 1]
                            j = k + 1
                        else:
                            k = j
                            while k < len(text) and (text[k].isdigit() or text[k] == '.'):
                                k += 1
                            exp_part = text[j:k]
                            j = k
                        out.append(f'(sqrt{inner})**{exp_part}')
                    else:
                        out.append(f'sqrt{inner}')
                    i = j
                else:
                    out.append('√')
            else:
                out.append(text[i])
                i += 1
        return ''.join(out)

    def _replace_abs(self, text):
        out = []
        i = 0
        while i < len(text):
            if text[i] == '|' and i + 1 < len(text) and text[i + 1] == '(':
                depth = 0
                j = i + 1
                while j < len(text):
                    if text[j] == '(':
                        depth += 1
                    elif text[j] == ')':
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                if j + 1 < len(text) and text[j + 1] == '|':
                    inner = text[i + 2:j]
                    out.append(f'abs({inner})')
                    i = j + 2
                else:
                    out.append(text[i])
                    i += 1
            else:
                out.append(text[i])
                i += 1
        return ''.join(out)

    def calculate(self):
        self.disableEqualsButton()
        try:
            raw = equation.get().strip()
            if not raw:
                raise ValueError
            processed = self.preprocess(raw)
            value = eval(processed, {"__builtins__": {}}, {"sqrt": sqrt, "abs": abs})
            self._last_raw_value = float(value)
            formatted = self._format_result_display(self._last_raw_value)
            res.set(formatted)
            self.addToHistory(raw, formatted)
        except ZeroDivisionError:
            self.errorMsg('divisionerror')
        except ValueError:
            self.errorMsg('sqrterror')
        except Exception:
            self.errorMsg('error')
        finally:
            self.parent.after(700, self.enableEqualsButton)

    def _format_result_display(self, value):
        if result_format.get() == "Scientific":
            return self.format_value(float(value))
        if value == int(value):
            return str(self.makeAsItIs(value))
        return self.format_value(value)

    def format_value(self, value):
        fmt = result_format.get()
        try:
            dec = int(decimal_places.get())
        except (ValueError, TclError):
            dec = 4
        if dec < 0:
            dec = 0
        elif dec > 15:
            dec = 15

        value = float(value)

        if fmt == "Scientific":
            return f"{value:.{dec}e}"
        if fmt == "Decimal":
            return f"{value:.{dec}f}"
        return f"{value:.{dec}f}".rstrip('0').rstrip('.')

    def _reformat_result(self):
        if self._last_raw_value is not None:
            res.set(self._format_result_display(self._last_raw_value))

    def _on_digits_change(self):
        try:
            val = int(decimal_places.get())
            if val < 0:
                decimal_places.set(0)
            elif val > 15:
                decimal_places.set(15)
        except ValueError:
            decimal_places.set(4)
        self._reformat_result()

    # Tadas
    def _apply_window_shell(self):
        self.parent.geometry("420x640")
        self.parent.resizable(True, True)
        self.parent.configure(bg=self._bg_main)

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
        style.configure("TFrame", background=self._bg_main)
        style.configure("TLabel", background=self._bg_main, foreground="#222222", font=font_spec)
        style.configure("TEntry", font=font_spec, padding=4)
        style.configure("TButton", font=font_spec)
        style.configure("TCombobox", font=font_spec)
        self.parent.configure(bg=self._bg_main)
        self._style_all_widgets(self)
        self._refresh_keypad_fonts()

    def _style_all_widgets(self, widget):
        wtype = widget.winfo_class()
        try:
            if wtype in ("Button", "TButton"):
                if getattr(widget, "_colored", False):
                    widget.configure(font=(self._font_family, self._font_size))
                    return
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
                if widget is equationEntry or widget is getattr(self, "_result_entry", None):
                    widget.configure(
                        font=(self._font_family, self._font_size),
                        bg=self._bg_display,
                        relief=SUNKEN,
                        borderwidth=2,
                    )
                    return
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
            elif wtype in ("Frame", "TFrame"):
                try:
                    widget.configure(bg=self._bg_main, relief=GROOVE, borderwidth=1)
                except Exception:
                    pass
            elif wtype == "Spinbox":
                widget.configure(
                    font=(self._font_family, self._font_size),
                    relief=SUNKEN,
                    borderwidth=1,
                )
                return
        except Exception:
            pass

        for child in widget.winfo_children():
            self._style_all_widgets(child)

    def _ensure_style(self):
        if self._theme_style is None:
            try:
                self._theme_style = Style(self.parent)
                try:
                    self._theme_style.theme_use("clam")
                except Exception:
                    pass
            except Exception:
                self._theme_style = None
        return self._theme_style

    def _decorate_original_widgets(self):
        self._style_all_widgets(self)
        try:
            equationEntry.focus_set()
        except Exception:
            pass
        self._lock_minimum_size()

    def _lock_minimum_size(self):
        try:
            self.parent.update_idletasks()
            self.parent.minsize(self.parent.winfo_reqwidth(), self.parent.winfo_reqheight())
        except Exception:
            self.parent.minsize(420, 640)

    def _install_shortcuts(self):
        self.parent.bind("<Return>", lambda event: self.calculate())
        self.parent.bind("<Escape>", lambda event: self.clear_all())
        self.parent.bind("<BackSpace>", lambda event: self.backspace())

    def clear_all(self):
        equation.set("")
        res.set("")
        self._last_raw_value = None
        historyList.delete(0, END)
        history.clear()
        try:
            equationEntry.focus_set()
        except Exception:
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
        except Exception:
            pass

    def set_font_family(self, family):
        self._font_family = family
        self._apply_smooth_style()
        self._refresh_spinbox()
        self._refresh_keypad_fonts()
        self._fit_window_to_content()

    def set_font_size(self, size):
        self._font_size = size
        self._apply_smooth_style()
        self._refresh_spinbox()
        self._refresh_keypad_fonts()
        self._fit_window_to_content()

    def _refresh_spinbox(self):
        try:
            dec_spin.configure(font=(self._font_family, self._font_size))
            dec_spin.update_idletasks()
        except Exception:
            pass

    def _refresh_keypad_fonts(self):
        for btn in self._keypad_buttons:
            try:
                btn.configure(font=(self._font_family, self._font_size))
            except Exception:
                pass

    def _fit_window_to_content(self):
        try:
            self.parent.update_idletasks()
            w = self.parent.winfo_reqwidth()
            h = self.parent.winfo_reqheight()
            self.parent.geometry(f"{w}x{h}")
            self.parent.minsize(w, h)
        except Exception:
            pass


def main():
    root = Tk()
    root.geometry("420x640")
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
