import json

class Model:
    def __init__(self) -> None:
        self.json_path = './db/data.json'

    def get_label_text_from_json(self) -> str:
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('text', '오류: 키를 찾을 수 없음')
            
        except FileNotFoundError:
            return "오류: JSON 파일을 찾을 수 없음"
        
        except json.JSONDecodeError:
            return "오류: JSON 파일 형식이 잘못됨"
