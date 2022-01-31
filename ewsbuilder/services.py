from .core import Core, etree


class Services(Core):

    def __init__(self, generate_strings=False) -> None:
        super().__init__()
        self.generate_strings = generate_strings

    def _make_element(self, element, value):
        namespace = self._get_namespace(value.attrs)
        element.append(namespace._makeelement(self._split(value.attrs['element'])))

    def generate(self, service):
        from .messages import Messages
        from .types import Types
        messages = Messages()
        types = Types()
        for descendent in service.descendants:
            if hasattr(descendent, 'attrs') and descendent.attrs.get('name') == 'request':
                parent = self.M_NAMESPACE.Body()
                self._make_element(parent, descendent)
                self.__logger.info(f"Processing Definition For: {self._split(descendent.attrs['element'])}")
                messages.element = descendent
                element_list = []
                for element in messages.element:
                    namespace = None
                    if element.get('type'):
                        namespace = self._get_namespace(element)
                        complex_types = types.find(attrs={'name': self._split(element.get('type'))})
                    else:
                        namespace = self._get_namespace(element.find('element'))
                        complex_types = types.find(attrs={'name': self._split(element.find('element').get('type'))})
                    if element.attrs.get('name') and element.attrs.get('name') not in element_list:
                        child = namespace._makeelement(element.attrs.get('name'))
                    if complex_types and complex_types is not None:
                        namespace = self._get_namespace(complex_types.find('element'))
                        if not namespace:
                            continue
                        if complex_types.find('element').get('name') and complex_types.find('element')['name'] not in element_list:
                            child.append(namespace._makeelement(complex_types.find('element')['name'], types.get_attribute(complex_types)))
                        for complex_type in complex_types.find_all('element'):
                            namespace = self._get_namespace(complex_type)
                            if complex_type.get('name'):
                                child.append(
                                    namespace._makeelement(
                                        complex_type['name'],
                                        types.get_attribute(complex_type)
                                        )
                                )
                        elements = types.get_element(complex_types)
                        if elements:
                            attribs_dict = {}
                            for elem in elements:
                                namespace = self._get_namespace(elem)
                                if elem.get('type'):
                                    temp = types.find(attrs={'name': elem['type']})
                                    if temp:
                                        attribs_dict.update(types.get_attribute(temp))
                                if complex_types.find('element').get('name'):
                                    child.find(
                                        complex_types.find('element')['name']
                                    ).append(
                                        namespace._makeelement(
                                            elem['name'], 
                                            attribs_dict
                                        )
                                    )
                    parent.find(self._split(descendent.attrs['element'])).append(child)
                if self.generate_strings:
                    return etree.tostring(parent, encoding='unicode')
                else:
                    return parent
