import ib_insync
import sys
import os

from utils.settings import Settings

class Botconnector(object):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.ib = ib_insync.IB()
        self.connect()

    def connect(self):
        try:
            self.ib.connect(self.settings.host, self.settings.port, clientId=self.settings.client_id, timeout=self.settings.timeout)
            print(f"Connected to IB at {self.settings.host}:{self.settings.port} with client ID {self.settings.client_id} and timeout {self.settings.timeout} seconds.")
        except Exception as e:
            print(f"Failed to connect to IB: {e}")
    
    def disconnect(self):
        if self.ib.isConnected():
            self.ib.disconnect()
            print("Disconnected from IB.")
        else:
            print("Not connected to IB.")

    