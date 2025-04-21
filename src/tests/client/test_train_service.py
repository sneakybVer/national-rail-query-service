import unittest
from src.client.train_service import (
    TrainServiceMonitorInstruction,
    TrainServiceUpdate,
    TrainServiceCancellationData,
    TrainServiceDelayData,
)
import datetime


class TestTrainServiceMonitorInstruction(unittest.TestCase):
    def test_isWithinTimeframe_30minutes(self):

        # Setup test service scheduled for 35 minutes from now
        now = datetime.datetime.now()
        in35Mins = now + datetime.timedelta(seconds=2100)
        testService = TrainServiceMonitorInstruction(
            in35Mins.strftime("%H:%M"), "SVG", "KGX"
        )

        # Outside of 30 min timeframe
        self.assertFalse(testService.isWithinTimeframe(1800))

        # But is within 40 min
        self.assertTrue(testService.isWithinTimeframe(2400))

    def test_canPrintService(self):
        testService = TrainServiceMonitorInstruction("08:42", "SVG", "KGX")
        self.assertTrue(str(testService))
        self.assertIsInstance(testService.printInfo(), str)


class TestTrainServiceUpdate(unittest.TestCase):
    def test_CancelledUpdate(self):
        update = TrainServiceUpdate(
            "08:42",
            None,
            "KGX",
            "SVG",
            TrainServiceCancellationData("There was a slight breeze"),
        )
        self.assertIsInstance(update.printInfo(), str)
        self.assertIn("There was a slight breeze", update.printInfo())

    def test_DelayedUpate(self):
        update = TrainServiceUpdate(
            "08:42",
            "08:50",
            "KGX",
            "SVG",
            TrainServiceDelayData(480, "There was yet another signalling failure"),
        )
        self.assertIsInstance(update.printInfo(), str)
        self.assertIn("There was yet another signalling failure", update.printInfo())
        self.assertIn("by 8 minutes", update.printInfo())
