import os 
from utils.utils import json2dict

class Settings(object):
    def __init__(self, input_json_path, **kwargs):
        self.settings = json2dict(os.path.join(input_json_path, 'ibbotsettings.json'))
        self.host = self.settings.get('host', 'localhost')
        self.port = self.settings.get('port', 7497)
        self.client_id = self.settings.get('client_id', 1)
        self.timeout = self.settings.get('timeout', 10)
