from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import pandas as pd
from main import bdd
import datetime
WINDOWS = []
class ScrollFrame(tk.Frame):
    def __init__(self, parent, width=100, height=100):
        super().__init__(parent)  # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff", width=width - 20,
                                height=height)  # place canvas on self
        self.viewPort = tk.Frame(self.canvas,
                                 background="#ffffff")  # place a frame on the canvas, this frame will hold the child widgets
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)  # place a scrollbar on self
        self.canvas.configure(yscrollcommand=self.vsb.set)  # attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")  # pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)  # pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw",
                                                       # add view port frame to canvas
                                                       tags="self.viewPort")

        self.viewPort.bind("<Configure>",
                           self.onFrameConfigure)  # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>",
                         self.onCanvasConfigure)  # bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(
            None)  # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"))  # whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window,
                               width=canvas_width)  # whenever the size of the canvas changes alter the window region respectively.


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
    popup.wm_title("Оповещение")
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
        regWindow()
        f = open("Ошибки.txt", 'w')
        print(log)
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
    
def regWindow():
    ndb = []
    def parsereg():
        lst = bdd.give_all_details()
        print(lst)
        row = 0
        for i in lst:
            if i[2] == 'Аккумуляторные батареи':
                l = Label(reg_sfr.viewPort, text = i[1], font=("Arial", 12), width = 50, bg = "white" )
                l.grid(row = row, column = 1)
                serial = StringVar()
                Entry(reg_sfr.viewPort, textvariable = serial, width = 30).grid(row = row, column = 2)
                l2 = Label(reg_sfr.viewPort, text = '1', font=("Arial", 12), width = 10, bg = "white" )
                l2.grid(row = row, column = 3)
                ndb.append((i[1], serial, '1',0))
                row += 1
        other = []
        otherp = []
        for i in lst:
            if i[2] != 'Аккумуляторные батареи':
                if i[1] not in other:
                    other.append(i[1])
                    otherp.append([i[1],1])
                else:
                    for j in otherp:
                        if j[0] == i[1]:
                            j[1] += 1
        #print(otherp)
        
        for i in otherp:

            l = Label(reg_sfr.viewPort, text = i[0], font=("Arial", 12), width = 50, bg = "white" )
            l.grid(row = row, column = 1)
            serial = StringVar()
            #Entry(reg_sfr.viewPort, textvariable = serial, width = 50).grid(row = row, column = 2)
            l2 = Label(reg_sfr.viewPort, text = str(i[1]), font=("Arial", 12), width = 10, bg = "white" )
            l2.grid(row = row, column = 3)
            ndb.append((i[1], serial, str(i[1]),1))
            row += 1

    def reg():
        hst = "Поставка №{n} от {dat}. Ответственный: {ot}".format(n=number,dat=dat,ot=e.get())
        print(hst)
        open("История.txt",'a').write(hst)
       
        rdb = []
        for i in ndb:
            print(i[3], i[1].get())
        for i in ndb:
            if i[3] == 0 and i[1].get() == '':
                popupmsg("Все АКБ должны иметь серийный номер")
                return False
        for i in ndb:
            s = (i[0],i[1],i[2],e.get(),number,dat)
            rdb.append(s)
        print(rdb)

        
        
        return True
    def regok():
        if reg():
            deletewindow("winreg")
            exit()
        
    window = Tk()
    WINDOWS.append((window, "winreg"))
    number = open("ses", "r").read()
    f = open("ses", "w")
    f.write(str(int(number)+1))
    f.close()
    st = "00000" + number
    d = datetime.datetime.now()

    dat = str(d.day) + "."+str(d.month)+"."+str(d.year)
    window.title("Поступление комплектующих №{st} от {dat}".format(st=st,dat=dat))
    window.resizable(False, False)
    window.geometry("800x500")
    reg_fr = Frame(window, relief=RIDGE)
    reg_sfr = ScrollFrame(reg_fr, width=750, height= 300)
    reg_fr.pack(side="top", fill="both", expand=True)
    reg_sfr.place(x = 25, y = 130)

    Label(window, text = "Ответственный за приём: ", font=("Arial", 15, "bold")).place(x = 25, y = 50)   
    Label(window, text = "Комплектующее: ", font=("Arial", 15, "bold")).place(x = 170, y = 85)
    Label(window, text = "Серийный номер: ", font=("Arial", 15, "bold")).place(x = 480, y = 85)
    Label(window, text = "Кол-во: ", font=("Arial", 15)).place(x = 675, y = 85)
    e = Entry(window, width = 40, font=("Arial", 15))
    e.place(x = 300, y= 50)
    Button(window, text = "ОК", font=("Arial", 15), command = regok).place(x=25, y=450)
    Button(window, text = "Записать", font=("Arial", 15), command = reg).place(x=100, y=450)
    Button(window, text = "Закрыть", font=("Arial", 15), command = lambda: deletewindow("winreg")).place(x=225, y=450)
    parsereg()
    window.mainloop()

