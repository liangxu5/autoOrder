import asyncio
import time
from unicodedata import decimal

from loguru import logger

from aevo import AevoClient


async def main():
    # The following values which are used for authentication on private endpoints, can be retrieved from the Aevo UI
    aevo = AevoClient(
        signing_key="",
        wallet_address="",
        api_key="",
        api_secret="",
        env="mainnet",
    )

    if not aevo.signing_key:
        raise Exception(
            "Signing key is not set. Please set the signing key in the AevoClient constructor."
        )

    logger.info("Creating order...")
    while True:
        time.sleep(5)
        # 1. 获取钱包余额
        b = aevo.rest_get_account()
        equity = b["equity"]
        logger.info("钱包余额为：" + equity)
        # 2. 开仓
        markets = aevo.get_markets("BNB")
        price = markets[0]["index_price"]
        quantity = round(float(equity) / float(price), 2)
        if float(equity) < 9:
            return
        response1 = aevo.rest_create_market_order(
            instrument_id=4042,
            is_buy=True,
            quantity=quantity,
        )
        logger.info(response1)
        # 3. 关仓
        time.sleep(2)
        response2 = aevo.rest_create_market_order(
            instrument_id=4042,
            is_buy=False,
            quantity=quantity,
        )
        logger.info(response2)


if __name__ == "__main__":
    asyncio.run(main())
