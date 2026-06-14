import asyncio
from datetime import datetime
from typing import Any, Dict, List

import ib_insync

from utils.settings import Settings


class Botconnector(object):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.ib = ib_insync.IB()

    async def connect(self):
        """Asynchronously connect to IBKR Gateway or TWS."""
        try:
            await self.ib.connectAsync(
                self.settings.host,
                self.settings.port,
                clientId=self.settings.client_id,
                timeout=self.settings.timeout,
            )
            print(
                f"Connected to IBKR at {self.settings.host}:{self.settings.port} "
                f"with client ID {self.settings.client_id}."
            )
        except Exception as e:
            print(f"Failed to connect to IBKR: {e}")
            raise

    async def disconnect(self):
        """Asynchronously disconnect from IBKR."""
        if self.ib.isConnected():
            self.ib.disconnect()
            await asyncio.sleep(0.1)
            print("Disconnected from IBKR.")
        else:
            print("Not connected to IBKR.")

    def is_connected(self) -> bool:
        return self.ib.isConnected()

    def get_positions(self) -> List[Dict[str, Any]]:
        positions = self.ib.positions()
        serialized_positions: List[Dict[str, Any]] = []

        for position in positions:
            serialized_positions.append(
                {
                    "account": position.account,
                    "symbol": position.contract.symbol,
                    "secType": position.contract.secType,
                    "exchange": position.contract.exchange,
                    "currency": position.contract.currency,
                    "quantity": position.position,
                    "average_cost": position.avgCost,
                }
            )

        return serialized_positions

    async def get_total_unrealized_gain_loss(self) -> float:
        account_summary = await self.ib.accountSummaryAsync()
        unrealized_values: List[float] = []

        for item in account_summary:
            if item.tag != "UnrealizedPnL" or item.currency != "BASE":
                continue

            try:
                unrealized_values.append(float(item.value))
            except (TypeError, ValueError):
                continue

        return sum(unrealized_values)

    async def get_account_snapshot(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "connected": self.is_connected(),
            "positions": self.get_positions(),
            "total_unrealized_gain_loss": await self.get_total_unrealized_gain_loss(),
        }

    