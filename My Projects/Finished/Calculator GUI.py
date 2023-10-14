"""
Created on Mon 12 Oct 10:16 2020
Finished on Mon 12 Oct 22:00 2020
@author: Cpt.Ender

Simple Calculator GUI using tkinter
                                  """
from tkinter import *

root = Tk()
root.title('Simple Calculator')

# label = Label(root)
# label.
entry = Entry(root, width=50, borderwidth=5)
entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
lstOfAcceptableCharacters = ['0', '1', '2', '3', '4', '5', '6',
                             '7', '8', '9', '-', '+', '/', '*']


def add2Screen(character):
    entry.insert(END, character)


def clearScreen():
    entry.delete(0, END)


def printResult():
    ans = entry.get()
    entry.delete(0, END)
    for char in ans:
        if char not in lstOfAcceptableCharacters:
            print('This is not an acceptable character: ' + char)
            return
    if len(ans) > 0:
        entry.insert(END, eval(ans))


button_1 = Button(root, text="1", padx=40, pady=20, command=lambda: add2Screen(1))
button_2 = Button(root, text="2", padx=40, pady=20, command=lambda: add2Screen(2))
button_3 = Button(root, text="3", padx=40, pady=20, command=lambda: add2Screen(3))
button_4 = Button(root, text="4", padx=40, pady=20, command=lambda: add2Screen(4))
button_5 = Button(root, text="5", padx=40, pady=20, command=lambda: add2Screen(5))
button_6 = Button(root, text="6", padx=40, pady=20, command=lambda: add2Screen(6))
button_7 = Button(root, text="7", padx=40, pady=20, command=lambda: add2Screen(7))
button_8 = Button(root, text="8", padx=40, pady=20, command=lambda: add2Screen(8))
button_9 = Button(root, text="9", padx=40, pady=20, command=lambda: add2Screen(9))
button_0 = Button(root, text="0", padx=40, pady=20, command=lambda: add2Screen(0))
button_add = Button(root, text="+", padx=40, pady=20, command=lambda: add2Screen('+'))
button_sub = Button(root, text="-", padx=40, pady=20, command=lambda: add2Screen('-'))
button_mul = Button(root, text="*", padx=40, pady=20, command=lambda: add2Screen('*'))
button_div = Button(root, text="/", padx=40, pady=20, command=lambda: add2Screen('/'))
button_clear = Button(root, text="C", padx=40, pady=20, command=clearScreen)
button_equals = Button(root, text="=", padx=40, pady=20, command=printResult)

button_7.grid(row=1, column=1)
button_8.grid(row=1, column=2)
button_9.grid(row=1, column=3)
button_add.grid(row=1, column=4)

button_4.grid(row=2, column=1)
button_5.grid(row=2, column=2)
button_6.grid(row=2, column=3)
button_sub.grid(row=2, column=4)

button_1.grid(row=3, column=1)
button_2.grid(row=3, column=2)
button_3.grid(row=3, column=3)
button_mul.grid(row=3, column=4)

button_clear.grid(row=4, column=1)
button_0.grid(row=4, column=2)
button_equals.grid(row=4, column=3)
button_div.grid(row=4, column=4)

root.mainloop()
