import json
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class Model(QObject):
    '''
    개발자 노트:
        Qt 시그널 및 Qt 프로퍼티는 클래스 수준(class attribute)으로 선언해야 합니다.
        그래야 Qt 메타시스템이 시그널과 프로퍼티를 인식할 수 있고, 오버라이딩을 방지할 수 있기 때문입니다.
        __init__()에서는 모델이 저장하는 정보를 선언합니다.
    '''
    userTextChanged = pyqtSignal(str)
    
    def __init__(self) -> None:
        super().__init__()
        self.json_path: str = './db/data.json'
        self.input_content: str = ''

    def _get_label_text_from_json(self) -> str:
        ''' QLabel에 표시될 내용을 가져오는 함수 '''
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('TextInTheShell', '오류: 키를 찾을 수 없음')
            
        except FileNotFoundError:
            return "오류: JSON 파일을 찾을 수 없음"
        
        except json.JSONDecodeError:
            return "오류: JSON 파일 형식이 잘못됨"

    def _set_label_text_to_json(self, content: str) -> None:
        ''' QLabel에 표시될 내용을 지정하는 함수 '''

        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data['TextInTheShell'] = content
            json.dumps(data, indent=4, ensure_ascii=False)

        self.userTextChanged.emit(data['TextInTheShell'])
        
    '''
    개발자 노트:
        Qt 프로퍼티 선언부입니다.
        컨트롤러가 이 프로퍼티에 값을 할당하여 모델을 업데이트하거나,
        이 함수에 담긴 값(모델에 저장된 데이터)을 꺼내어 이용할 수 있습니다.
        
        컨트롤러가 이 프로퍼티에서 값을 꺼낼 경우 fget 인자로 들어온 함수가 실행되고,
        컨트롤러가 이 프로퍼티에 값을 할당할 경우 fset 인자로 들어온 함수가 실행됩니다.
    '''
    text_json = pyqtProperty(
        str,
        fget=_get_label_text_from_json,
        fset=_set_label_text_to_json,
        notify=userTextChanged
    )
    
