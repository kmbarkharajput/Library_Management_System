import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import messagebox



class library():
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="light gray")
        self.root.title("Library Management System")

        '''giving width to the gui'''
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        '''set label'''
        label = tk.Label(self.root, bg=self.clr(200,100,180), bd=3, fg="white", relief="groove",text="Library Management System", font=("Arial", 50, "bold"))
        label.pack(side="top", fill="x") #pack the label

        '''create input frame'''
        inFrame = tk.Frame(self.root, bg=self.clr(150,100,220), bd=4, relief="ridge")
        inFrame.place(width=self.width/3, height=self.height-180, x=80, y=100)

        '''create button inside of input frame'''
        regBtn = tk.Button(inFrame, command=self.regFun, text="Register Student", bg="light green", bd=2, font=("Arial", 15, "bold"), width=20)
        regBtn.grid(row=0, column=0, padx=180, pady=80)

        resBtn = tk.Button(inFrame, command=self.resBook, text="Reserve Book", bg="light green", bd=2, font=("Arial", 15, "bold"), width=20)
        resBtn.grid(row=1, column=0, padx=180, pady=80)

        retBtn = tk.Button(inFrame, command=self.retFun, text="Return Book", bg="light green", bd=2, font=("Arial", 15, "bold"), width=20)
        retBtn.grid(row=2, column=0, padx=180, pady=80)


        '''List Frame'''
        self.listFrame = tk.Frame(self.root, bd=4, relief="groove", bg=self.clr(120,220,100))
        self.listFrame.place(width=self.width/2, height=self.height-180, x=self.width/3+130, y=100)

        self.tabFun()
        self.showBk()

        
    def tabFun(self):
        tabFrame = tk.Frame(self.listFrame, bd=4, relief="sunken", bg=self.clr(200,100,110))
        tabFrame.place(width=self.width/2-60, height=self.height-280, x=30, y=70)  

        '''Scroll bar'''
        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")  

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")  

        '''create table'''
        self.table = ttk.Treeview(tabFrame, columns=("bId", "bname", "quant"), xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set)

        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)


        self.table.heading("bId", text="Book_ID")
        self.table.heading("bname", text="Book_Name")
        self.table.heading("quant", text="Quantity")
        self.table["show"] = "headings" # to remove empty column

        '''set the columns'''
        self.table.column("bId", width=170)
        self.table.column("bname", width=170)
        self.table.column("quant", width=170)

        self.table.pack(fill="both", expand=1)

    '''to register student'''
    def regFun(self):   
        self.regFrame = tk.Frame(self.root, bd=3, relief="ridge", bg=self.clr(150,150,150))
        self.regFrame.place(width=self.width/3, height=self.height-180, x=self.width/3+120, y=100)

        '''create labels inside registeration form'''
        rnLbl = tk.Label(self.regFrame, bg=self.clr(150,150,150), text="RollNo:", font=("Arial", 15, "bold"))
        rnLbl.grid(row=0, column=0, padx=20, pady=30)
        self.rnIn = tk.Entry(self.regFrame, bd=1, font=("Arial", 15, "bold"), width=20)
        self.rnIn.grid(row=0, column=1, padx=10, pady=30)

        nameLble = tk.Label(self.regFrame, bg=self.clr(150,150,150), text="Name:", font=("Arial", 15, "bold"))
        nameLble.grid(row=1, column=0, padx=20, pady=30)
        self.nameIn = tk.Entry(self.regFrame, bd=1, font=("Arial", 15, "bold"), width=20)
        self.nameIn.grid(row=1, column=1, padx=10, pady=30)
        
        subLbl = tk.Label(self.regFrame, bg=self.clr(150,150,150), text="Subject:", font=("Arial", 15, "bold"))
        subLbl.grid(row=2, column=0, padx=20, pady=30)
        self.subIn = tk.Entry(self.regFrame, bd=1, font=("Arial", 15, "bold"), width=20)
        self.subIn.grid(row=2, column=1, padx=10, pady=30)

        okBtn = tk.Button(self.regFrame, command=self.insertFun, text="OK", bd=2, bg="gray", width=20, font=("Arial", 20, "bold"))
        okBtn.grid(row=3, column=1, padx=30, pady=40)

    def insertFun(self):
        rn = int(self.rnIn.get())
        name = self.nameIn.get()
        subVal = self.subIn.get()
        totalBk=0
        
        
        '''To connect database'''
        if rn and name and subVal:
            try:
                con = pymysql.connect(host="localhost", user="root", passwd="barkha", database="record")
                cur = con.cursor()
                cur.execute("insert into reg(rollNo,sName,sub,total_book) values(%s,%s,%s,%s)",(rn,name,subVal,totalBk))
                con.commit()
                tk.messagebox.showinfo("Success", "Student Registered in Library Management System")
                self.desRegFrame()
                cur.close()
                con.close()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")  
                self.desRegFrame()  
        else:
            tk.messagebox.showerror("Error", "Please All Input Fields")  


    def desRegFrame(self):
        self.regFrame.destroy()    

    def showBk(self):
        try:
            con = pymysql.connect(host="localhost", user="root", passwd="barkha", database="record")
            cur = con.cursor()
            cur.execute("select * from library")
            data = cur.fetchall()

            self.tabFun()
            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('',tk.END,values=i)
            cur.close()
            con.close()    
        except Exception as ex:
            tk.messagebox.showerror("Error", f"Error: {ex}")       

    '''for reserved book'''
    def resBook(self):
        self.resFrame = tk.Frame(self.root, bg=self.clr(150,200,80), bd=4, relief="ridge")
        self.resFrame.place(width=self.width/3, height=self.height-180, x=self.width/3+120, y=100)    

        rnLbl = tk.Label(self.resFrame, bg=self.clr(150,200,80), text="RollNo:", font=("Arial", 15, "bold"))
        rnLbl.grid(row=0, column=0, padx=20, pady=30)
        self.rnIn = tk.Entry(self.resFrame, bd=1, font=("Arial", 15, "bold"), width=20)
        self.rnIn.grid(row=0, column=1, padx=10, pady=30)

        bkLbl = tk.Label(self.resFrame, bg=self.clr(150,200,80), text="Book_Id:", font=("Arial", 15, "bold"))
        bkLbl.grid(row=1, column=0, padx=20, pady=30)
        self.bkIn = tk.Entry(self.resFrame, bd=1, font=("Arial", 15, "bold"), width=20)
        self.bkIn.grid(row=1, column=1, padx=10, pady=30)


        okBtn = tk.Button(self.resFrame, command=self.resFun, text="OK", bd=2, bg="gray", width=20, font=("Arial", 20, "bold"))
        okBtn.grid(row=2, column=1, padx=30, pady=40)

    
    def resFun(self):
        rn = int(self.rnIn.get())
        bk = int(self.bkIn.get())
        try:
            con = pymysql.connect(host="localhost", user="root", passwd="barkha", database="record")
            cur = con.cursor()
            query = f"select sName,total_book from reg where rollNo={rn}"
            cur.execute(query)
            std = cur.fetchone()
            query2 = f"select bName,quant from library where bookID={bk}"
            cur.execute(query2)
            bkName = cur.fetchone()

            if std and bkName:
                if bkName[1] > 0:
                    totalBooks = std[1]+1
                    query3 = f"update reg set total_book={totalBooks} where rollNo={rn}"
                    cur.execute(query3)
                    con.commit()
                    remQuant = bkName[1] -1
                    query4 = f"update library set quant={remQuant} where bookID={bk}"
                    cur.execute(query4)
                    con.commit()
                    tk.messagebox.showinfo("Success", f"Book. {bkName[0]} Reserverd for student. {std[0]}")

                    cur.execute("select * from library")
                    newVal = cur.fetchall()

                    self.tabFun()
                    self.table.delete(*self.table.get_children())
                    for j in newVal:
                        self.table.insert('',tk.END, values=j)

                    self.desResFrame()    
                else:
                    tk.messagebox.showerror("Error", "This Book is out of Stock")  
                    self.desResFrame()   
            else:
                tk.messagebox.showerror("Error", "Invalid RollNo or Book ID")          
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")   

    def desResFrame(self):
        self.resFrame.destroy()    

    def retFun(self):
        self.resFrame = tk.Frame(self.root, bg=self.clr(150,200,80), bd=4, relief="ridge")
        self.resFrame.place(width=self.width/3, height=self.height-180, x=self.width/3+120, y=100)    

        rnLbl = tk.Label(self.resFrame, bg=self.clr(150,200,80), text="RollNo:", font=("Arial", 15, "bold"))
        rnLbl.grid(row=0, column=0, padx=20, pady=30)
        self.rnIn = tk.Entry(self.resFrame, bd=1, font=("Arial", 15, "bold"), width=20)
        self.rnIn.grid(row=0, column=1, padx=10, pady=30)

        bkLbl = tk.Label(self.resFrame, bg=self.clr(150,200,80), text="Book_Id:", font=("Arial", 15, "bold"))
        bkLbl.grid(row=1, column=0, padx=20, pady=30)
        self.bkIn = tk.Entry(self.resFrame, bd=1, font=("Arial", 15, "bold"), width=20)
        self.bkIn.grid(row=1, column=1, padx=10, pady=30)


        okBtn = tk.Button(self.resFrame, command=self.retBk, text="OK", bd=2, bg="gray", width=20, font=("Arial", 20, "bold"))
        okBtn.grid(row=2, column=1, padx=30, pady=40)    

    def retBk(self):
        rn = int(self.rnIn.get())
        bk = int(self.bkIn.get())

        con = pymysql.connect(host="localhost", user="root", passwd="barkha", database="record")
        cur = con.cursor()
        query = f"select bName,quant from library where bookID={bk}"
        cur.execute(query)
        rowBk = cur.fetchone()

        query2 = f"select sName, total_book from reg where rollNo={rn}"
        cur.execute(query2)
        rowStd = cur.fetchone()

        if rowBk and rowStd:
            stdBook = rowStd[1] -1
            bkQuant = rowBk[1]+1

            query3 = f"update library set quant={bkQuant} where bookID={bk}"
            cur.execute(query3)
            con.commit()

            query4 = f"update reg set total_book={stdBook} where rollNo={rn}"
            cur.execute(query4)
            con.commit()

            cur.execute("select * from library")
            data = cur.fetchall()

            self.tabFun()
            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('',tk.END, values=i)

            tk.messagebox.showinfo("Success", f"Book.{rowBk[0]} returend from Student.{rowStd[0]}")
            self.desResFrame()

            

        else:
            tk.messagebox.showerror("Error", "Invalid Book or Student ID")    

            

    


        
        





    '''define colors'''
    def clr(self,r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"    

root = tk.Tk()
obj = library(root)
root.mainloop()     