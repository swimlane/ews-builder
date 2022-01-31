from .core import Core, BeautifulSoup


class Types(Core):

    def __init__(self) -> None:
        super().__init__()
        self.complex_type_control_list = []
        self.element_return_list = []

    def get_element(self, complex_type):
        return_list = []
        for element in complex_type.find_all('element'):
            if element.get('name') and element.get('type'):
                if element not in self.element_return_list:
                    self.element_return_list.append(element)
                if element.get('type'):
                    self.__logger.debug(f"    Processing Element Type: {element['type']}")
                    if element['type'] not in self.complex_type_control_list:
                        self.complex_type_control_list.append(element['type'])
                        temp_complex_type = self.find(attrs={'name': self._split(element['type'])}, recurse=True)
                        if temp_complex_type:
                            self.element_return_list.extend(temp_complex_type)
                            return_list.extend(temp_complex_type)
                        else:
                            self.element_return_list.append(element)
                            return_list.append(element)
                else:
                    return_list.append(element)
        return return_list

    def find(self, name='complexType', attrs=None, recurse=False):
        for complex_type in self.types.find_all(name=name, attrs=attrs):
            if recurse:
                return self.get_element(complex_type)
            return complex_type

    def get_attribute(self, complex_type):
        return_dict = {}
        for attr in complex_type.find_all('attribute'):
            if attr:
                if attr.attrs.get('name'):
                    if attr.attrs['name'] not in return_dict:
                        return_dict[attr.attrs['name']] = None
                    return_dict[attr.attrs['name']] = attr.attrs.get('use', ' ')
        return return_dict
