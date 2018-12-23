"""
A device represents the superclass of any device, which can be controlled
by this small application.
"""

class Device():
    def __init__(self, name: str):
        self.__name = name
    
    def getName(self):
        return self.__name

    def setName(self, newName: str):
        self.__name = newName

    name = property(getName, setName)

    def turnOn(self):
        raise NotImplementedError('The devices subclass has to implement this function')

    def turnOff(self):
        raise NotImplementedError('The devices subclass has to implement this function')
