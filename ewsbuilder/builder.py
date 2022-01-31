import os
import json
from pick import pick
from .services import Services


class Builder:

    __title = "Please select 'All' or specific services to generate"
    __service_names = []
    services = Services().services

    def __init__(self) -> None:
        if not self.__service_names:
            self.__get_service_names()

    def __pick(self):
        option = pick(self.__service_names, self.__title, multi_select=True)
        return option

    def __get_service_names(self):
        self.__service_names = ['All']
        for service in self.services.find_all('message'):
            if 'SoapIn' in service.get('name'):
                self.__service_names.append(service['name'].split('SoapIn')[0])

    def __build_envelope(self, header, body, generate_strings=False):
        from lxml import etree
        ENVELOPE = Services.SOAP_MESSAGE_ELEMENT.Envelope
        self.envelope = ENVELOPE(
            header,
            body
        )
        if generate_strings:
            return etree.tostring(self.envelope, encoding='unicode')
        else:
            return self.envelope

    def __get_absolute_path(self, value):
        return os.path.abspath(
            os.path.expanduser(
                os.path.expandvars(value)
            )
        )

    def __save_soap(self, path, name, data):
        from lxml import etree
        full_path = self.__get_absolute_path(os.path.join(self.__get_absolute_path(path), name + '.xml'))
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))
        et = etree.ElementTree(data)
        et.write(full_path, pretty_print=True, xml_declaration=True,   encoding="utf-8")

    def build(self, service_name=None, generate_strings=False, output=None):
        if not service_name:
            pick_list = self.__pick()
            options = [i[0] for i in pick_list]
        else:
            options = service_name if isinstance(service_name, list) else [service_name]
        return_list = []
        if 'All' in options or len(options) == 0:
            for name in self.__service_names:
                data = self.__build(service_name=name, generate_strings=generate_strings)
                if output:
                    self.__save_soap(output, name, data)
                else:
                    return_list.append(data)
        else:
            for name in options:
                data = self.__build(service_name=name, generate_strings=generate_strings)
                if output:
                    self.__save_soap(output, name, data)
                else:
                    return_list.append(data)
        return return_list
    
    def __build(self, service_name=None, generate_strings=False):
        from .headers import Headers
        for service in self.services.find_all('message'):
            if 'SoapIn' in service.get('name'):
                if service_name and service_name == service.get('name').split('Soap')[0]:
                    headers = Headers().generate(service)
                    body = Services().generate(service)
                    return self.__build_envelope(headers, body, generate_strings=generate_strings)
