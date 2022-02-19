""" Module providing mock data representing the data structure returned by the national rail client """

import datetime


class MockNationalRailResponse(object):
    def __init__(self, trainServices):
        self.trainServices = trainServices


class MockNationalRailTrainServices(object):
    def __init__(self, service):
        self.service = service


class MockNationalRailTrainService(object):
    def __init__(
        self, std, destination, etd, delayReason=None, subsequentCallingPoints=None
    ):
        self.std = std
        self.destination = destination
        self.etd = etd
        self.delayReason = delayReason
        self.subsequentCallingPoints = subsequentCallingPoints


class MockNationalRailDestination(object):
    def __init__(self, location):
        self.location = location


class MockNationalRailSubsequentCallingPoints(object):
    def __init__(self, callingPointList):
        self.callingPointList = [callingPointList]


class MockNationalRailCallingPointList(object):
    def __init__(self, callingPoint):
        self.callingPoint = callingPoint


class MockNationalRailCallingPoint(object):
    def __init__(self, crs):
        self.crs = crs


class MockNationalRailLocation(object):
    def __init__(self, crs):
        self.crs = crs


def setUpOnTimeService(std, destination=None, callingPoint=None):
    return MockNationalRailResponse(
        MockNationalRailTrainServices(
            [
                MockNationalRailTrainService(
                    std,
                    MockNationalRailDestination(
                        [MockNationalRailLocation(destination)]
                    ),
                    std,
                    subsequentCallingPoints=MockNationalRailSubsequentCallingPoints(
                        MockNationalRailCallingPointList(
                            [MockNationalRailCallingPoint(callingPoint)]
                        )
                    ),
                )
            ]
        ),
    )


def setUpDelayedService(std, destination=None, callingPoint=None):
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
                    subsequentCallingPoints=MockNationalRailSubsequentCallingPoints(
                        MockNationalRailCallingPointList(
                            [MockNationalRailCallingPoint(callingPoint)]
                        )
                    ),
                )
            ]
        ),
    )
