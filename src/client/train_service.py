import datetime
import pytz
from enum import Enum


class TrainServiceMonitorInstruction(object):
    def __init__(self, scheduledTimeStr, station, destination):
        self.scheduledTimeStr = scheduledTimeStr
        self.scheduledTime = datetime.datetime.strptime(scheduledTimeStr, "%H:%M")
        self.station = station
        self.destination = destination

    def __str__(self):
        return " ".join((self.scheduledTimeStr, self.station, self.destination))

    def printInfo(self):
        return "The %s service from %s to %s" % (
            self.scheduledTimeStr,
            self.station,
            self.destination,
        )

    def isWithinTimeframe(self, timeframe):
        now = datetime.datetime.now(pytz.timezone("Europe/London"))
        now = now.replace(tzinfo=None)
        return (self.scheduledTime - now).seconds < timeframe


class TrainServiceState(Enum):
    ON_TIME = "On Time"
    DELAYED = "Delayed"
    DELAYED_NO_ETD = "Delayed with no estimate"
    CANCELLED = "Cancelled"


class TrainServiceStateData(object):
    def state(self):
        return self.stateVal.value

    def _stateReason(self):
        return None

    def stateReason(self):
        return self._stateReason()


class TrainServiceOnTimeData(TrainServiceStateData):
    stateVal = TrainServiceState.ON_TIME


class TrainServiceDelayData(TrainServiceStateData):
    def __init__(self, delayEstimateSeconds, delayReason):
        self.delayEstimateSeconds = delayEstimateSeconds
        self.delayReason = delayReason

    def _stateReason(self):
        return self.delayReason

    def state(self):
        return (
            TrainServiceState.DELAYED.value
            + (" by %s minutes" % (self.delayEstimateSeconds // 60))
            if self.delayEstimateSeconds
            else TrainServiceState.DELAYED_NO_ETD.value
        )


class TrainServiceCancellationData(TrainServiceStateData):
    stateVal = TrainServiceState.CANCELLED

    def __init__(self, cancelReason):
        self.cancelReason = cancelReason

    def _stateReason(self):
        return self.cancelReason


class TrainServiceUpdate(object):
    def __init__(
        self,
        scheduledTimeStr,
        estimatedTimeStr,
        station,
        destination,
        stateData,
    ):
        self.scheduledTimeStr = scheduledTimeStr
        self.estimatedTimeStr = estimatedTimeStr
        self.stateData = stateData
        self.scheduledTime = datetime.datetime.strptime(scheduledTimeStr, "%H:%M")
        self.station = station
        self.destination = destination

    def __str__(self):
        return " ".join((self.scheduledTimeStr, self.station, self.destination))

    def printInfo(self):
        return "The %s service from %s to %s is %s" % (
            self.scheduledTimeStr,
            self.station,
            self.destination,
            self.stateData.state(),
        ) + (
            ", Reason: %s" % self.stateData.stateReason()
            if self.stateData.stateReason()
            else ""
        )
