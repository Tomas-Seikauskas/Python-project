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
        historyList.pack(side=LEFT, fill=X, padx=5, expand=True)
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

    def sqr(self):
        self.addToEquation('²')#

    def root(self):
        self.addToEquation('√( )')#

    def addToEquation(self, sign):
        place = equationEntry.index(INSERT)
        equationEntry.insert(place, sign)
        equationEntry.icursor(place + 1)
        equationEntry.focus_set()

    def calculate(self):
        try:
            i=0#
            while i < len(text):#
              if text[i] == '√':#
                 text[i] =sqrt(text[i+2])#
                  
            
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

def main():
    root = Tk()
    root.geometry("420x240")
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
