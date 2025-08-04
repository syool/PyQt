from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication

from src.model import Model
from src.view import View


class Launcher(QObject):
    '''
    the launch controller
        1. 이 컨트롤러는 parent 인자를 명시하지 않으면 기본적으로 Qbject를 상속받습니다.
        2. 이 컨트롤러를 실행하는 상위 컨트롤러의 self를 parent 인자로 상속받는 걸 권장합니다.
    '''
    def __init__(
            self,
            parent: QObject|None = None
        ) -> None:
        super().__init__(parent)
        self.model = Model()
        self.view = View()
        self.controller = [
            LineEditController(self, self.model, self.view),
            LabelController(self, self.model, self.view),
            ButtonController(self, self.model, self.view)
        ]

        self._do()

    def _do(self):
        ''' controller functions '''
        self.view.show()


class LineEditController(QObject):
    ''' a functional controller for QLineEdits '''
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
        ''' controller functions '''
        self.view.line_input.textChanged.connect(self._get_input)
        
    @pyqtSlot(str)
    def _get_input(self, content: str) -> None:
        self.model.input_content = content


class LabelController(QObject):
    ''' a functional controller for QLabels '''
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
        self.model.userTextChanged.connect(self._set_label)
        
    @pyqtSlot(str)
    def _set_label(self, content: str) -> None:
        self.view.label_output.setText(content)


class ButtonController(QObject):
    ''' a functional controller for QPushButtons '''
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
        ''' controller functions '''
        self.view.btn_apply.clicked.connect(self._on_apply_clicked)
        self.view.btn_close.clicked.connect(self._on_close_clicked)
        
    @pyqtSlot()
    def _on_apply_clicked(self) -> None:
        self.model.text_json = self.model.input_content
        
    @pyqtSlot()
    def _on_close_clicked(self) -> None:
        QApplication.instance().quit()
