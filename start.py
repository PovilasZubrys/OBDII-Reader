from src.Run import Run
from src.SendData import SendData
import threading
import time

appObd = Run()
sendData = SendData()


def start():
    while True:
        for DataType in appObd.DataLogger.AvailableCommands:
            sendData.query(appObd.DataLogger.get_current_value(DataType), DataType)


if __name__ == '__main__':
    print('Starting OBD thread')
    thread = threading.Thread(target=appObd.start)
    thread.start()
    time.sleep(1)
    start()
