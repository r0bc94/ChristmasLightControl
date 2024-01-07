"""
A device represents the superclass of any device, which can be controlled
by this small application.
"""

class Device():
    def __init__(self, name: str, friendlyName: str = ''):
        self.__name = name
        self.__friendlyName = friendlyName
    
    def getName(self):
        return self.__name

    def setName(self, newName: str):
        self.__name = newName

    def getFriendlyName(self):
        return self.__friendlyName
    
    def setFriendlyName(self, newFriendlyName: str):
        self.__friendlyName = newFriendlyName

    name = property(getName, setName)
    friendlyName = property(getFriendlyName, setFriendlyName)

    def turnOn(self):
        raise NotImplementedError('The devices subclass has to implement this function')

    def turnOff(self):
        raise NotImplementedError('The devices subclass has to implement this function')
