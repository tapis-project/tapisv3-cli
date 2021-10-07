from abc import ABC, abstractclassmethod

class AbstractView(ABC):
    
    @abstractclassmethod
    def __init__(self, data):
        pass
    
    @abstractclassmethod
    def render(self):
        pass