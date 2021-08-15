import sqlite3
import easygui as ui

conn = sqlite3.connect("films.db")
c = conn.cursor()


def sortdata():
    None


def insert():
    title = ui.enterbox("Please enter the title of the movie")
    year = ui.integerbox("Please enter the year the movie was released", lowerbound=1888,upperbound=2050)
    age = ui.enterbox("Please enter the age restriction on the movie")
    runtime=ui.integerbox("Please enter the length of the film in minutes", lowerbound=0, upperbound=500)
    genre=ui.enterbox("Please enter the genre of the film")
    values = (str(title),int(year),str(age),int(runtime),str(genre))
    c.execute("INSERT INTO tblFilms(TITLE,YEAR,AGE,RUNTIME,GENRE) VALUES (?,?,?,?,?);", values)
    conn.commit()


def amend():
    None


def showdb():
    printtemp = []
    for row in c.execute('SELECT * FROM tblFilms'):
        printtemp.append(row)
    for i in range(len(printtemp)):
        printtemp[i] = ", ".join([str(x) for x in printtemp[i]])
    ui.codebox("Here is the database", text="\n".join(printtemp))


def delete():
    c.execute("SELECT TITLE from tblFilms")
    films = c.fetchall()
    films = [t for x in films for t in x]
    film = ui.multchoicebox("Which city do you want to delete", choices=films, preselect=None)
    print(films, film)
    for title in film:
        print(title)
        if title is not None:
            c.execute("DELETE FROM tblFilms WHERE TITLE='" + title + "'")
    conn.commit()


ans = ""
while ans != "Quit":
    ans = ui.buttonbox("What do you want to do", choices=["Print", "Insert", "Amend", "Delete", "Quit"], title="Menu")
    if ans == "Print":
        showdb()
    if ans == "Insert":
        insert()
    if ans == "Amend":
        amend()
    if ans == "Delete":
        delete()
