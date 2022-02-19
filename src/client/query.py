from suds.client import Client
from suds.sax.element import Element
import logging
from config import DARWIN_WEBSERVICE_NAMESPACE, DARWIN_TOKEN, LDBWS_URL
from util import retry
import datetime
import pytz
import time


class NationalRailQuery(object):
    def __init__(self, services):
        self._services = services
        self._serviceTimeframe = 1800

    def _setupNationalRailClient(self):
        logging.info("Setting up national rail client")
        token = Element("AccessToken", ns=DARWIN_WEBSERVICE_NAMESPACE)
        val = Element("TokenValue", ns=DARWIN_WEBSERVICE_NAMESPACE)
        val.setText(DARWIN_TOKEN)
        token.append(val)
        client = Client(LDBWS_URL)
        client.set_options(soapheaders=token)
        self.nationalRailClient = client

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

    def queryServices(self):
        while 1:
            for service in self._getServicesToMonitor():
                self._publishServiceData(service)
            time.sleep(self.interval)
