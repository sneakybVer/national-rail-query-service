import datetime
import pytz


class TrainService(object):
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
