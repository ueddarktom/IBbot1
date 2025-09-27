import os, sys
import argparse

import ibconnection.connector as ibc
from utils.settings import Settings


root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

settings=Settings(root_folder)


class Executor(object):
    def __init__(self, settings: Settings, experiment_name= None):
        self.settings = settings
        self.experiment_name = experiment_name


    def run(self):
        print(f"Running experiment: {self.experiment_name} with settings: {self.settings.__dict__}")
        link = ibc.Botconnector(self.settings)
        position=link.ib.positions()
        print(position)

        accountval=[v for v in link.ib.accountValues() if v.tag == 'NetLiquidationByCurrency' and v.currency == 'BASE']
        print(f"Net Liquidation Value: {accountval}")

        from ib_insync import Stock
        contract = Stock('TSLA', 'SMART', 'USD')
        temp=link.ib.reqContractDetails(contract)
        print(f"Contract Details: {temp}")

        link.ib.disconnect()




if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='IBbot Main Script')
    # parser.add_argument("--experiment", type=str, help="Name of the experiment to run")
    # args= parser.parse_args()


    executor= Executor(settings)
    executor.run()