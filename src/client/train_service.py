import datetime
import pytz


class TrainService(object):
    def isWithinTimeframe(self, timeframe):
        now = datetime.datetime.now(pytz.timezone("Europe/London"))
        now = now.replace(tzinfo=None)
        return (self.scheduledTime - now).seconds < timeframe
