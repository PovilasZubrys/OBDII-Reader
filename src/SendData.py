import mysql.connector as mysql
import config.Database as Db
import json
from datetime import datetime
import requests
import config.MercureCredentials as mercure
import jwt

class SendData:

    lastValue = {}
    mydb = None
    vehicle_id = None
    bearer_token = None

    def __init__(self):
        if self.mydb is None:
            self.mydb = mysql.connect(
                host=Db.DatabaseCredentials['host'],
                user=Db.DatabaseCredentials['user'],
                password=Db.DatabaseCredentials['password'],
                database=Db.DatabaseCredentials['database']
            )

        self.bearer_token = jwt.encode(payload=mercure.MercureCredentials['payload'],
                         key=mercure.MercureCredentials['auth_jwt'],
                         algorithm=mercure.MercureCredentials['algorithm'])

    def query(self, r, TableName):
        if self.vehicle_id is None:
            self.get_vehicle_id()

        if r != 'N/A':
            if TableName in self.lastValue and self.lastValue[TableName] != r or TableName not in self.lastValue:
                cursor = self.mydb.cursor()
                sql = "INSERT INTO " + TableName.lower() + " (value, vehicle_id, date) VALUES (%s, %s, %s)"
                cursor.execute(sql, (r, self.vehicle_id, datetime.now()))

                self.mydb.commit()

            self.lastValue[TableName] = r

    def get_vehicle_id(self):
        data = open('config/Settings.json')
        data = json.loads(data.read())

        cursor = self.mydb.cursor()
        sql = "SELECT v.id FROM vehicle v LEFT JOIN device d ON v.device_id = d.id WHERE d.authentication_token = %s"
        cursor.execute(sql, (data['authentication_token'],))
        vehicle_id = cursor.fetchone()
        self.vehicle_id = vehicle_id[0]

    def send_request_mercure(self, r, TableName):
        if self.vehicle_id is None:
            self.get_vehicle_id()

        if r != 'N/A':
            if TableName in self.lastValue and self.lastValue[TableName] != r or TableName not in self.lastValue:
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Bearer ' + self.bearer_token
                }

                data = {'topic': '/vehicle_data', 'data': json.dumps({TableName.lower(): r})}

                requests.post(mercure.MercureCredentials['endpoint_url'], headers=headers, data=data)