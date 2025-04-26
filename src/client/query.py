import logging
from config.api import getNationalRailClient
from client.util import retry
import datetime
from client.train_service import (
    TrainServiceUpdate,
    TrainServiceCancellationData,
    TrainServiceDelayData,
    TrainServiceOnTimeData,
)


class NationalRailQuery(object):
    def __init__(self, services, serviceTimeframe=1800):
        self._services = services
        self._serviceTimeframe = serviceTimeframe
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
                        for (
                            callingPointList
                        ) in serviceItem.subsequentCallingPoints.callingPointList:
                            for callingPoint in callingPointList.callingPoint:
                                if callingPoint.crs == service.destination:
                                    return serviceItem

        return _queryNationalRail()

    def _getServicesToMonitor(self):
        return [
            service
            for service in self._services
            if service.isWithinTimeframe(self._serviceTimeframe)
        ]

    def _parseServiceData(self, serviceToMonitor, serviceData):
        if serviceData.etd == "Cancelled":
            data = TrainServiceCancellationData(cancelReason=serviceData.cancelReason)
        elif serviceData.etd == "On time":
            data = TrainServiceOnTimeData()
        elif serviceData.etd == "Delayed":
            data = TrainServiceDelayData(None, serviceData.delayReason)
        else:
            etd = datetime.datetime.strptime(serviceData.etd, "%H:%M")
            delay = etd - serviceToMonitor.scheduledTime
            if delay.seconds > (180):
                data = TrainServiceDelayData(delay.seconds, serviceData.delayReason)
            else:
                data = TrainServiceOnTimeData()

        update = TrainServiceUpdate(
            serviceData.std,
            serviceData.etd,
            serviceToMonitor.station,
            serviceToMonitor.destination,
            data,
        )
        return update

    def queryServices(self):
        ret = []
        for serviceToMonitor in self._getServicesToMonitor():
            logging.info(
                "[NationalRailQuery]: Querying for service: %s",
                serviceToMonitor.printInfo(),
            )
            serviceData = self._getDesiredServiceFromDepartureBoard(serviceToMonitor)
            if serviceData:
                parsedUpdate = self._parseServiceData(serviceToMonitor, serviceData)
                logging.info(
                    "[NationalRailQuery]: Parsed service update: %s",
                    parsedUpdate.printInfo(),
                )
                ret.append(parsedUpdate)
        return ret
