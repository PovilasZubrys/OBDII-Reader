from src.Run import Run
from src.SendData import SendData
import threading
import time

appObd = Run()
sendData = SendData()


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

if __name__ == '__main__':
    print('Starting OBD thread')
    thread = threading.Thread(target=appObd.start)
    databaseLogThread = threading.Thread(target=database_log())
    thread.start()
    databaseLogThread.start()
    time.sleep(1)
    start()
