from packages.tapisetl.ETLController import ETLController


class Index(ETLController):
    def __init__(self):
        ETLController.__init__(self)
    
    def index(self):
        self.help()
    