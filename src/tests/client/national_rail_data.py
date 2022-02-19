""" Module providing mock data representing the data structure returned by the national rail client """

import datetime


class MockNationalRailResponse(object):
    def __init__(self, trainServices):
        self.trainServices = trainServices


class MockNationalRailTrainServices(object):
    def __init__(self, service):
        self.service = service


class MockNationalRailTrainService(object):
    def __init__(self, std, destination, etd, delayReason=None):
        self.std = std
        self.destination = destination
        self.etd = etd
        self.delayReason = delayReason


class MockNationalRailDestination(object):
    def __init__(self, location):
        self.location = location


class MockNationalRailLocation(object):
    def __init__(self, crs):
        self.crs = crs


def setUpOnTimeService(std, destination):
    return MockNationalRailResponse(
        MockNationalRailTrainServices(
            [
                MockNationalRailTrainService(
                    std,
                    MockNationalRailDestination(
                        [MockNationalRailLocation(destination)]
                    ),
                    std,
                )
            ]
        ),
    )


def setUpDelayedService(std, destination):
    return MockNationalRailResponse(
        MockNationalRailTrainServices(
            [
                MockNationalRailTrainService(
                    std,
                    MockNationalRailDestination(
                        [MockNationalRailLocation(destination)]
                    ),
                    (
                        datetime.datetime.strptime(std, "%H:%M")
                        + datetime.timedelta(seconds=2000)
                    ).strftime("%H:%M"),
                    delayReason="Slight breeze",
                )
            ]
        ),
    )
