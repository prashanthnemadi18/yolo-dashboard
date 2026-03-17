from tkinter import *
from tkinter import messagebox

parent = Tk()
parent.title("student details from user")
parent.geometry("400x400")

name=Label(parent, text="Name", fg="blue", bg="lightblue", font=("Arial", 10, "bold"))
name.grid(row=0, column=0,padx=10, pady=10)
e1=Entry(parent, fg="darkblue", bg="lightyellow", font=("Arial", 10))
e1.grid(row=0, column=1,padx=10, pady=10)

roll=Label(parent, text="Roll No", fg="green", bg="lightgreen", font=("Arial", 10, "bold"))  
roll.grid(row=1, column=0,padx=10, pady=10)
e2=Entry(parent, fg="darkgreen", bg="lightyellow", font=("Arial", 10))
e2.grid(row=1, column=1,padx=10, pady=10)

def submit_name():
    name_value = e1.get()
    roll_value = e2.get()
    
    if name_value == "" or roll_value == "":
        messagebox.showerror("Error", "Please fill all fields!")
    else:
        messagebox.showinfo("Success", f"Student Details Submitted:\nName: {name_value}\nRoll No: {roll_value}")
        e1.delete(0, END)
        e2.delete(0, END)

submit=Button(parent, text="Submit", command=submit_name, bg="orange", fg="white", font=("Arial", 10, "bold"))
submit.grid(row=2, column=0,padx=10, pady=10)
parent.mainloop()