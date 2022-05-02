from tkinter import Tk, Button, PhotoImage, Label, LabelFrame, W, E, N, S, Entry, END, StringVar, Scrollbar, Toplevel
from tkinter import ttk  # Provide access to themed widget
import sqlite3
from  datetime import datetime 


class Todo:
    db_file = 'task.db'

    def __init__(self, root):
        self.root = root
        self.drawGui()
        
    def drawGui(self):
        self.icons()
        self.make_label_frame()
        self.message_area()
        self.tree_view()
        ttk.style = ttk.Style()
        ttk.style.configure("TreeView", font=("helvetica", 10))
        ttk.style.configure("TreeView.Heading", font=("helvetica", 12, "bold"))
        self.create_scrollbar()
        self.create_ud_btn()
        self.viewTask()
        self.beginfieldDate.bind("<Button-1>",self.focusBeginDate)
        self.beginfieldDate.bind("<Leave>",self.unfocusBeginDate)
        self.endfieldDate.bind("<Button-1>",self.focusEndDate)
        self.endfieldDate.bind("<Leave>",self.unfocusEndDate)
        
        self.beginfieldTime.bind("<Button-1>",self.focusBeginTime)
        self.beginfieldTime.bind("<Leave>",self.unfocusBeginTime)
        self.endfieldTime.bind("<Button-1>",self.focusEndTime)
        self.endfieldTime.bind("<Leave>",self.unfocusEndTime)
                        

    def execute_db_query(self, query, args=()):
        with sqlite3.connect(self.db_file) as conn:
            print(conn)
            print("Connection réussie")
            cursor = conn.cursor()
            query_result = cursor.execute(query, args)
            conn.commit()
        return query_result

    def add_new_task(self):
        if self.newtakIsValide():
            query = 'INSERT INTO tasklist VALUES(NULL,?,?,?,?,?)'
            args = (self.taskNameField.get(), self.placefield.get(
            ), self.beginfield.get(), self.endfield.get(), self.descriptionfield.get())
            print(args)
            self.execute_db_query(query,args)
            self.message['text'] = "La tache {} a été ajouté avec succes".format(
                self.taskNameField.get())

            self.taskNameField.delete(0,END)
            self.placefield.delete(0,END)
            self.beginfield.delete(0,END)
            self.endfield.delete(0,END)
            self.descriptionfield.delete(0,END)
        else:
            self.message['text'] = "Erreur"
        self.viewTask()
        
    def newtakIsValide(self):
        valid = len(self.taskNameField.get())!=0 and (self.placefield.get())!=0 and len(self.beginfield.get())!=0 and len(self.endfield.get())!=0
        print("VALIDATE RESULT :", valid)
        return valid
    
    def viewTask(self):
        items = self.tree.get_children()
        for item in items :
            self.tree.delete(item)
        query = 'SELECT * FROM tasklist'
        taskEntries = self.execute_db_query(query)
        for row in taskEntries:
            print(row)
            self.tree.insert('',0,text=row[0],value=(row[1],row[2],row[3],row[4],row[5]))
            
    def icons(self):
        icone = PhotoImage(file="icons/icon_todo.png")
        label = Label(image=icone)
        label.image = icone
        label.grid(row=0, column=0)


    def btnTaskAdd(self):
        self.add_new_task()
        
    def make_label_frame(self):
        labelframe = LabelFrame(
            self.root, text="Add New Task", bg="sky blue", font="helvetica 10")
        labelframe.grid(row=0, column=1, padx=8, pady=8, sticky='ew')
        Label(labelframe, text=" Task name :", bg="sky blue").grid(
            row=1, column=1, sticky=W, padx=5, pady=5)
        self.taskNameField = Entry(labelframe)
        self.taskNameField.grid(row=1, column=2, pady=5)
        Label(labelframe, text=" Place :", bg="sky blue").grid(
            row=2, column=1, sticky=W, padx=5, pady=5)
        self.placefield = Entry(labelframe)
        self.placefield.grid(row=2, column=2, pady=5)
        Label(labelframe, text=" Begin :", bg="sky blue").grid(
            row=3, column=1,  sticky=W, padx=5, pady=5)

        self.beginfieldTime = Entry(labelframe)
        self.beginfieldDate = Entry(labelframe)
        self.beginfieldTime.grid(row=3, column=2, pady=5)
        self.beginfieldDate.grid(row=3, column=3, pady=5)
        
        Label(labelframe, text=" End :", bg="sky blue").grid(
            row=4, column=1, sticky=W, padx=5, pady=5)
        self.endfieldTime = Entry(labelframe)
        self.endfieldDate = Entry(labelframe)
        self.endfieldTime.grid(row=4, column=2, pady=5)
        self.endfieldDate.grid(row=4, column=3, pady=5)
        
        Label(labelframe, text=" Task Description :", bg="sky blue").grid(
            row=5, column=1, sticky=W, padx=5, pady=5)
        self.descriptionfield = Entry(labelframe)
        self.descriptionfield.grid(row=5, column=2, pady=5)
        Button(labelframe, text="Add task", command=self.btnTaskAdd).grid(
            row=6, column=2, pady=5, sticky=E)


        self.beginfieldTime.insert(0,"hh:mm")
        self.beginfieldTime["fg"]='gray'
        self.endfieldTime.insert(0,"hh:mm")
        self.endfieldTime["fg"]='gray'

        self.beginfieldDate.insert(0,"dd/mm/yyyy")
        self.beginfieldDate["fg"]='gray'
        self.endfieldDate.insert(0,"dd/mm/yyyy")
        self.endfieldDate["fg"]='gray'

    def message_area(self):
        self.message = Label(text="Wait")
        self.message.grid(row=3, column=1, sticky=W, padx=5)

    def tree_view(self):
        self.tree = ttk.Treeview(height=10, column=("Name","Place","Begin", "End","Description"))
        self.tree.grid(row=6, column=0, columnspan=3)
        self.tree.heading("#0", text="id", anchor=N)
        self.tree.column("#0",minwidth=5,width=35)
        self.tree.heading("Name", text="Task Name", anchor=N)
        self.tree.column("Name",minwidth=5,width=100)
        self.tree.heading("Place", text="Place", anchor=N)
        self.tree.column("Place",minwidth=5,width=100)
        self.tree.heading("Begin", text="Task begin", anchor=N)
        self.tree.column("Begin",minwidth=5,width=100)
        self.tree.heading("End", text="Task end", anchor=N)
        self.tree.column("End",minwidth=5,width=100)
        self.tree.heading("Description", text="Description", anchor=N)
        self.tree.column("Description",minwidth=5, width=150)


    def create_scrollbar(self):
        self.scrollbar = Scrollbar(orient='vertical', command=self.tree.yview)
        self.scrollbar.grid(row=6, column=3, rowspan=3, sticky="sn")

    def create_ud_btn(self):
        Button(text="Modify selected", command='', bg="purple", fg="white").grid(
            row=9, column=0, sticky=W, padx=5, pady=5)
        Button(text="Delete selected", command='', bg="red", fg="white").grid(
            row=9, column=2, sticky=E, padx=5, pady=5)

    # PlaceHolder
