import unittest
from src.client.query import NationalRailQuery
from src.client.train_service import TrainServiceMonitorInstruction, TrainServiceState
import mock
from tests.client.national_rail_data import setUpDelayedService, setUpOnTimeService


class TestNationalRailQueryNonFunctionals(unittest.TestCase):
    def test_failedConnection(self):
        nationalRailMock = mock.MagicMock()
        with mock.patch(
            "src.client.query.getNationalRailClient", return_value=nationalRailMock
        ) as getClientMock:
            testQuery = NationalRailQuery([])
            getClientMock.assert_called_once()

            getClientMock.service.GetDepBoardWithDetails.side_effect = RuntimeError()

            with self.assertRaisesRegexp(RuntimeError, "Retries exceeded"):
                testQuery._getDesiredServiceFromDepartureBoard(None)

            # we retry twice then fail
            self.assertEqual(getClientMock.call_count, 3)


class TestNationalRailQuery(unittest.TestCase):
    def setUp(self):
        self.nationalRailMock = mock.MagicMock()
        mock.patch(
            "src.client.query.getNationalRailClient", return_value=self.nationalRailMock
        ).__enter__()

        testService1 = TrainServiceMonitorInstruction("08:42", "SVG", "KGX")
        testService1.isWithinTimeframe = lambda *args, **kwargs: True
        self.testClient = NationalRailQuery([testService1])

    def test__queryServices(self):
        self.nationalRailMock.service.GetDepBoardWithDetails.return_value = (
            setUpOnTimeService("08:42", "KGX")
        )

        results = self.testClient.queryServices()
        self.nationalRailMock.service.GetDepBoardWithDetails.assert_called_once()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].stateData.state(), TrainServiceState.ON_TIME.value)

    def test__queryServices_callingPoint(self):
        # Setup a service which finishes in Horsham but calls at Kings Cross
        self.nationalRailMock.service.GetDepBoardWithDetails.return_value = (
            setUpOnTimeService("08:42", "HRH", "KGX")
        )

        results = self.testClient.queryServices()
        self.nationalRailMock.service.GetDepBoardWithDetails.assert_called_once()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].stateData.state(), TrainServiceState.ON_TIME.value)

    def test_delayedService(self):
        self.nationalRailMock.service.GetDepBoardWithDetails.return_value = (
            setUpDelayedService("08:42", "KGX")
        )
        results = self.testClient.queryServices()
        self.nationalRailMock.service.GetDepBoardWithDetails.assert_called_once()

        self.assertEqual(len(results), 1)
        self.assertIn(
            TrainServiceState.DELAYED.value,
            results[0].stateData.state(),
        )
        self.assertEqual(results[0].stateData.stateReason(), "Slight breeze")
