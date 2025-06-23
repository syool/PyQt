import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

widget_form, base_class = uic.loadUiType('./designer_made.ui')  # Qt Designer로 제작된 .ui 파일 연결

class MainClass(base_class, widget_form):
    def __init__(self, *args: None, **kwargs: None) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self) # .ui 파일 내 속성을 .py 파일로 연결
        self.setWindowTitle('blah') # 윈도우 타이틀 설정
        
        self.initUi()

    def initUi(self) -> None:
        ''' UI 기능 구현부 '''
        
        # 내용은 여기에
        
        self.show()


if __name__ == '__main__' :
    app = QApplication(sys.argv) 
    window = MainClass() 
    app.exec_()
