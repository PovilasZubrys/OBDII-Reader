class DataLogger:

    CurrentValues = {}
    AvailableCommands = []

    def set_current_value(self, data, DataType):
        if DataType not in self.AvailableCommands:
            self.AvailableCommands.append(DataType)

        self.CurrentValues[DataType] = data

    def get_current_value(self, DataType):
        if DataType in self.CurrentValues:
            if self.CurrentValues[DataType]:
                return self.CurrentValues[DataType]
        return 'N/A'