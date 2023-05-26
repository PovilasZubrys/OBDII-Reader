import obd
from config.ObdCommands import obd_commands
from src.DataLogger import DataLogger


class Run:

    connection = None
    commands = obd_commands

    def __init__(self):
        self.DataLogger = DataLogger()

    def start(self):
        if self.connection is None or self.connection.is_connected() is False:
            print('Connecting')
            self.connection = obd.Async("/dev/pts/3")

        self.start_watch_commands()
        self.connection.start()

    def start_watch_commands(self):
        for c in self.commands:
            self.connection.watch(eval(c), callback=self.logData)

    def logData(self, r):
        self.DataLogger.set_current_value(r.value.m, r.command.name)