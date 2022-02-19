import unittest
from src.client.query import NationalRailQuery
from src.client.train_service import TrainServiceMonitorInstruction, TrainServiceState
import mock
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


class TestNationalRailQuery(unittest.TestCase):
    def setUp(self):
        self.nationalRailMock = mock.MagicMock()
        mock.patch(
            "src.client.query.getNationalRailClient", return_value=self.nationalRailMock
        ).__enter__()

        testService1 = TrainServiceMonitorInstruction("08:42", "SVG", "KGX")
        testService1.isWithinTimeframe = lambda *args, **kwargs: True
        self.testClient = NationalRailQuery([testService1])

    def _setUpOnTimeService(self, std, destination):
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

    def _setUpDelayedService(self, std, destination):
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

    def test__queryServices(self):
        self.nationalRailMock.service.GetDepBoardWithDetails.return_value = (
            self._setUpOnTimeService("08:42", "KGX")
        )

        results = self.testClient._queryServices()
        self.nationalRailMock.service.GetDepBoardWithDetails.assert_called_once()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].stateData.state(), TrainServiceState.ON_TIME.value)

    def test_delayedService(self):
        self.nationalRailMock.service.GetDepBoardWithDetails.return_value = (
            self._setUpDelayedService("08:42", "KGX")
        )
        results = self.testClient._queryServices()
        self.nationalRailMock.service.GetDepBoardWithDetails.assert_called_once()

        self.assertEqual(len(results), 1)
        self.assertIn(
            TrainServiceState.DELAYED.value,
            results[0].stateData.state(),
        )
        self.assertEqual(results[0].stateData.stateReason(), "Slight breeze")
