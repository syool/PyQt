class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self._do()

    def _do(self):
        label_text = self.model.get_label_text_from_json()
        self.view.update_label(label_text)
        
