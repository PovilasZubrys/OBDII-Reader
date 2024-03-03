import secrets
import json


class FirstRunSetup:

    def setup(self, data):
        authentication_token = self.generate_authentication_token()
        self.save_data(data, authentication_token)

    def generate_authentication_token(self):
        return secrets.token_hex(125)

    def save_data(self, data, authentication_token):
        data['first_run'] = False
        data['authentication_token'] = authentication_token

        with open('config/Settings.json', 'w') as f:
            json.dump(data, f)