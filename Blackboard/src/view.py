from PyQt5 import uic

widget_class, base_class = uic.loadUiType('./ui/test.ui')

class View(base_class, widget_class):
    ''' 뷰 '''
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('blah')