#Time
    def focusBeginTime(self,*args):
        self.beginfieldTime.delete(0,'end')
        self.beginfieldTime["fg"]="black"

    def unfocusBeginTime(self,*args):
        if (len(self.beginfieldTime.get())==0):
            self.beginfieldTime.delete(0,'end')
            self.beginfieldTime.insert(0,"hh:mm")
            self.beginfieldTime["fg"]="gray"
        else:
            self.validateTime(self.beginfieldTime.get())
        self.root.focus()

    
    def focusEndTime(self,*args):
        self.endfieldTime.delete(0,'end')
        self.endfieldTime["fg"]="black"

    def unfocusEndTime(self,*args):
        if (len(self.endfieldTime.get())==0):
            self.endfieldTime.delete(0,'end')
            self.endfieldTime.insert(0,"hh:mm")
            self.endfieldTime["fg"]="gray"
        else:
            self.validateTime(self.endfieldTime.get())
        self.root.focus()

#Date
    def focusBeginDate(self,*args):
        print("Date Foscus begin")
        print(self.beginfieldDate.get()!= "dd/mm/yyy")
        if (self.beginfieldDate.get()!= "dd/mm/yyy"):
            print("DAte ", self.beginfieldDate.get())
            self.beginfieldDate.delete(0,'end')
            self.beginfieldDate["fg"]="black"

    def unfocusBeginDate(self,*args):
        print("Unfocus date begin")
        if (len(self.beginfieldDate.get())==0):
            self.beginfieldDate.delete(0,'end')
            self.beginfieldDate.insert(0,"dd/mm/yyyy")
            self.beginfieldDate["fg"]="gray"
        else:
            self.validateDate(self.beginfieldDate.get())
        self.root.focus()

    
    def focusEndDate(self,*args):
        self.endfieldDate.delete(0,'end')
        self.endfieldDate["fg"]="black"

    def unfocusEndDate(self,*args):
        if (len(self.endfieldDate.get())==0):
            self.endfieldDate.delete(0,'end')
            self.endfieldDate.insert(0,"dd/mm/yyyy")
            self.endfieldDate["fg"]="gray"
        else:
            self.validateDate(self.endfieldDate.get())
        self.root.focus()

    def validateDate(self,dateString):
        format = "%d/%m/%Y"
        try :
            datetime.strptime(dateString, format)
            print("Date valide")
        except :
            print("Date not valid")
    
    def validateTime(self,dateString):
        format = "%H:%M"
        try :
            datetime.strptime(dateString, format)
            print("Time valided")
        except :
            print("Time not valid")



if __name__ == "__main__":
    root = Tk()
    root.title("My Todo List")
    application = Todo(root)
    root.mainloop()
