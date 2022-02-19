from src.client.query import NationalRailQuery
from src.client.publisher import TrainServiceUpdatePublisher
import time

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def _runApp(query, publisher):
    while 1:
        updates = query.queryServices()
        publisher.publishUpdates(updates)
        logging.info("Sleeping...")
        time.sleep(300)


# For dev testing purposes hardcode the services here
from src.client.train_service import TrainServiceMonitorInstruction

TEST_SERVICES = [TrainServiceMonitorInstruction("22:47", "SVG", "LBG")]
TEST_TIMEFRAME = 86400


def devTestApp():
    query = NationalRailQuery(TEST_SERVICES, serviceTimeframe=TEST_TIMEFRAME)
    publisher = TrainServiceUpdatePublisher()
    _runApp(query, publisher)


def run():
    devTestApp()


if __name__ == "__main__":
    run()
