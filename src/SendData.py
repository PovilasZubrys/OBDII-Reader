import mysql.connector as mysql
import config.Database as db


class SendData:

    lastValue = 0
    mydb = None

    def __init__(self):
        self.mydb = mysql.connect(
            host=db.database_credentials['host'],
            user=db.database_credentials['user'],
            password=db.database_credentials['password'],
            database=db.database_credentials['database']
        )

    def connect(self, r):
        if r != 'N/A':
            if self.lastValue != r:
                cursor = self.mydb.cursor()
                sql = "INSERT INTO speed (value) VALUES (%s)"
                cursor.execute(sql, (r,))

                self.mydb.commit()
                self.lastValue = r
