class DataLogger:

    current_values = {}

    def set_current_value(self, data, data_type):
        self.current_values[data_type] = data

    def get_current_value(self, data_type):
        if data_type in self.current_values:
            if self.current_values[data_type]:
                return self.current_values[data_type]
        return 'N/A'