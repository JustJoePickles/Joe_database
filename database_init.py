import sqlite3, os

os.remove("films.db")

conn = sqlite3.connect("films.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE tblFilms
(id INTEGER PRIMARY KEY AUTOINCREMENT,
TITLE TEXT,
YEAR INTEGER,
AGE TEXT,
RUNTIME INTEGER,
GENRE TEXT);''')

VALUES = [(1,"Ghostbusters",2016,"PG",116,"Comedy"),
          (2,"The Legend of Tarzan",2016,"PG",109,"Action"),
          (3,"Jason Bourne",2016,"PG",123,"Action"),
          (4,"The Nice Guys",2016,"R",116,"Crime"),
          (5,"The Secret Life of Pets",2016,"G",91,"Animation"),
          (6,"Star Trek Beyond",2016,"PG",120,"Action"),
          (7,"Batman v Superman",2016,"PG",151,"Action"),
          (8,"Finding Dory",2016,"G",103,"Animation"),
          (9,"Zootopia",2016,"G",108,"Animation"),
          (10,"The BFG",2016,"PG",90,"Fantasy"),
          (11,"A Monster Calls",2016,"PG",108,"Fantasy"),
          (12,"Independence Day: Resurgence",2016,"PG",120,"Action"),
          (13,"The Green Room",2016,"R",94,"Crime"),
          (14,"Doctor Strange",2016,"PG",130,"Fantasy"),
          (15,"The Jungle Book",2016,"PG",105,"Fantasy"),
          (16,"Alice Through the Looking Glass",2016,"PG",118,
           "Fantasy"),
          (17,"Imperium",2016,"R",109,"Crime"),
          (18,"The Infiltrator",2016,"R",127,"Crime"),
          (19,"Mad Max: Fury Road",2015,"R",120,"Action"),
          (20,"Spectre",2015,"PG",145,"Action"),
          (21,"Jurassic World",2015,"PG",100,"Action"),
          (22,"The Intern",2015,"PG",121,"Comedy"),
          (23,"Ted 2",2015,"R",121,"Comedy"),
          (24,"Trainwreck",2015,"R",122,"Comedy"),
          (25,"Inside Out",2015,"PG",94,"Animation"),
          (26,"The Good Dinosaur",2015,"G",101,"Animation"),
          (27,"Divergent",2014,"PG",121,"Action"),
          (28,"The Max Runner",2014,"PG",115,"Action"),
          (29,"Birdman",2014,"R",119,"Comedy"),
          (30,"Guardians of the Galaxy",2014,"PG",121,"Fantasy"),
          (31,"The Lego Movie",2014,"PG",100,"Animation"),
          (32,"Big Hero 6",2014,"PG",108,"Animation"),
          (33,"The Drop",2014,"R",106,"Crime")]

for item in VALUES:
    params = []
    for object in item:
        params.append(object)
    cursor.execute("INSERT INTO tblFilms VALUES (?,?,?,?,?,?)", params)

conn.commit()
conn.close()