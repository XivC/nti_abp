try:
    from tkinter import *
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog as fd
except:
    from Tkinter import *
    import Tkinter as tk
    from Tkinter import ttk
    from Tkinter import filedialog as fd
import pandas as pd
from main import bdd
import datetime
from tkcalendar import *
import os
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

def get_current_ost(dateost):
            other = []
            otherp = []
            for i in dateost:
                if i[0] not in other:
                    other.append(i[0])
                    otherp.append([i[0], int(i[2])])
                else:
                    for j in otherp:
                        if j[0] == i[0]:
                            j[1] += int(i[2])
            return otherp

def get_current_ost_akb(dateost):
            other = []
            otherp = []
            for i in dateost:
                if i[0] not in other and i[1] != '':
                    other.append(i[0])
                    otherp.append([i[0], int(i[2])])
                else:
                    for j in otherp:
                        if j[0] == i[0]:
                            j[1] += int(i[2])
            return otherp
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
    s1 = StringVar(window, '')
    s2 = StringVar(window,'')
    s3 = StringVar(window,'')
    e1 = Entry(window, width = 45, font=("Arial", 15), textvariable = s1)
    e2 = Entry(window, width = 45, font=("Arial", 15), textvariable = s2)
    e3 = Entry(window, width = 45, font=("Arial", 15), textvariable = s3)
    e1.place(x = 250, y = 50)
    e2.place(x = 250, y = 100)
    e3.place(x = 250, y = 150)
    
    Button(window, text = "...", height = 1, command = lambda: s1.set(fd.askopenfilename(filetypes=(("Таблица Excel", "*.xlsx"),)))).place(x = 750, y = 50)
    Button(window, text = "...", height = 1, command = lambda: s2.set(fd.askopenfilename(filetypes=(("Таблица Excel", "*.xlsx"),)))).place(x = 750, y = 100)
    Button(window, text = "...", height = 1, command = lambda: s3.set(fd.askopenfilename(filetypes=(("Таблица Excel", "*.xlsx"),)))).place(x = 750, y = 150)

    Button(window, text = "Загрузить", font=("Arial", 15), command = download).place(x = 50, y = 200)
    Button(window, text = "Закрыть", font=("Arial", 15), command = lambda: deletewindow("win1")).place(x = 170, y = 200)
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
                serial = StringVar(reg_sfr)
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
            ndb.append((i[0], serial, str(i[1]),1))
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
            ddt = dat.split('.')[::-1]
            month = int(ddt[1])
            month = str(month//10) + str(month % 10)
            day = int(ddt[2])
            day = str(day//10) + str(day % 10)
            ndata = ddt[0] + "-" + month + "-" + day
            

            
            s = (i[0],i[1].get(),i[2],e.get(),number,ndata)
            rdb.append(s)
        bdd.write_receipt_in_bd(rdb)
        popupmsg("Загрузка прошла успешно")

        
        
        return True
    def regok():
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
            ddt = dat.split('.')[::-1]
            month = int(ddt[1])
            month = str(month//10) + str(month % 10)
            day = int(ddt[2])
            day = str(day//10) + str(day % 10)
            ndata = ddt[0] + "-" + month + "-" + day
            

            
            s = (i[0],i[1].get(),i[2],e.get(),number,ndata)
            rdb.append(s)
        bdd.write_receipt_in_bd(rdb)
        popupmsg("Загрузка прошла успешно")
        
        #deletewindow("winreg")
        window.destroy()
        
        
            
        
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

def baseWindow():
    window = Tk()
    WINDOWS.append((window, "winbase"))
    window.title("АБП")
    window.resizable(False, False)
    window.geometry("500x500")
    Button(window,  text = "Загрузка данных из excel", command = mainWindow, font=("Arial", 15, "bold")).place( x = 50, y = 100)
    Button(window,  text = "Поступление комплектующих", command = regWindow, font=("Arial", 15, "bold")).place( x = 50, y = 150)
    Button(window,  text = "Остатки комплектующих", command = ostWindow, font=("Arial", 15, "bold")).place( x = 50, y = 200)
    Button(window,  text = "Анализ остатков АКБ", command = analiticWindow, font=("Arial", 15, "bold")).place( x = 50, y = 250)
    Button(window,  text = "Заявки на поставку", command = zayWindow, font=("Arial", 15, "bold")).place( x = 50, y = 300)
    window.mainloop()

def ostWindow():
    currentost = []
    llist = []
    def updateost(first = False):
        currentost.clear()
        for i in llist:
            i.destroy()
        if first:
            a = Label(ost_sfr.viewPort, font=("Arial", 15, "bold"), text = "№п/п", width = 5, bg = "white")
            a.grid(row = 0,column = 1)
            b = Label(ost_sfr.viewPort, font=("Arial", 15, "bold"), text = "Комплектующее", width = 37, bg = "white")
            b.grid(row = 0,column = 2)
            c = Label(ost_sfr.viewPort, font=("Arial", 15, "bold"), text = "Остаток", width = 15,  bg = "white")
            c.grid(row = 0,column = 3)
            llist.append(a)
            llist.append(b)
            llist.append(c)
        else:
            a = Label(ost_sfr.viewPort, font=("Arial", 15, "bold"), text = "№п/п", width = 5, bg = "white")
            a.grid(row = 0,column = 1)
            b = Label(ost_sfr.viewPort, font=("Arial", 15, "bold"), text = "Комплектующее", width = 37, bg = "white")
            b.grid(row = 0,column = 2)
            c = Label(ost_sfr.viewPort, font=("Arial", 15, "bold"), text = "Остаток", width = 15,  bg = "white")
            c.grid(row = 0,column = 3)
            llist.append(a)
            llist.append(b)
            llist.append(c)
            date = cal.get_date()
            month = int(date.month)
            month = str(month//10) + str(month % 10)
            day= int(date.day)
            day = str(day//10) + str(day % 10)
            fdate = "{y}-{m}-{d}".format(
                y=date.year,
                m=month,
                d=day
            )
            dateost = bdd.give_all_less_date(fdate)
            
            
            otherp = get_current_ost(dateost)
        

            #currentost = otherp
            k = 1
            for i in otherp:
                currentost.append([str(k),str(i[0]),str(i[1])])
                k += 1

            #print(currentost)
            n = 1
            for i in currentost:
                l1 = Label(ost_sfr.viewPort, font=("Arial", 15, "bold"), text = str(i[0]), width = 5, bg = "white")
                l1.grid(row = n,column = 1)
                l2 = Label(ost_sfr.viewPort, font=("Arial", 15, "bold"), text = i[1], width = 37, bg = "white")
                l2.grid(row = n,column = 2)
                l3 = Label(ost_sfr.viewPort, font=("Arial", 15, "bold"), text = str(i[2]), width = 15,  bg = "white")
                l3.grid(row = n,column = 3)
                llist.append(l1)
                llist.append(l2)
                llist.append(l3)
                n += 1
    def print_to_printer():
        dir = print_to_excel()
        
 
        os.startfile(dir, "print")

    def print_to_excel():
        dir = fd.asksaveasfilename(defaultextension='*.xlsx', filetypes=(("Таблица Excel", "*.xlsx"),))
        if dir != '':
            print(currentost)
            
            df = pd.DataFrame(currentost,columns=['№п/п', 'Комплектующее', 'Остаток'])
            pd.set_option('display.width', 500)
            df.to_excel(dir,  engine='xlsxwriter', index = False)
            return dir
    def buttons2():
        bp.destroy()
        Button(window, text = "Печать", font=("Arial", 15), command = print_to_printer).place(x = 550, y = 400)
        Button(window, text = "Сохранить", font=("Arial", 15), command = print_to_excel).place(x = 650, y = 400)


    d = datetime.datetime.now()
    window = Tk()
    WINDOWS.append((window, "ostwin"))
    window.title("Остатки комплектующих")
    window.resizable(False, False)
    window.geometry("800x500")
    ost_fr = Frame(window, relief=RIDGE)
    ost_sfr = ScrollFrame(ost_fr, width=700, height= 300)
    ost_fr.pack(side="top", fill="both", expand=True)
    ost_sfr.place(x = 50, y = 80)
    Label(window, text = "Показывать остатки на: ",  font=("Arial", 15, "bold") ).place(x = 50, y = 50)
    dateS = StringVar(window)
    #dateEntry = Entry(window, width = 35,  font=("Arial", 15), state = DISABLED, textvariable = dateS)
    #dateEntry.place(x = 300, y= 50)
    #Button(window, text = "...").place(x =690, y = 50)
    cal = DateEntry(window, width=35, background='darkblue',
                    foreground='white', borderwidth=2, year=d.year, day = d.day, month = d.month, font=("Arial", 15))
    cal.place(x = 300, y = 50)
    
    Button(window, text = "Выполнить", font=("Arial", 15), command = updateost).place(x = 50, y = 400)
    Button(window, text = "Закрыть", font=("Arial", 15), command = lambda: deletewindow("ostwin")).place(x = 180, y = 400)
    bp = Button(window, text = "Печать", font=("Arial", 15), command = buttons2)
    bp.place(x = 600, y = 400)
    updateost(first = True)
    window.mainloop()



def tosq(date):
    month = int(date.month)
    month = str(month//10) + str(month % 10)
    day= int(date.day)
    day = str(day//10) + str(day % 10)
    return str(date.year) + "-"+ str(month) + "-" + str(day)
def zayWindow():

    def add_new_zay():
            drones = []
            d_list = list(bdd.give_drons())
            d_list2 = []
            for i in d_list:
                d_list2.append(i[1])
            d_list = d_list2
            def add_drone():
                ll = []
                def update_drones():
                    k = 1
                    for i in ll:
                        i.destroy()
                    for i in drones:
                        a = Label(d_sfr.viewPort, text = i[0], font=("Arial", 10))
                        a.grid(row = k, column = 1)
                        ll.append(a)
                        a = Label(d_sfr.viewPort, text = i[1], font=("Arial", 10))
                        ll.append(a)
                        a.grid(row = k, column = 2)
                        k += 1
                def add():
                    try:
                        int(ae.get())
                    except:
                        popupmsg("Проверьте правильность данных в заявке")
                        return
                    if int(ae.get()) <= 0 or date_form.get() == '':
                        popupmsg("Проверьте правильность данных в заявке")
                        return
                    drones.append((date_form.get(), int(ae.get())))
                    update_drones()



                add_window = Tk()
                add_window.geometry("300x150")
                add_window.resizable(False, False)
                Label(add_window, text =  "Дрон: ").grid(row = 0,column = 1)
                Label(add_window, text = "Кол-во: ").grid(row = 1,column = 1)
                
                date_form =  ttk.Combobox(add_window, state="readonly",
                                  values=d_list,  width=32)
                date_form.grid(row = 0, column = 2)
                ae = Entry(add_window)
                ae.grid(row = 1, column = 2)
                Button(add_window, text = "Добавить", command = add).grid(row = 2, column = 1)

                add_window.mainloop()

                
            def create():
                date = tosq(date_form.get_date())
                pokup = pok_form.get()
               
                bdd.create_new_request(date,  pokup,drones)
                update_zay_list()
                popupmsg("Заявка создана")
            d = datetime.datetime.now()
            add_room_window = Tk()
            WINDOWS.append(add_room_window)
            add_room_window.title("Добавить заявку")
            add_room_window.geometry("500x500")
            w = add_room_window.winfo_pointerx()
            h = add_room_window.winfo_pointery()
            w = w - 200  # смещение от середины
            h = h - 200
            #add_room_window.geometry('300x500+{}+{}'.format(w, h))
            add_room_window.maxsize(500, 500)
            add_room_window.minsize(500, 500)
           
            d_fr = Frame(add_room_window, relief=RIDGE)
            d_sfr = ScrollFrame(d_fr, width=350, height= 200)
            d_fr.pack(side="top", fill="both", expand=True)
            d_sfr.place(x = 10, y = 150)
            date_form = DateEntry(add_room_window, width=15, background='darkblue',
                    foreground='white', borderwidth=2, year=d.year, day = d.day, month = d.month) 
            Label(add_room_window, text="дата\nсоздания: ").place(x = 10, y = 50)
            date_form.place(x = 200, y = 50)

            pok_form = Entry(add_room_window, width=35)
            Label(add_room_window, text="Покупатель: ").place(x = 10, y = 100)
            pok_form.place(x = 200, y = 100)
            
            #drones_form = Text(add_room_window, width=35,height = 10)
            Button(add_room_window, text="Добавить дрона ", command = add_drone).place(x = 10, y = 120)
           

            Button(add_room_window, text="Сохранить",  width=30, command = create).place(x = 10, y = 400)
            Button(add_room_window, text="Отмена", command=lambda: add_room_window.destroy(), width=30).place(x = 10, y = 450)

            add_room_window.mainloop()

    llist = []
    btns = []
    ids = []
    def update_zay_list():
        for i in llist:
            i.destroy()
        for i in btns:
            i.destroy()
        rq = bdd.give_all_requests()

        a = Label(ost_sfr.viewPort, text= "№п.п", font=("Arial", 10, "bold"))
        a.grid(row = 0, column = 1)
        llist.append(a)
        a = Label(ost_sfr.viewPort, text= "№Дата создания", font=("Arial", 10, "bold"))
        a.grid(row = 0, column = 2)
        llist.append(a)
        a = Label(ost_sfr.viewPort, text= "№Дата изм. сост.", font=("Arial", 10, "bold"))
        a.grid(row = 0, column = 3)
        llist.append(a)
        a = Label(ost_sfr.viewPort, text= "Состояние", font=("Arial", 10, "bold"))
        a.grid(row = 0, column = 4)
        llist.append(a)
        a = Label(ost_sfr.viewPort, text= "Сумма заявки", font=("Arial", 10, "bold"))
        a.grid(row = 0, column = 5)
        llist.append(a)
        k = 1
        for i in rq:
            a = Label(ost_sfr.viewPort, text= str(i[0]), font=("Arial", 10))
            a.grid(row = k, column = 1)
            llist.append(a)
            a = Label(ost_sfr.viewPort, text= str(i[1]), font=("Arial", 10))
            a.grid(row = k, column = 2)
            llist.append(a)
            a = Label(ost_sfr.viewPort, text= str(i[2]), font=("Arial", 10))
            a.grid(row = k, column = 3)
            llist.append(a)
            a = Label(ost_sfr.viewPort, text= str(i[3]), font=("Arial", 10))
            a.grid(row = k, column = 4)
            llist.append(a)
            a = Label(ost_sfr.viewPort, text= str(i[4]), font=("Arial", 10))
            a.grid(row = k, column = 5)
            ids.append(i[0])
            btns.append(Button(ost_sfr.viewPort, text = "Изм.Статус " + str(i[0]), command = lambda x = i[0]: edit_zay(x)))
            btns[-1].grid(row = k, column = 6)
            llist.append(a)
            k += 1
        print(rq)
    
    def edit_zay(idd):
        print(idd)
        def save():
            print(idd)
            a = date_form.get()
            print(a)
            x = bdd.change_status_request(idd,a)
            print(x)
            if  x == True:
                update_zay_list()
            else:
                popupmsg("Не хватает комплектующих")
        add_room_window = Tk()
        add_room_window.title("Добавить заявку")
        add_room_window.geometry("500x100")
           
        lst = ["Создано", "Идёт сборка", "Готово к отгрузке", "Запрошено разрешение у ФСБ", "Анулирована", "Отгружена"]
        date_form =  ttk.Combobox(add_room_window, state="readonly",
                                  values=lst,  width=32)
        Label(add_room_window, text="Статус заявки: ").grid(row=2, column=1)
        date_form.grid(row=2, column=2)
        Button(add_room_window, text = "Сохранить", command = save).grid(row = 3,column = 1)
        add_room_window.mainloop()
    window = Tk()
    WINDOWS.append((window, "zaywin"))
    window.title("Заявки на продажу")
    window.resizable(False, False)
    window.geometry("800x500")
    ost_fr = Frame(window, relief=RIDGE)
    ost_sfr = ScrollFrame(ost_fr, width=750, height= 300)
    ost_fr.pack(side="top", fill="both", expand=True)
    ost_sfr.place(x = 50, y = 80)
    Button(window, text = "Создать заявку", command = add_new_zay).place(x = 50, y = 50)
    update_zay_list()
    #Button(window, "").place(x = 50, y = 50)


def analiticWindow():

    def sum_date_ost(akbs):
        s = 0
        for i in akbs:
            s += int(i[1])
        return s

    def update_graph():
        canvas.delete("all")
        
        #print("hi")
        d1 = cal1.get_date()
        d2 = cal2.get_date()
        #cs1.set("{}.{}.{}".format(d1.day,d1.month,d1.year))
        delta = d2-d1
        if delta.days < 0:
            return
        rng = delta.days + 1
        step = int(600/rng)
        yprev = sum_date_ost(get_current_ost_akb(bdd.give_all_less_date(tosq(d1))))
        k = 1
        for i in range(20,600,step):
            #print(yprev)
            ynew = sum_date_ost(get_current_ost_akb(bdd.give_all_less_date(tosq(d1+datetime.timedelta(days = k)))))
            canvas.create_line(i, 230-yprev, i+step, 230-ynew, fill = "green", width = 3)
            canvas.create_text(i+step, 240, text = tosq(d1+datetime.timedelta(days = k-1)), fill = "red" )
            canvas.create_text(10, 240-yprev, fill = "red",text = yprev )
            k += 1
            yprev = ynew




    def fakechange():
        update_graph()
        window.after(1000, fakechange)

    window = Tk()
    window.title("Анализ остатков АКБ")
    window.geometry("700x400")
    window.resizable(False, False)
    WINDOWS.append((window, "analwin"))
    ost_fr = Frame(window, relief=RIDGE, width = 660, height = 150, bg = "white")
    #ost_sfr = ScrollFrame(ost_fr, width=500, height= 300)
    #ost_fr.pack(side="top", fill="both", expand=True)
    #ost_sfr.place(x = 50, y = 80)
    ost_fr.place(x = 50, y = 80)
    
    d = datetime.datetime.now()
    Label(window, text = "Анализ остатков с: ",  font=("Arial", 15) ).place(x = 25, y = 25)
    cs1 = StringVar(window, name = "")
    cs2 = StringVar(window,name = "")
    cal1 = DateEntry(window, width=15, background='darkblue',
                    foreground='white', borderwidth=2, year=d.year, day = d.day, month = d.month, font=("Arial", 15) )
    cal2 = DateEntry(window, width=15, background='darkblue',
                    foreground='white', borderwidth=2, year=d.year, day = d.day, month = d.month, font=("Arial", 15))
    cal1.place(x = 240, y = 25)
    Label(window, text = "До: ",  font=("Arial", 15) ).place(x = 440, y = 25)
    cal2.place(x = 490, y = 25)
    window.after(1000, fakechange)
    
    
    canvas = Canvas(ost_fr, bg = "white", width = 660,height = 250)
    canvas.pack(fill = BOTH, expand=1)
    update_graph()
        
    window.mainloop()