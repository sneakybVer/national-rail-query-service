from src.client.query import NationalRailQuery
from src.client.publisher import TrainServiceUpdatePublisher
import time


def run():
    query = NationalRailQuery([])
    publisher = TrainServiceUpdatePublisher()
    while 1:
        updates = query.queryServices()
        publisher.publishUpdates(updates)
        time.sleep(1)
