class DataLogger:

    CurrentValues = {}
    AvailableCommands = []
    DataBatch = {'data': []}

    def set_current_value(self, data, DataType):
        if DataType not in self.AvailableCommands:
            self.AvailableCommands.append(DataType)

        self.CurrentValues[DataType] = data

    def get_current_value(self, DataType):
        if DataType in self.CurrentValues:
            if self.CurrentValues[DataType]:
                return self.CurrentValues[DataType]
        return 'N/A'

    def add_data_batch(self, data, DataType, vehicleId, dateTime):
        if vehicleId is not None:
            tempData = {
                "data_type": DataType.lower(),
                "vehicle_id": vehicleId,
                "value": data,
                "date": dateTime
            }

            self.DataBatch["data"].append(tempData)

    def get_current_data_batch(self):
        return self.DataBatch

    def set_empty_data_batch(self):
        self.DataBatch = {'data': []}
