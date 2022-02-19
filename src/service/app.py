from src.client.query import NationalRailQuery
from src.client.publisher import TrainServiceUpdatePublisher
import time


def _runApp(query, publisher):
    while 1:
        updates = query.queryServices()
        publisher.publishUpdates(updates)
        time.sleep(1)


# For dev testing purposes hardcode the services here
from src.client.train_service import TrainServiceMonitorInstruction

TEST_SERVICES = [TrainServiceMonitorInstruction("08:02", "SVG", "LBG")]
TEST_TIMEFRAME = 86400


def devTestApp():
    query = NationalRailQuery(TEST_SERVICES, serviceTimeframe=TEST_TIMEFRAME)
    publisher = TrainServiceUpdatePublisher()
    _runApp(query, publisher)
