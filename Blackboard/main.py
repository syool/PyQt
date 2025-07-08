import sys
from PyQt5.QtWidgets import QApplication

from src import model, view, controller

def run() -> None:
    app = QApplication(sys.argv)
    
    m = model.Model()
    v = view.View()
    _ = controller.Controller(m, v)
    
    v.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    run()
