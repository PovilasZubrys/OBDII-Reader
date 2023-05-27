import mysql.connector as mysql
import config.Database as Db


class SendData:

    lastValue = {}
    mydb = None

    def __init__(self):
        if self.mydb is None:
            self.mydb = mysql.connect(
                host=Db.DatabaseCredentials['host'],
                user=Db.DatabaseCredentials['user'],
                password=Db.DatabaseCredentials['password'],
                database=Db.DatabaseCredentials['database']
            )

    def query(self, r, TableName):
        if r != 'N/A':
            if TableName in self.lastValue and self.lastValue[TableName] != r or TableName not in self.lastValue:
                cursor = self.mydb.cursor()
                sql = "INSERT INTO " + TableName.lower() + " (value) VALUES (%s)"
                cursor.execute(sql, (r,))

                self.mydb.commit()

            self.lastValue[TableName] = r
