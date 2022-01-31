from .core import Core


class Messages(Core):

    def __init__(self) -> None:
        super().__init__()

    @property
    def element(self):
        return self.__element.previous_sibling.find_all('element')

    @element.setter
    def element(self, value):
        self.__element = self.messages.find(
            name='element', 
            attrs={'name': self._split(value.attrs['element'])}
        ).previous_sibling
