# alert_system.py
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
from login import User

class AlertSystem(QObject):
    viewNodeRequested = pyqtSignal(int)   # node_id

    def __init__(self, parent=None, user:User=None):
        super().__init__(parent)
        self.parent = parent
        self.user = user if user else User("Guest", "", 0, [])

    def show_alert_node(self, notification):
        msg = QMessageBox(self.parent)
        msg.setWindowTitle("Node Alert")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(f"Node {notification[1]} ALERT")
        msg.setInformativeText(notification[4])

        view_btn = None

        if notification[1] in self.user.viewable_nodes:
            view_btn = msg.addButton(
                "View on Map",
                QMessageBox.ButtonRole.AcceptRole
            )
        dismiss_btn = msg.addButton(
            "Dismiss",
            QMessageBox.ButtonRole.RejectRole
        )

        msg.exec()

        if msg.clickedButton() == view_btn:
            print("View on Map clicked for node", notification[1])
            self.viewNodeRequested.emit(notification[1])

    def show_login_alert(self, notification):
        msg = QMessageBox(self.parent)
        msg.setWindowTitle(notification[0])
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(notification[1])
        msg.setInformativeText(notification[2])
        login_btn = msg.addButton("Login", QMessageBox.ButtonRole.AcceptRole)
        dismiss_btn = msg.addButton("Dismiss", QMessageBox.ButtonRole.RejectRole)
        msg.exec()

        if msg.clickedButton() == login_btn:
            print("Login button clicked")
            # Placeholder for actual login dialog; for now just print message
