from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import pandas as pd
from main import bdd
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

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Ошибка")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Ок", command=popup.destroy)
    B1.pack()
    popup.mainloop()    
        
def mainWindow():

    def download():
        
        try:
            dr, det, mp = excel_to_list(e1.get(), e2.get(), e3.get())
        except FileNotFoundError:
            popupmsg("Неверно указан путь к одному из файлов")

        log = bdd.insert_in_tables(drons_table=dr,
						dron_map=mp,
						details_table=det)
        
        f = open("Ошибки.txt", 'w')
        for i in log:
            print(i, file = f)
        popupmsg('Загрузка завершена, список ошибок выгружен в файл "Ошибки.txt" ')
    window = Tk()
    WINDOWS.append((window, "win1"))
    window.title("АБП")
    window.resizable(False, False)
    window.geometry("800x300")
    Label(window, text = "Дроны", font=("Arial", 15, "bold")).place(x = 50, y = 50)
    Label(window, text = "Комплектующие", font=("Arial", 15, "bold")).place(x = 50, y = 100)
    Label(window, text = "Тех. карты", font=("Arial", 15, "bold")).place(x = 50, y = 150)
    s1 = StringVar('')
    s2 = StringVar('')
    s3 = StringVar('')
    e1 = Entry(window, width = 45, font=("Arial", 15), textvariable = s1)
    e2 = Entry(window, width = 45, font=("Arial", 15), textvariable = s2)
    e3 = Entry(window, width = 45, font=("Arial", 15), textvariable = s3)
    e1.place(x = 250, y = 50)
    e2.place(x = 250, y = 100)
    e3.place(x = 250, y = 150)
    
    Button(text = "...", height = 1, command = lambda: s1.set(fd.askopenfilename(filetypes=(("Таблица Excel", "*.xlsx"),)))).place(x = 750, y = 50)
    Button(text = "...", height = 1, command = lambda: s2.set(fd.askopenfilename(filetypes=(("Таблица Excel", "*.xlsx"),)))).place(x = 750, y = 100)
    Button(text = "...", height = 1, command = lambda: s3.set(fd.askopenfilename(filetypes=(("Таблица Excel", "*.xlsx"),)))).place(x = 750, y = 150)

    Button(text = "Загрузить", font=("Arial", 15), command = download).place(x = 50, y = 200)
    Button(text = "Закрыть", font=("Arial", 15), command = lambda: deletewindow("win1")).place(x = 170, y = 200)
    window.mainloop()
    


