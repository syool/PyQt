
widget_class, base_class = uic.loadUiType('./assets/ui/ui_mission_mgr/mission_navigator.ui')

class MissionMgrView(base_class, widget_class):
    def __init__(self, *args: None, **kwargs: None) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('asdf')
        
        self.msn_categories = ['search', 'strike', 'patrol', 'surv']

        self.main_btypes = ['close', 'msn_send', 'msn_create']
        self.main_buttons = [
            getattr(self, f'btn_{btype}') for btype in self.main_btypes
        ]
        
        self.msn_btypes = ['delete', 'modify']
        for cat in self.msn_categories:
            key_ = f'{cat}_buttons'
            val_ = [getattr(self, f'btn_{cat}_{btype}') for btype in self.msn_btypes]
            
            setattr(self, key_, val_)
        
        self.trees = [
            self.tree_search,
            self.tree_strike,
            self.tree_patrol,
            self.tree_surv
        ]
        
        self.pages = self.mission_pages

    def wp_labels_clear(self, cat) -> None:
        getattr(self, f'label_{cat}_wp_id').clear()
        getattr(self, f'label_{cat}_wp_type').clear()
        getattr(self, f'label_{cat}_wp_coord').clear()
        getattr(self, f'label_{cat}_wp_next_action').clear()
        
        if cat == self.msn_categories[0]:
            getattr(self, f'label_{cat}_wp_fight').clear()
        elif cat == self.msn_categories[1]:
            getattr(self, f'label_{cat}_wp_fight_range').clear()
            getattr(self, f'label_{cat}_wp_fight_status').clear()
        elif cat == self.msn_categories[2]:
            getattr(self, f'label_{cat}_wp_detect_obj').clear()
        elif cat == self.msn_categories[3]:
            getattr(self, f'label_{cat}_wp_detect_obj').clear()
            getattr(self, f'label_{cat}_wp_rcws_status').clear()
            getattr(self, f'label_{cat}_wp_duration').clear()
        else:
            None
