import database
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame,
    QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from PyQt6.QtGui import QKeySequence

class User:
    def __init__(self, username:str, password:str, is_admin:int = 0, viewable_nodes:list = []):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.viewable_nodes = database.get_nodes() if is_admin else viewable_nodes

    def list_info(self):
        return (self.username, self.password, self.is_admin, str(self.viewable_nodes))
        
def store_db(user:User):
    user_info = user.list_info()
    database.add_user(user_info)


class LoginWindow(QWidget):

    login_successful = pyqtSignal(User)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SafeTrack - Login")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(self.styles())
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("card")
        card.setFixedWidth(400)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("SafeTrack")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("Login")
        login_btn.setShortcut(QKeySequence("Return"))
        login_btn.clicked.connect(self.handle_login)

        card_layout.addWidget(title)
        card_layout.addSpacing(20)
        card_layout.addWidget(self.username)
        card_layout.addWidget(self.password)
        card_layout.addWidget(login_btn)

        layout.addWidget(card)

    def handle_login(self):
        name = (self.username.text().strip()).capitalize()
        if not self.username.text():
            QMessageBox.warning(self, "Login Failed", "Please enter a username")
            return -1
        
        user = User(
            username=name,
            password=self.password.text().strip(),
            is_admin = 1 if name.lower() == "admin" and self.password.text().strip() == "admin" else 0,
        )
        if user.is_admin:
            user.viewable_nodes = database.get_nodes() # Admin can view all nodes regardless of DB entry

        if user.username not in database.list_users():
            database.add_user(user.list_info())
            self.login_successful.emit(user)
            self.close()

        elif database.authenticate_user(user.username, user.password):
            self.login_successful.emit(user)
            self.close()

        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def styles(self):
        return """
        /* ===== APP BACKGROUND ===== */
        QWidget {
            background-color: #060d1a;
            color: #e6edf3;
            font-family: "Segoe UI";
            font-size: 14px;
        }

        /* ===== LOGIN CARD ===== */
        QFrame#card {
            background-color: #0e1625;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.04);
        }

        /* ===== TITLE ===== */
        QLabel#title {
            font-size: 30px;
            font-weight: 600;
            color: #ffffff;
            letter-spacing: 1px;
            border: 0px;
            padding: 0px;
            margin: 0px;
            background: transparent;
        }

        /* ===== INPUT FIELDS ===== */
        QLineEdit {
            background-color: #111c30;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 14px 16px;
            font-size: 14px;
        }

        QLineEdit:hover {
            border: 1px solid rgba(255,255,255,0.15);
        }

        QLineEdit:focus {
            border: 1px solid #3b82f6;
            background-color: #13213a;
        }

        /* ===== LOGIN BUTTON ===== */
        QPushButton {
            background-color: #2563eb;
            border: none;
            border-radius: 12px;
            padding: 14px;
            font-size: 15px;
            font-weight: 600;
            color: white;
        }

        QPushButton:hover {
            background-color: #3b82f6;
        }

        QPushButton:pressed {
            background-color: #1d4ed8;
        }
        """