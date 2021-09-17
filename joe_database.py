import sqlite3
import easygui as ui

conn = sqlite3.connect("films.db")
c = conn.cursor()


def sortdata(values):  # Sorts the data into the appropriate format (ensures strings begin with a capital letter and
    name, year, rating, runtime, genre = values  # don't have trailing whitespaces, ensures integers are saved as
    return [str(name).title(), int(year), str(rating).upper().strip(), int(runtime), str(genre).title()]  # integers)


def insert_errorcheck(i, n, v):  # Function used by both the insert and amend functions to ensure each input is valid
    # i is the number associated with each variable so the program can determine which error checking to apply
    # n is the name of the variable used to output relevant error messages (eg. "Release Year" must be an integer)
    # v is the user entered value associated with each variable, which is tested to ensure it's a valid input
    year_boundary = 1888  # Using boundary variables makes it easier to navigate and change the expected data
    age_ratings = ["G", "PG", "R", "R13", "R16", "R18", "M"]
    if i == 1 or i == 3:
        try:
            v = int(v)
        except:
            return '"{}" must be an integer'.format(n)
    if i == 1:
        if v < year_boundary:
            return 'There were no movies released in {}'.format(v)
    if i == 3:
        if v < 1:
            return 'Movies must have a positive runtime, not {} minutes'.format(v)
    if i == 2:
        if v.upper().strip() not in age_ratings:
            return '{} is not a valid age restriction'.format(v)


def insert():  # Function to insert a film into the database
    fieldnames = ["Title", "Release Year", "Age Rating", "Runtime (minutes)", "Genre"]
    values = ui.multenterbox("Please enter the information on your film", "Add a film", fieldnames)
    while 1:  # Error checking loop
        if values is None:  # Exits back to menu if the user selects cancel or [x]
            break
        errs = list()  # Empty list to append relevant error messages
        for i, n, v in zip(range(len(fieldnames)), fieldnames, values):  # Variables explained previously
            if v.strip() == "":  # Ensuring the user hasn't left any fields blank or with just whitespace
                errs.append('"{}" is a required field.'.format(n))
            else:
                if insert_errorcheck(i, n, v) is not None:  # Only appends if there is an error message
                    errs.append(insert_errorcheck(i, n, v))
                    values[i] = ""  # Removes the users invalid input so the next time the insert box is shown,
                    # only the valid inputs will remain
        if not len(errs):  # If there are no errors insert the data into the film and break the loop
            values = sortdata(values)
            c.execute("INSERT INTO tblFilms(TITLE,YEAR,AGE,RUNTIME,GENRE) VALUES (?,?,?,?,?);", values)
            conn.commit()
            break
        values = ui.multenterbox("\n".join(errs), "Add a film", fieldnames, values)  # Otherwise prompt the user to
        # enter values again


def amend():  # Function to change a film's data
    c.execute("SELECT TITLE from tblFilms")
    titles = c.fetchall()
    titles = [t for x in titles for t in x]  # Titles are currently in single value tuples nested in a list, so this
    # removes them from the tuples
    title = ui.multchoicebox("Which movie do you want to amend", choices=titles, preselect=None)
    items = ["TITLE", "YEAR", "AGE", "RUNTIME", "GENRE"]
    if title is not None:  # Once again allowing for cancel or [x] inputs
        for movie in title:  # The user can select multiple titles at a time, this will run through for each film
            fieldnames = ["Title", "Release Year", "Age Rating", "Runtime (minutes)", "Genre"]
            sql = "SELECT * FROM tblFilms where TITLE = ?"  # Parameterised sql to protect against injection attacks
            # and allow for films with strange characters (eg those that contain an apostrophe)
            fields = list(c.execute(sql, [movie]))  # Selects the relevant information for the chosen film
            fields = list(fields[0])[1:]  # Removes the information from tuple and ignores the primary key as it is
            # only needed by the software
            values = ui.multenterbox("Change the information you'd like", "Amend a film", fieldnames, fields)
            while 1:  # Same error checking loop as insert film component
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
                if i == 0:  # Updates the film title where TITLE = the original title
                    sql = "UPDATE tblFilms SET '" + items[i] + "' = ? where TITLE = ?"
                    c.execute(sql, [str(values[i]), movie])
                else:  # Updates for every other variable as the film title may have been changed
                    sql = "UPDATE tblFilms SET '" + items[i] + "' = ? where TITLE = ?"
                    c.execute(sql, [str(values[i]), values[0]])
    conn.commit()


def sort_category():
    fieldnames = ["Title", "Release Year", "Age Rating", "Runtime (minutes)", "Genre"]
    column = ui.buttonbox("Choose a column to sort by", choices=fieldnames)
    if column is not None:
        showdb(fieldnames.index(column) + 1)  # Sorts by key used in showdb (the reason for the +1 is because
        # fieldnames doesn't include the primary key)


