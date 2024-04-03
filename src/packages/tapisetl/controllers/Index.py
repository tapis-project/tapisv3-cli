from packages.tapisetl.ETLController import ETLController
from utils.Prompt import prompt


class Index(ETLController):
    directories = {}
    
    def __init__(self):
        ETLController.__init__(self)
        
    def index(self):
        self.help()