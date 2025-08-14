class Launcher(QObject):
    def __init__(self, parent: QObject|None = None) -> None:
        super().__init__(parent)
        self.model = mission_navigator_model.MissionMgrModel()
        self.view = mission_navigator_view.MissionMgrView()
        self.controller = [
            ButtonController(self, self.model, self.view),
            StackedWidgetController(self, self.model, self.view),
            MissionTreeController(self, self.model, self.view),
            MissionLabelController(self, self.model, self.view),
            WaypointTreeController(self, self.model, self.view),
            WaypointLabelController(self, self.model, self.view)
        ]
        
        self._do()
    
    def _do(self) -> None:
        self.view.show()
        

class ButtonController(QObject):
    def __init__(
            self,
            parent: Launcher,
            model: mission_navigator_model.MissionMgrModel,
            view: mission_navigator_view.MissionMgrView
        ) -> None:
        super().__init__(parent)
        
        self.model = model
        self.view = view
        
        for i, btype in enumerate(self.view.main_btypes):
            setattr(self, f'btn_{btype}', self.view.main_buttons[i])
        
        for cat in self.view.msn_categories:
            for i, btype in enumerate(self.view.msn_btypes):
                setattr(self, f'btn_{cat}_{btype}', getattr(self.view, f'{cat}_buttons')[i])

        self.MISSION_CREATE_AND_MODIFY: mission_create_n_modify_ctrl.Launcher = None
        
        self._do()

    def _do(self) -> None:
        self.btn_close.clicked.connect(self._on_close_clicked)
        self.btn_msn_create.clicked.connect(self._on_msn_create_clicked)
        self.btn_msn_send.clicked.connect(self._on_msn_send_clicked)
        for cat in self.view.msn_categories: # 슬롯으로 인자를 넘기려면 lambda 또는 partial을 이용해야 합니다.
            getattr(self, f'btn_{cat}_delete').clicked.connect(lambda checked=False, c=cat: self._on_msn_delete_clicked(c))
            getattr(self, f'btn_{cat}_modify').clicked.connect(lambda checked=False, c=cat: self._on_msn_modify_clicked(c))
            
    @pyqtSlot()
    def _on_close_clicked(self) -> None:
        self.view.close()
        
    @pyqtSlot()
    def _on_msn_create_clicked(self) -> None:
        self.MISSION_CREATE_AND_MODIFY = mission_create_n_modify_ctrl.Launcher(self)
        
    @pyqtSlot()
    def _on_msn_send_clicked(self) -> None:
        print(f'{self.btn_msn_send.objectName()} has been clicked')
            
    @pyqtSlot(str)
    def _on_msn_delete_clicked(self, msn_cat: str) -> None:
        self.model.current_page = self.model.page_init
        
        for tree in self.view.trees:
            tree.blockSignals(True)
            tree.clearSelection()
            tree.blockSignals(False)
        
    @pyqtSlot(str)
    def _on_msn_modify_clicked(self, msn_cat: str) -> None:
        tmp = getattr(self, f'btn_{msn_cat}_modify').objectName()
        print(f'{tmp} has been clicked')
        
        self.mission_create_n_modify = mission_create_n_modify_ctrl.Launcher(self, msn_cat)
      
class MissionTreeController(QObject):
    def __init__(
            self,
            parent: Launcher,
            model: mission_navigator_model.MissionMgrModel,
            view: mission_navigator_view.MissionMgrView
        ) -> None:
        super().__init__(parent)
        
        self.model = model
        self.view = view
        
        self.tree_page_map = self.model.tree_page_map
        
        self._do()
        
    def _do(self) -> None:
        for cat in self.model.msn_categories:
            self._populate_trees(cat, getattr(self.model, f'mission_items_{cat}'))
        
        for tree in self.view.trees: # 네 개의 tree widget에 대해
            tree.itemSelectionChanged.connect(self._on_tree_selected)
            
    def _populate_trees(self, msn_cat: str, msn_items: list) -> None:
        getattr(self.view, f'tree_{msn_cat}').clear()
        for msn_item in msn_items:
            QTreeWidgetItem(getattr(self.view, f'tree_{msn_cat}'), [msn_item])
    
    @pyqtSlot()
    def _on_tree_selected(self) -> None:
        sender_tree = self.sender()
        tree_name = sender_tree.objectName()
        msn_item = sender_tree.currentItem().text(0)
        
        if tree_name not in self.tree_page_map:
            return
        
        page_name = self.tree_page_map[tree_name]
        self.model.current_page = page_name
        
        for tree in self.view.trees:
            if tree is sender_tree:
                continue
            tree.blockSignals(True)
            tree.clearSelection()
            tree.blockSignals(False)
        
        msn_cat = tree_name[5:]
        self.view.wp_labels_clear(msn_cat)
        self.model.set_mission_details(msn_cat, msn_item)


class StackedWidgetController(QObject):
    def __init__(
            self,
            parent: Launcher,
            model: mission_navigator_model.MissionMgrModel,
            view: mission_navigator_view.MissionMgrView
        ) -> None:
        super().__init__(parent)
        
        self.model = model
        self.view = view
        
        self.pages = self.view.pages
        
        self._do()
        
    def _do(self) -> None:
        if self.model.current_page:
            self._show_page(self.model.current_page)
        
        self.model.currentPageChanged.connect(self._show_page)
        
    @pyqtSlot(str)
    def _show_page(self, page_name: str) -> None:    
        page = self.pages.findChild(QWidget, page_name)
        if page:
            self.pages.setCurrentWidget(page)


