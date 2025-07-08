from PyQt5 import uic

widget_form, base_class = uic.loadUiType('./ui/test.ui')

class View(base_class, widget_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def update_label(self, text):
        self.my_label.setText(text)
