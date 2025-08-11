import json
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class MissionMgrModel(QObject):
    currentPageChanged = pyqtSignal(str)
    missionItemSelected = pyqtSignal(str, str, dict)
    waypointItemSelected = pyqtSignal(int)

    def __init__(self, *args: None, **kwargs: None) -> None:
        super().__init__(*args, **kwargs)
        self.path_json_missions: str = './JSON/missions_v2_sample.json'
        self.page_init: str = 'page_init'
        self._current_page = self.page_init
        
        self.json_missions: dict = self._load_from_json()
        
        self.current_msn_cat: str = ''
        self.current_msn_name: str = ''
        self.current_mission_details: dict = {}
        
        self.msn_categories: list = ['search', 'strike', 'patrol', 'surv']
        self.ap_types = ['수색지점(원형)', '수색지점(사각)', '타격지점', '정찰지점', '감시지점']
        self.tree_page_map: dict = {f'tree_{cat}': f'page_{cat}' for cat in self.msn_categories}
        for cat in self.msn_categories:
            setattr(self, f'mission_items_{cat}', sorted(self._fetch_mission_content(cat).keys()))
        
    @pyqtProperty(str, notify=currentPageChanged)
    def current_page(self) -> str:
        return self._current_page
    
    @current_page.setter
    def current_page(self, page_name: str) -> None:
        if page_name != self._current_page:
            self._current_page = page_name
            self.currentPageChanged.emit(self._current_page)

    @pyqtProperty(int, notify=waypointItemSelected)
    def waypoint_selected(self) -> int:
        return None
    
    @waypoint_selected.setter
    def waypoint_selected(self, wp_idx: int) -> None:
        self.waypointItemSelected.emit(wp_idx)
    
    def _load_from_json(self) -> dict:
        try:
            with open(self.path_json_missions, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except (FileNotFoundError, json.JSONDecodeError):
            print("Warning: JSON not found.")
            
    def save_to_json(self, key: str, val: str) -> None:
        None
        
    def _fetch_mission_content(self, msn_cat: str) -> list:
        msn_names = {item['name']: item['details'] for item in self.json_missions[msn_cat]}
        return msn_names
    
    def set_mission_details(self, msn_cat: str, msn_name: str) -> None:
        self.current_msn_cat = msn_cat
        self.current_msn_name = msn_name
        self.current_mission_details = self._fetch_mission_content(msn_cat).get(msn_name)
        self.missionItemSelected.emit(
                self.current_msn_cat,
                self.current_msn_name,
                self.current_mission_details
            )
