import os
from bs4 import BeautifulSoup
from lxml.builder import ElementMaker
from lxml import etree
from .utils.logger import LoggingBase


class Core(metaclass=LoggingBase):

    services = None
    messages = None
    types = None
    NAMESPACE_MAP = {
        'soap': "http://schemas.xmlsoap.org/soap/envelope/", 
        'm': "http://schemas.microsoft.com/exchange/services/2006/messages", 
        't': "http://schemas.microsoft.com/exchange/services/2006/types", 
        'a': "http://schemas.microsoft.com/exchange/2010/Autodiscover",
    }
    SOAP_MESSAGE_ELEMENT = ElementMaker(
        namespace=NAMESPACE_MAP['soap'],
        nsmap={
            'soap': NAMESPACE_MAP['soap'], 
            'm': NAMESPACE_MAP['m'], 
            't': NAMESPACE_MAP['t']
        }
    )
    SOAP_NAMESPACE = ElementMaker(namespace=NAMESPACE_MAP['soap'],nsmap={'soap': "http://schemas.xmlsoap.org/soap/envelope/"})
    M_NAMESPACE =  ElementMaker(namespace=NAMESPACE_MAP['m'],nsmap={'m': "http://schemas.microsoft.com/exchange/services/2006/messages"})
    T_NAMESPACE = ElementMaker(namespace=NAMESPACE_MAP['t'], nsmap={'t': "http://schemas.microsoft.com/exchange/services/2006/types"})

    def __init__(self) -> None:
        path = os.path.abspath(os.path.dirname(__file__))
        if not Core.services:
            Core.services = BeautifulSoup(
            open(os.path.join(path, 'data', 'services.wsdl'), 'rb').read(), 'xml'
        )
        if not Core.messages:
            Core.messages = BeautifulSoup(
                open(os.path.join(path, 'data', Core.services.find_all('import')[0]['schemaLocation']), 'rb').read(), 'xml'
            )
        if not Core.types:
            Core.types = BeautifulSoup(
                open(os.path.join(path, 'data', Core.messages.find_all('import')[0]['schemaLocation']), 'rb').read(), 'xml'
            )

    @staticmethod
    def _get_namespace(value):
        if value:
            if value.get('type'):
                value = value['type'].split(':')[0]
            elif value.get('element'):
                value = value['element'].split(':')[0]
            if value == 't' or value == 'tns':
                return Core.T_NAMESPACE
            elif value == 'm':
                return Core.M_NAMESPACE
            else:
                return Core.M_NAMESPACE
        return None

    @staticmethod
    def _split(value):
        return value.split(':')[-1]
