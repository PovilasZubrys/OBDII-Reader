import json
import requests
import config.MercureCredentials as mercure
import jwt

class SendData:

    lastValue = {}
    bearer_token = None

    def __init__(self):
        self.bearer_token = jwt.encode(payload=mercure.MercureCredentials['payload'],
                         key=mercure.MercureCredentials['auth_jwt'],
                         algorithm=mercure.MercureCredentials['algorithm'])

    def send_data(self, dataBatch):
        url = "http://livevehicledata.lan/api/send/vehicle_data"
        payload = json.dumps(dataBatch['data'])
        headers = {
            'Content-Type': 'application/json'
        }

        requests.post(url, headers=headers, data=payload)

    def send_request_mercure(self, r, TableName, VehicleId):
        if r != 'N/A' and VehicleId is not None:
            if TableName in self.lastValue and self.lastValue[TableName] != r or TableName not in self.lastValue:
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Bearer ' + self.bearer_token
                }

                data = {'topic': '/vehicle_data/' + str(VehicleId), 'data': json.dumps({TableName.lower(): r})}

                requests.post(mercure.MercureCredentials['endpoint_url'], headers=headers, data=data)