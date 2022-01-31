from .core import Core, etree


class Headers(Core):

    __enumerations = {}
    __endpoint_list = []
    __parent = None

    def __init__(self, generate_strings=False) -> None:
        super().__init__()
        self.generate_strings = generate_strings

    def generate(self, service):
        child = None
        if service.get('name').split('Soap')[0] not in self.__endpoint_list:
            self.__endpoint_list.append(service.get('name').split('Soap')[0])
            self.__logger.info(f"Generating Headers for {service.get('name').split('Soap')[0]}")
            self.__parent = self.SOAP_NAMESPACE.Header()
            for header in service.find_all('part'):
                if header.get('name') != 'request':
                    element = self.__find_element(self._split(header['element']))
                    if isinstance(element, dict):
                        temp_dict = {}
                        for key,val in element.items():
                            temp_dict[key] = ','.join([v for v in val.get('enumeration')])
                        child = self.T_NAMESPACE._makeelement(self._split(header['element']), temp_dict)
                    elif not isinstance(element, dict) and element is not None:
                        child = self.T_NAMESPACE._makeelement(self._split(header['element']))
                        child.append(element)
                    self.__parent.append(child)
            if self.generate_strings:
                return etree.tostring(self.__parent)
            else:
                return self.__parent

    def __get_simple_type(self, value):
        return_dict = {}
        for type in self.types.find_all(name='simpleType', attrs={'name': value.split(':')[-1]}):
            for item in type.find_all('enumeration'):
                if 'enumeration' not in return_dict:
                    return_dict['enumeration'] = []
                return_dict['enumeration'].append(item['value'])
        return return_dict

    def __get_element(self, value):
        for element in self.types.find_all(name='element', attrs={'name': value.split(':')[-1]}):
            return element

    def __get_complex_type(self, value):
        return_dict = {}
        attribute_dict = {}
        enum_list = []
        child = None
        for type in self.types.find_all(name='complexType', attrs={'name': value.split(':')[-1]}):
            for attribute in type.find_all(name='attribute'):
                if attribute.get('type'):
                    enum = self.__get_simple_type(attribute['type'])
                    if enum:
                        enum_list.extend(enum.get('enumeration'))
                attribute_dict[attribute['name']] = attribute.get('use') if attribute.get('use') else ''
            if enum_list:
                return_dict['enumeration'] = enum_list
            if not type.find_all(name='element'):
                child = self.T_NAMESPACE._makeelement(type['name'])
            for element in type.find_all(name='element'):
                if element.get('type') and element.get('type').startswith('t'):
                    child = self.T_NAMESPACE._makeelement(element['name'], attribute_dict)
                    complex_type = self.__get_complex_type(element['type'])
                    if complex_type is not None:
                        child.append(complex_type)
                elif element.get('ref'):
                    child = self.T_NAMESPACE._makeelement(self._split(element['ref']))
                    complex_type = self.__get_complex_type(self.__get_element(element['ref'])['type'])
                    if complex_type is not None:
                        child.append(complex_type)
        return child

    def __find_element(self, value):
        for type in self.types.find_all(name='element', attrs={'name': value}):
            if type.find('complexType'):
                for attribute in type.find_all(name='attribute'):
                    if attribute.get('type') and attribute.get('type').startswith('t'):
                        return {attribute.get('name'): self.__get_simple_type(attribute['type'])}
            elif type.get('type'):
                return self.__get_complex_type(type['type'])
