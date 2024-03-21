from src.Run import Run
from src.SendData import SendData
from src.GPS import Gps
from datetime import datetime
import threading
import time

appObd = Run()
sendData = SendData()
gps = Gps()


def start():
    while True:
        time.sleep(0.5)
        for DataType in appObd.DataLogger.AvailableCommands:
            sendData.send_request_mercure(appObd.DataLogger.get_current_value(DataType), DataType, appObd.vehicle_id)

def database_log():
    while True:
        time.sleep(15)
        sendData.send_data(appObd.DataLogger.get_current_data_batch())
        appObd.DataLogger.set_empty_data_batch()

def get_gps_data():
    serial = Gps.enable_serial()
    Gps.enable_gps(serial)
    time.sleep(1)

    while True:
        coordinates = Gps.get_gps_location(serial)
        if not coordinates:
            continue

        appObd.DataLogger.set_current_value(coordinates, 'gps')
        appObd.DataLogger.add_data_batch(coordinates, 'gps', appObd.get_vehicle_id, datetime.now().strftime('%Y-%m-%d, %H:%M:%S'))
        time.sleep(1)


if __name__ == '__main__':
    print('Starting OBD thread')
    thread = threading.Thread(target=appObd.start)
    databaseLogThread = threading.Thread(target=database_log)
    gpsThread = threading.Thread(target=get_gps_data)
    gpsThread.start()
    thread.start()
    databaseLogThread.start()
    time.sleep(1)
    start()
