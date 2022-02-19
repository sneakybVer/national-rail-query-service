from imghdr import tests
import unittest
from src.client.train_service import TrainService
import datetime


class TestTrainService(unittest.TestCase):
    def test_isWithinTimeframe_30minutes(self):

        # Setup test service scheduled for 35 minutes from now
        now = datetime.datetime.now()
        in35Mins = now + datetime.timedelta(seconds=2100)
        testService = TrainService(in35Mins.strftime("%H:%M"), "SVG", "KGX")

        # Outside of 30 min timeframe
        self.assertFalse(testService.isWithinTimeframe(1800))

        # But is within 40 min
        self.assertTrue(testService.isWithinTimeframe(2400))

    def test_canPrintService(self):
        testService = TrainService("08:42", "SVG", "KGX")
        self.assertTrue(str(testService))
        self.assertIsInstance(testService.printInfo(), str)
