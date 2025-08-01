from PyQt5.QtCore import QObject, pyqtSlot

from src.model import Model
from src.view import View


class Launcher(QObject):
    '''
    실행 컨트롤러
        1. 이 컨트롤러는 parent 인자를 명시하지 않으면 기본적으로 Qbject를 상속받습니다.
        2. 이 컨트롤러를 실행하는 상위 컨트롤러의 self를 parent 인자로 상속받는 걸 권장합니다.
        3. 이 컨트롤러가 앱 전체 최상위 컨트롤러일 경우, parent 인자를 명시하지 않아도 좋습니다.
    '''
    def __init__(
            self,
            parent: QObject|None = None
        ) -> None:
        super().__init__(parent)
        self.model = Model()
        self.view = View()
        self.controller = [
            LabelController(self, self.model, self.view), # QLabel 기능 컨트롤러
            ButtonController(self, self.model, self.view) # QPushButton 기능 컨트롤러
        ]

        self._do()

    def _do(self):
        self.view.show()


class LabelController(QObject):
    ''' QLabel 기능 컨트롤러 '''
    def __init__(
            self,
            parent: Launcher,
            model: Model,
            view: View
        ) -> None:
        super().__init__(parent)
        
        self.model = model
        self.view = view
        
        self._do()
        
    def _do(self):
        text = self.model.get_label_text_from_json()
        self._on_label_updated(text)
    
    @pyqtSlot() 
    def _on_label_updated(self, text):
        self.view.my_label.setText(text)
        

class ButtonController(QObject):
    ''' QPushButton 기능 컨트롤러 '''
    def __init__(
            self,
            parent: Launcher,
            model: Model,
            view: View
        ) -> None:
        super().__init__(parent)
        
        self.model = model
        self.view = view
        
        self._do()
        
    def _do(self):
        None
