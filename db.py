import pyodbc

class Sql:
    def __init__(self, database, server="HOME-PC\SQLEXPRESS"):
        self.server = server
        self.database = database
        self.cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"                   
                                    "Server=" + self.server + ";"
                                    "Database=" + self.database + ";"
                                    "Trusted_Connection=yes;")