class MissionLabelController(QObject):
    def __init__(
            self,
            parent: Launcher,
            model: mission_navigator_model.MissionMgrModel,
            view: mission_navigator_view.MissionMgrView
        ) -> None:
        super().__init__(parent)
        
        self.model = model
        self.view = view
        
        self._do()
        
    def _do(self) -> None:
        self.model.missionItemSelected.connect(self._populate_labels)
        
    @pyqtSlot(str, str, dict)
    def _populate_labels(self, msn_cat: str, msn_name: str, msn_detail: dict) -> None:
        wpcounts: int = len(msn_detail['waypoints'])
        apcounts: int = 0
        for wp in msn_detail['waypoints']:
            if wp['type'] in self.model.ap_types:
                apcounts += 1
        
        getattr(self.view, f'label_{msn_cat}_id').setText(msn_detail['id'])
        getattr(self.view, f'label_{msn_cat}_name').setText(msn_name)
        getattr(self.view, f'label_{msn_cat}_wpcounts').setText(f'{wpcounts}개')
        getattr(self.view, f'label_{msn_cat}_apcounts').setText(f'{apcounts}개')


class WaypointTreeController(QObject):
    def __init__(
            self,
            parent: Launcher,
            model: mission_navigator_model.MissionMgrModel,
            view: mission_navigator_view.MissionMgrView
        ) -> None:
        super().__init__(parent)
        
        self.model = model
        self.view = view
        
        self._do()
        
    def _do(self) -> None:
        self.model.missionItemSelected.connect(self._populate_tree)
        for cat in self.model.msn_categories:
            getattr(self.view, f'tree_{cat}_waypoints').itemSelectionChanged.connect(self._on_tree_selected)
        
    @pyqtSlot(str, str, dict)
    def _populate_tree(self, msn_cat: str, _: str, msn_detail: dict) -> None:
        getattr(self.view, f'tree_{msn_cat}_waypoints').clear()
        
        for wp in msn_detail['waypoints']:
            wp_on_tree = [wp['name'], wp['type'], wp['coord']]
            QTreeWidgetItem(getattr(self.view, f'tree_{msn_cat}_waypoints'), wp_on_tree)
        
    @pyqtSlot()
    def _on_tree_selected(self) -> None:
        sender_tree = self.sender()
        wp_name = sender_tree.currentItem().text(0)
        for idx, wp in enumerate(self.model.current_mission_details['waypoints']):
            if wp['name'] == wp_name:
                self.model.waypoint_selected = idx
                break


class WaypointLabelController(QObject):
    def __init__(
            self,
            parent: Launcher,
            model: mission_navigator_model.MissionMgrModel,
            view: mission_navigator_view.MissionMgrView
        ) -> None:
        super().__init__(parent)
        
        self.model = model
        self.view = view
        
        self._do()
        
    def _do(self) -> None:
        self.model.waypointItemSelected.connect(self._populate_labels)
        
    @pyqtSlot(int)
    def _populate_labels(self, wp_idx: int) -> None:
        self.view.wp_labels_clear(self.model.current_msn_cat)
        wp_details = self.model.current_mission_details['waypoints'][wp_idx]

        #공통 속성
        getattr(self.view, f'label_{self.model.current_msn_cat}_wp_id').setText(wp_details.get('id', ''))
        getattr(self.view, f'label_{self.model.current_msn_cat}_wp_type').setText(wp_details.get('type', ''))
        getattr(self.view, f'label_{self.model.current_msn_cat}_wp_coord').setText(wp_details.get('coord', ''))
        getattr(self.view, f'label_{self.model.current_msn_cat}_wp_next_action').setText(wp_details.get('next_action', ''))
        if self.model.current_msn_cat == self.model.msn_categories[0]:
            getattr(self.view, f'label_{self.model.current_msn_cat}_wp_fight').setText(str(wp_details.get('fight', '')))
        elif self.model.current_msn_cat == self.model.msn_categories[1]:
            getattr(self.view, f'label_{self.model.current_msn_cat}_wp_fight_range').setText(f"{wp_details.get('fight_range', '')}m")
            getattr(self.view, f'label_{self.model.current_msn_cat}_wp_fight_status').setText(wp_details.get('fight_status', ''))
        elif self.model.current_msn_cat == self.model.msn_categories[2]:
            getattr(self.view, f'label_{self.model.current_msn_cat}_wp_detect_obj').setText(wp_details.get('detect_obj', ''))
        elif self.model.current_msn_cat == self.model.msn_categories[3]:
            getattr(self.view, f'label_{self.model.current_msn_cat}_wp_detect_obj').setText(wp_details.get('detect_obj', ''))
            getattr(self.view, f'label_{self.model.current_msn_cat}_wp_rcws_status').setText(wp_details.get('rcws_status', ''))
            getattr(self.view, f'label_{self.model.current_msn_cat}_wp_duration').setText(f"{wp_details.get('duration', '')}초")
        else:
            None
