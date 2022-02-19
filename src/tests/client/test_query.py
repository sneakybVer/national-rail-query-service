import unittest
from src.client.query import NationalRailQuery
from src.client.train_service import TrainService
import mock


class TestNationalRailQuery(unittest.TestCase):
    def setUp(self):
        self.nationalRailMock = mock.MagicMock()
        mock.patch(
            "src.config.api.getNationalRailClient", return_value=self.nationalRailMock
        )

        testService1 = TrainService("08:42", "SVG", "KGX")
        self.testClient = NationalRailQuery([testService1])

    def test__queryServices(self):
        self.testClient._queryServices()
        self.nationalRailMock.assert_called_once()
