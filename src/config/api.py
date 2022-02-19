import logging
from suds.client import Client
from suds.sax.element import Element


def getNationalRailDarwinConfig():
    from national_rail import DARWIN_WEBSERVICE_NAMESPACE, DARWIN_TOKEN

    return DARWIN_WEBSERVICE_NAMESPACE, DARWIN_TOKEN


def getLDBWSConfig():
    from national_rail import LDBWS_URL

    return LDBWS_URL


def getNationalRailClient():
    logging.info("Setting up national rail client")
    ns, token = getNationalRailDarwinConfig()
    tokenElement = Element("AccessToken", ns=ns)
    tokenVal = Element("TokenValue", ns=ns)
    tokenVal.setText(token)
    tokenElement.append(tokenVal)
    client = Client(getLDBWSConfig())
    client.set_options(soapheaders=token)
