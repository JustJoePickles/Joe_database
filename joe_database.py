import sqlite3
import easygui as ui

conn = sqlite3.connect("films.db")
c = conn.cursor()

def sortdata():
    None

def insert():
    None

def amend():
    None

def printdb():
    printtemp = []
    for row in c.execute('SELECT * FROM tblFilms'):
        printtemp.append(row)
    for i in range(len(printtemp)):
        printtemp[i] = ", ".join([str(x) for x in printtemp[i]])
    ui.codebox("Here is the database", text="\n".join(printtemp))

def delete():
    None

ans = ""
while ans != "Quit":
    ans = ui.buttonbox("What do you want to do", choices=["Print", "Insert", "Amend", "Delete", "Quit"], title="Menu")
    if ans == "Print":
        printdb()
    if ans == "Insert":
        insert()
    if ans == "Amend":
        amend()
    if ans == "Delete":
        delete()