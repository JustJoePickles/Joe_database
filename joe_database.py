import sqlite3
import easygui as ui

conn = sqlite3.connect("films.db")
c = conn.cursor()


def sortdata(name, year, rating, runtime, genre):
    return [str(name).title(),int(year),str(rating).upper(),int(runtime),str(genre).title()]


def insert():
    title = ui.enterbox("Please enter the title of the movie")
    year = ui.integerbox("Please enter the year the movie was released", lowerbound=1888, upperbound=2050)
    age = ui.enterbox("Please enter the age restriction on the movie")
    runtime = ui.integerbox("Please enter the length of the film in minutes", lowerbound=0, upperbound=500)
    genre = ui.enterbox("Please enter the genre of the film")
    values = (str(title), int(year), str(age), int(runtime), str(genre))
    c.execute("INSERT INTO tblFilms(TITLE,YEAR,AGE,RUNTIME,GENRE) VALUES (?,?,?,?,?);", values)
    conn.commit()


def amend():
    c.execute("SELECT TITLE from tblFilms")
    titles = c.fetchall()
    titles = [t for x in titles for t in x]
    title = ui.multchoicebox("Which movie do you want to amend", choices=titles, preselect=None)
    items = ["TITLE", "YEAR", "AGE", "RUNTIME", "GENRE"]
    for movie in title:
        name = ui.enterbox("Please enter a new title for " + movie)
        year = ui.integerbox("Please enter a new year of release for " + movie)
        rating = ui.enterbox("Please enter a new age rating for " + movie)
        runtime = ui.integerbox("Please enter a new runtime for " + movie)
        genre = ui.enterbox("Please enter a new genre for " + movie)
        updated_values = sortdata(name, year, rating, runtime, genre)
        for i in range(len(items)):
            if i == 0:
                c.execute(
                    "UPDATE tblFilms SET '" + items[i] + "' = '" + str(updated_values[i]) + "' where TITLE = '" + movie + "'")
            else:
                c.execute(
                    "UPDATE tblFilms SET '" + items[i] + "' = '" + str(updated_values[i]) + "' where TITLE = '" + updated_values[
                        0] + "'")
    conn.commit()


def showdb():
    printtemp = []
    for row in c.execute('SELECT * FROM tblFilms'):
        printtemp.append(row)
    print(printtemp)
    for i in range(len(printtemp)):
        printtemp[i]=list(printtemp[i])
        printtemp[i][0]=i+1
        printtemp[i] = ", ".join([str(x) for x in printtemp[i]])
    ui.codebox("Here is the database", text="\n".join(printtemp))


def delete():
    c.execute("SELECT TITLE from tblFilms")
    films = c.fetchall()
    films = [t for x in films for t in x]
    film = ui.multchoicebox("Which city do you want to delete", choices=films, preselect=None)
    for title in film:
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
