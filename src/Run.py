from config.ObdCommands import ObdCommands
from src.DataLogger import DataLogger
from src.FirstRunSetup import FirstRunSetup
from datetime import datetime
import obd
import json

class Run:

    connection = None
    commands = ObdCommands
    vehicle_id = None

    def __init__(self):
        self.DataLogger = DataLogger()
        self.FirstRunSetup = FirstRunSetup()

    def start(self):
        data = self.load_settings()
        if data['first_run'] is True:
            self.FirstRunSetup.setup(data)

        if self.connection is None or self.connection.is_connected() is False:
            self.get_vehicle_id()
            print('Connecting')
            # When debugging
            self.connection = obd.Async("/dev/pts/8")

            # When connected to actual OBD scan tool
            # self.connection = obd.Async("/dev/ttyACM0")

        self.start_watch_commands()
        self.connection.start()

    def start_watch_commands(self):
        for c in self.commands:
            self.connection.watch(eval(c), callback=self.log_data)

    def log_data(self, r):
        if hasattr(r.value, 'm') is False:
            return

        self.DataLogger.set_current_value(r.value.m, r.command.name)
        self.DataLogger.add_data_batch(r.value.m, r.command.name, self.vehicle_id, datetime.now().strftime('%Y-%m-%d, %H:%M:%S'))

    def load_settings(self):
        file = open('config/Settings.json')
        data = json.load(file)

        return data

    def get_vehicle_id(self):
        # data = open('config/Settings.json')
        # data = json.loads(data.read())
        self.vehicle_id = 1