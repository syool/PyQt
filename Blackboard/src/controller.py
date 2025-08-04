from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication

from src.model import Model
from src.view import View


class Launcher(QObject):
    '''
    실행 컨트롤러
        ✅개발자 노트:
            1. 이 컨트롤러는 parent 인자를 명시하지 않으면 기본적으로 Qbject를 상속
            2. 이 컨트롤러가 앱의 최초 실행점일 경우 parent 인자를 명시하지 않아도 됨
            3. 이 컨트롤러를 실행하는 상위 컨트롤러가 존재할 경우 self를 parent 인자로 상속받는 걸 권장
    '''
    def __init__(
            self,
            parent: QObject|None = None
        ) -> None:
        super().__init__(parent)
        self.model = Model()
        self.view = View()
        self.controller = [
            LabelController(self, self.model, self.view),
            ButtonController(self, self.model, self.view)
        ]
        
        self._do()

    def _do(self):
        ''' controller functions '''
        LabelController._set_label(self, self.model.get_text_json) # 초기화: json 데이터를 QLabel에 반영
                
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
        self.model.jsonChanged.connect(self._set_label) # json 데이터 읽기 및 쓰기를 감지하여 슬롯 실행
        
    @pyqtSlot(str)
    def _set_label(self, content: str) -> None:
        '''
        QLabel 글 설정
            ✅개발자 노트:
                jsonChanged 시그널이 활성화되면 Model.get_text_json()의 리턴 값이 content 인자로 들어 옴\n
                Model.get_text_json()는 @pyqtProperty 데코레이터에 의해 jsonChanged 시그널과 연동됨
        '''
        self.view.label_output.setText(content)


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
        self.view.btn_apply.clicked.connect(self._on_apply_clicked) # apply 버튼 이벤트 연결
        self.view.btn_close.clicked.connect(self._on_close_clicked) # close 버튼 이벤트 연결
        
    @pyqtSlot()
    def _on_apply_clicked(self) -> None:
        ''' apply 버튼 클릭 이벤트 '''
        self.model.save_to_json(self.view.line_input.text()) # QLineEdit 입력 값을 json에 저장
        
    @pyqtSlot()
    def _on_close_clicked(self) -> None:
        ''' close 버튼 클릭 이벤트 '''
        QApplication.instance().quit()
