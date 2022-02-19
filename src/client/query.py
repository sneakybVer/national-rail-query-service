import logging
from src.config.api import getNationalRailClient
from src.client.util import retry, runForever
import datetime
import pytz
import time


class NationalRailQuery(object):
    def __init__(self, services):
        self._services = services
        self._serviceTimeframe = 1800
        self._setupNationalRailClient()

    def _setupNationalRailClient(self):
        self.nationalRailClient = getNationalRailClient()

    def _getDesiredServiceFromDepartureBoard(self, service):
        @retry(self._setupNationalRailClient)
        def _queryNationalRail():
            depBoard = self.nationalRailClient.service.GetDepBoardWithDetails(
                10, service.station, service.destination, None, None, None
            )
            if depBoard:
                for serviceItem in depBoard.trainServices.service:
                    if serviceItem.std == service.scheduledTimeStr:
                        for serviceLocation in serviceItem.destination.location:
                            if serviceLocation.crs == service.destination:
                                return serviceItem

        return _queryNationalRail()

    def _getServicesToMonitor(self):
        return [
            service
            for service in self._services
            if service.isWithinTimeframe(self._serviceTimeframe)
        ]

    def _publishServiceData(self, service):
        data = self._getDesiredServiceFromDepartureBoard(service)
        # Log data for now during testing
        logging.info("Service data found: %s", data)

    def _queryServices(self):
        for service in self._getServicesToMonitor():
            self._publishServiceData(service)

    def queryServices(self):
        runForever(self._queryServices, self.interval)