def search():  # Function to search for a card
    while 1:  # Error checking loop ensures the user doesn't enter a blank field
        query = ui.enterbox("Please enter the name of the film you want to search for")
        if query == "":
            ui.msgbox("This is a required field")
        else:
            break
    if query is not None:  # Only runs if the input wasn't cancel or [x] otherwise returns to the main menu
        lstquery = query.split()  # Splits the user's input into a list of each 'word' to allow multiple variations of
        # the query to be searched
        temp = []
        # The following code (up until inaccurate_search = False) is a little difficult to explain, but essentially
        # it takes an input (eg the nice guys) and splits it into every possible combination to allow for spelling
        # mistakes in certain words
        # Using the example, this would give the following output:
        # [['the', 'nice', 'guys'], ['the', 'nice'], ['nice', 'guys'], ['the'], ['nice'], ['guys']]
        for i in range(len(lstquery)):
            for x in range(len(lstquery)):
                if x == 0:
                    temp.append(lstquery[i:])
                else:
                    temp.append(lstquery[i:-x])
        temp = [x for x in temp if x != []]  # Removes empty lists from the nested list
        temp.sort(key=len, reverse=True)  # Sorts the nested list in descending order based on the length of each
        # sublist this allows the program to stop looking when it gets the most accurate search result (longest sublist)
        inaccurate_search = False
        for i in range(len(temp)):  # Tests each sublist to see if it is contained in a film title and breaks once it
            # finds a match
            temp[i] = " ".join(temp[i])  # turns the sublist into a string, eg ['the', 'nice', 'guys'] → 'the nice guys'
            c.execute("SELECT * FROM tblFilms WHERE TITLE LIKE ? ", ("%" + temp[i] + "%",))  # Using where TITLE LIKE
            # allows for differences in capitalisation further enhancing the programs ability to find a search result
            rows = c.fetchall()
            if len(temp) - i == len(lstquery) and len(lstquery) != 1:  # Essentially, if the loop has got down to
                # searching one word sublists (such as 'the' where there will be a number of results) then it is
                # recorded so the program can display a different message and acknowledge that it couldn't find an
                # accurate result. 'and len(lstquery) != 1' ensures this message isn't shown if the user's query is
                # only one word long (e.g 'divergent')
                inaccurate_search = True
            if rows != []:  # Once a result is found break out of the code
                break
        rows = [tuple(str(x) for x in y) for y in rows]  # As the data is retrieved directly from the database there
        # will be varying datatypes, this makes every item a string for ease of displaying.
        if rows == []:
            ui.msgbox("Sorry but there weren't any matches, try changing the spelling or viewing the entire database")
        elif inaccurate_search == True:
            ui.codebox("Sorry but there weren't any exact results, here are the closest ones to your query (" +
                       " ".join(lstquery) + "):", text="\n".join([", ".join(x[1:]) for x in rows]))
        else:
            ui.codebox("Search results:", text="\n".join([", ".join(x[1:]) for x in rows]))


def showdb(sort_key):  # Function to display the database
    printtemp = []
    for row in c.execute('SELECT * FROM tblFilms'):  # Creates nested tuple containing all the data in the database
        printtemp.append(row)
    printtemp = sorted(printtemp, key=lambda x: x[sort_key])  # Sorts the database using the key given, i.e given a
    # key of 2, the program  will sort the nested tuple by whatever value is at index 2 (in this case it would sort
    # by Release Year)
    for i in range(len(printtemp)):
        printtemp[i] = list(printtemp[i])  # Converts each tuple to a list
        printtemp[i][0] = i + 1  # The primary key isn't necessarily in sequential order as is the nature of primary
        # keys, therefore for display purposes this replaces the primary key with a counter
        printtemp[i] = ", ".join([str(x) for x in printtemp[i]])  # Convert each sublist into a comma separated string
    ui.codebox("Here is the database", text="\n".join(printtemp))


def delete():
    c.execute("SELECT TITLE from tblFilms")
    films = c.fetchall()
    films = [t for x in films for t in x]  # Same as before, removes values from nested function
    film = ui.multchoicebox("Which movie do you want to delete", choices=films, preselect=None)
    if film is not None:
        for title in film:
            if title is not None:
                c.execute("DELETE FROM tblFilms WHERE TITLE='" + title + "'")
    conn.commit()


ans = ""
while ans != "Quit":  # Main menu loop
    ans = ui.buttonbox("What do you want to do", choices=["View data", "Insert", "Amend", "Delete", "Quit"], title=
    "Menu")
    if ans == "View data":
        choice = ui.buttonbox("What would you like to do?", choices=["Search for item", "Sort by category",
                                                                     "View in default ordering", "Return to main menu"])
        if choice == "Search for item":
            search()
        if choice == "Sort by category":
            sort_category()
        if choice == "View in default ordering":
            showdb(0)  # Note the sort_key is 0 which will sort by primary key or more specifically, the order in
            # which items were added to the database
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
