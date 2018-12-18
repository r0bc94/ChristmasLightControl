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
