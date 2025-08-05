import json
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class Model(QObject):
    ''' 모델 '''
    
    '''
    ✅개발자 노트:
        Qt 시그널 및 Qt 프로퍼티는 클래스 수준(class attribute)으로 선언해야 함
        그래야 Qt 메타시스템이 시그널과 프로퍼티를 인식할 수 있고, 오버라이딩을 방지할 수 있음
    '''
    jsonChanged = pyqtSignal(dict) # json 데이터 읽기 및 쓰기 시그널 선언
    
    def __init__(self) -> None:
        super().__init__()
        self.json_path: str = './db/data.json'
        
        # 모델 객체 생성 시 json 데이터를 메모리에 고정: json 파일의 반복적인 읽고 쓰기를 방지하기 위함
        self._json_data: dict = self.load_from_json()

    @pyqtProperty(dict, notify=jsonChanged) # 데코레이터를 활용해 간소한 프로퍼티로 선언
    def get_text_json(self):
        return self._json_data

    def load_from_json(self):
        ''' json 파일 읽기 '''
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                # self.jsonChanged.emit(self._json_data) # json 데이터 읽기가 발생했다는 시그널 방출
                
                return json.load(f) # json 데이터를 딕셔너리로 반환
                
        except (FileNotFoundError, json.JSONDecodeError):
            print("Warning: JSON 파일을 찾을 수 없거나 형식이 잘못되었습니다.")

    def save_to_json(self, key: str, val: str):
        ''' json 파일 쓰기 '''
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                self._json_data[key] = val # 메모리에 고정된 json 데이터 수정
                json.dump(self._json_data, f, indent=4, ensure_ascii=False) # json에 변경된 데이터 저장
            
            self.jsonChanged.emit(self._json_data) # json 데이터 쓰기가 발생했다는 시그널 방출
            
        except Exception as e:
            print(f"Error saving to JSON: {e}")

    '''
    ✅개발자 노트:
        Qt 프로퍼티 선언부
        컨트롤러가 이 프로퍼티에 값을 할당하여 모델을 업데이트하거나,
        이 함수에 담긴 값(모델에 저장된 데이터)을 꺼내어 이용할 수 있움
        
        컨트롤러가 이 프로퍼티에서 값을 꺼낼 경우 fget 인자로 들어온 함수가 실행되고,
        컨트롤러가 이 프로퍼티에 값을 할당할 경우 fset 인자로 들어온 함수가 실행
        
        현재 get_text_json()은 데코레이터를 통해 간소한 프로퍼티로 쓸 수 있는 상태
        따라서 아래 프로퍼티는 필요 없으나 예제로 남김
    ''' 
    sample_property = pyqtProperty(
        str,
        fget=get_text_json,
        fset=None,
        notify=jsonChanged
    )
