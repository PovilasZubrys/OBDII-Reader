import obd
from config.ObdCommands import ObdCommands
from src.DataLogger import DataLogger


class Run:

    connection = None
    commands = ObdCommands

    def __init__(self):
        self.DataLogger = DataLogger()

    def start(self):
        if self.connection is None or self.connection.is_connected() is False:
            print('Connecting')
            # When debugging
            self.connection = obd.Async("/dev/pts/1")

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
