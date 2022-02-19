import unittest
from src.client.query import NationalRailQuery
from src.client.train_service import TrainService
import mock


class TestNationalRailQuery(unittest.TestCase):
    def setUp(self):
        self.nationalRailMock = mock.MagicMock()
        mock.patch(
            "src.client.query.getNationalRailClient", return_value=self.nationalRailMock
        ).__enter__()

        testService1 = TrainService("08:42", "SVG", "KGX")
        testService1.isWithinTimeframe = lambda *args, **kwargs: True
        self.testClient = NationalRailQuery([testService1])

    def test__queryServices(self):
        self.testClient._queryServices()
        self.nationalRailMock.service.GetDepBoardWithDetails.assert_called_once()
