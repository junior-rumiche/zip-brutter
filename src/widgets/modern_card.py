from qfluentwidgets import CardWidget


class ModernCardWidget(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modernCard")
        self.setStyleSheet(
            """
            #modernCard {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
        """
        )
