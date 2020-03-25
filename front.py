from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import pandas as pd
WINDOWS = []
def deletewindow(window):
    for i in WINDOWS:
        if i[1] == window:
            WINDOWS.remove(i)
            i[0].destroy()

    pass

def excel_to_list(dir1, dir2, dir3):
     drones = pd.read_excel(dir1).values.tolist()
     details = pd.read_excel(dir2).values.tolist()
     mapp = pd.read_excel(dir3).values.tolist()
     return drones,details,mapp
    
        
def mainWindow():

    def download():
        dr, det, mp = excel_to_list(e1.get(), e2.get(), e3.get())
        bd.insert_in_tables(drons_table=dr,
						dron_map=mp,
						details_table=det)
    window = Tk()
    WINDOWS.append((window, "win1"))
    window.title("АБП")
    window.resizable(False, False)
    window.geometry("800x300")
    Label(window, text = "Дроны", font=("Arial", 15, "bold")).place(x = 50, y = 50)
    Label(window, text = "Комплектующие", font=("Arial", 15, "bold")).place(x = 50, y = 100)
    Label(window, text = "Тех. карты", font=("Arial", 15, "bold")).place(x = 50, y = 150)
    e1 = Entry(window, width = 45, font=("Arial", 15))
    e2 = Entry(window, width = 45, font=("Arial", 15))
    e3 = Entry(window, width = 45, font=("Arial", 15))
    e1.place(x = 250, y = 50)
    e2.place(x = 250, y = 100)
    e3.place(x = 250, y = 150)
    Button(text = "...", height = 1, command = lambda: e1.insert(0,fd.askopenfilename(filetypes=(("Таблица Excel", "*.xlsx"),)))).place(x = 750, y = 50)
    Button(text = "...", height = 1, command = lambda: e1.insert(0,fd.askopenfilename(filetypes=(("Таблица Excel", "*.xlsx"),)))).place(x = 750, y = 100)
    Button(text = "...", height = 1, command = lambda: e1.insert(0,fd.askopenfilename(filetypes=(("Таблица Excel", "*.xlsx"),)))).place(x = 750, y = 150)

    Button(text = "Загрузить", font=("Arial", 15), command = download).place(x = 50, y = 200)
    Button(text = "Закрыть", font=("Arial", 15), command = lambda: deletewindow("win1")).place(x = 170, y = 200)
    window.mainloop()
    


mainWindow()