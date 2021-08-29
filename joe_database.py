import sqlite3
import easygui as ui

conn = sqlite3.connect("films.db")
c = conn.cursor()


def sortdata(values):
    name, year, rating, runtime, genre = values
    return [str(name).title(), int(year), str(rating).upper().strip(), int(runtime), str(genre).title()]


def insert_errorcheck(i, n, v):
    if i == 1 or i == 3:
        try:
            v = int(v)
        except:
            return '"{}" must be an integer'.format(n)
    if i == 1:
        if v < 1888:
            return 'There were no movies released in {}'.format(v)
    if i == 3:
        if v < 0:
            return 'Movies must have a positive runtime, not {} minutes'.format(v)
    if i == 2:
        if v.upper().strip() not in ["G", "PG", "R", "R13", "R16", "R18", "M"]:
            return '{} is not a valid age restriction'.format(v)


def insert():
    fieldnames = ["Title", "Release Year", "Age Rating", "Runtime (minutes)", "Genre"]
    values = ui.multenterbox("Please enter the information on your film", "Add a film", fieldnames)
    while 1:
        if values is None:
            break
        errs = list()
        for i, n, v in zip(range(len(fieldnames)), fieldnames, values):
            if v.strip() == "":
                errs.append('"{}" is a required field.'.format(n))
            else:
                if insert_errorcheck(i, n, v) is not None:
                    errs.append(insert_errorcheck(i, n, v))
                    values[i] = ""
        if not len(errs):
            values = sortdata(values)
            c.execute("INSERT INTO tblFilms(TITLE,YEAR,AGE,RUNTIME,GENRE) VALUES (?,?,?,?,?);", values)
            conn.commit()
            break
        values = ui.multenterbox("\n".join(errs), "Add a film", fieldnames, values)


def amend():
    c.execute("SELECT TITLE from tblFilms")
    titles = c.fetchall()
    titles = [t for x in titles for t in x]
    title = ui.multchoicebox("Which movie do you want to amend", choices=titles, preselect=None)
    items = ["TITLE", "YEAR", "AGE", "RUNTIME", "GENRE"]
    if title is not None:
        for movie in title:
            fieldnames = ["Title", "Release Year", "Age Rating", "Runtime (minutes)", "Genre"]
            values = list(c.execute("SELECT * FROM tblFilms where TITLE = '" + movie + "'"))
            values = list(values[0])[1:]
            values = ui.multenterbox("Change the information you'd like", "Add a film", fieldnames, values)
            while 1:
                if values is None:
                    break
                errs = list()
                for i, n, v in zip(range(len(fieldnames)), fieldnames, values):
                    if v.strip() == "":
                        errs.append('"{}" is a required field.'.format(n))
                    else:
                        if insert_errorcheck(i, n, v) is not None:
                            errs.append(insert_errorcheck(i, n, v))
                            values[i] = ""
                if not len(errs):
                    break
                values = ui.multenterbox("\n".join(errs), "Add a film", fieldnames, values)
            if values is None:
                continue
            values = sortdata(values)
            for i in range(len(items)):
                if i == 0:
                    c.execute(
                        "UPDATE tblFilms SET '" + items[i] + "' = '" + str(
                            values[i]) + "' where TITLE = '" + movie + "'")
                else:
                    c.execute(
                        "UPDATE tblFilms SET '" + items[i] + "' = '" + str(values[i]) + "' where TITLE = '" +
                        values[
                            0] + "'")
    conn.commit()


def sort_category():
    fieldnames = ["Title", "Release Year", "Age Rating", "Runtime (minutes)", "Genre"]
    column = ui.buttonbox("Choose a column to sort by", choices=fieldnames)
    showdb(fieldnames.index(column) + 1)


def showdb(sort_key):
    printtemp = []
    for row in c.execute('SELECT * FROM tblFilms'):
        printtemp.append(row)
    printtemp = sorted(printtemp, key=lambda x: x[sort_key])
    for i in range(len(printtemp)):
        printtemp[i] = list(printtemp[i])
        printtemp[i][0] = i + 1
        printtemp[i] = ", ".join([str(x) for x in printtemp[i]])
    ui.codebox("Here is the database", text="\n".join(printtemp))


def delete():
    c.execute("SELECT TITLE from tblFilms")
    films = c.fetchall()
    films = [t for x in films for t in x]
    film = ui.multchoicebox("Which city do you want to delete", choices=films, preselect=None)
    if film is not None:
        for title in film:
            if title is not None:
                c.execute("DELETE FROM tblFilms WHERE TITLE='" + title + "'")
    conn.commit()


ans = ""
while ans != "Quit":
    ans = ui.buttonbox("What do you want to do", choices=["Print", "Insert", "Amend", "Delete", "Quit"], title="Menu")
    if ans == "Print":
        choice = ui.buttonbox("What would you like to do?", choices=["Search for item", "Sort by category",
                                                                     "View in default ordering", "Return to main menu"])
        if choice == "Search for item":
            pass
        if choice == "Sort by category":
            sort_category()
        if choice == "View in default ordering":
            showdb(0)
        if choice == "Return to main menu":
            pass
    if ans == "Insert":
        insert()
    if ans == "Amend":
        amend()
    if ans == "Delete":
        delete()
    if ans is None:
        break
