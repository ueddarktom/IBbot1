import asyncio
import os
from typing import Any, Dict, Optional

import ibconnection.connector as ibc
from utils.settings import Settings


STATUS_INTERVAL_SECONDS = 10 * 60

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
settings = Settings(root_folder)


class Executor(object):
    def __init__(self, settings: Settings, experiment_name: Optional[str] = None):
        self.settings = settings
        self.experiment_name = experiment_name or "IB account monitor"
        self.link = ibc.Botconnector(self.settings)

    def _print_status(self, snapshot: Dict[str, Any]) -> None:
        print(f"[{snapshot['timestamp']}] {self.experiment_name}")
        print(f"Connected to IBKR: {snapshot['connected']}")
        print(
            "Total Unrealized Gain/Loss: "
            f"{snapshot['total_unrealized_gain_loss']:.2f}"
        )

        if snapshot["positions"]:
            print("Open Positions:")
            for position in snapshot["positions"]:
                print(
                    "  "
                    f"{position['symbol']} "
                    f"({position['secType']} @ {position['exchange']}) | "
                    f"qty={position['quantity']} | "
                    f"avg_cost={position['average_cost']} {position['currency']}"
                )
        else:
            print("Open Positions: none")

        print(f"Next update in {STATUS_INTERVAL_SECONDS // 60} minutes.\n")

    async def run(self):
        print(f"Starting {self.experiment_name}.")
        await self.link.connect()

        try:
            while True:
                snapshot = await self.link.get_account_snapshot()
                self._print_status(snapshot)
                await asyncio.sleep(STATUS_INTERVAL_SECONDS)
        except asyncio.CancelledError:
            raise
        finally:
            await self.link.disconnect()


if __name__ == '__main__':
    executor = Executor(settings, experiment_name="Production IB Monitor")

    try:
        asyncio.run(executor.run())
    except KeyboardInterrupt:
        print("IB account monitor stopped by user.")