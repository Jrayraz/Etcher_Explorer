import os
import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QScrollArea, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QMenu, QDialog, QFormLayout, QHBoxLayout, QSizePolicy)
from PySide6.QtCore import Qt

class PassSave(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PassSave")
        self.setGeometry(100, 100, 600, 400)
        
        self.secrets_dir = os.path.join(os.getcwd(), ".config/.secrets")
        os.makedirs(self.secrets_dir, exist_ok=True)

        self.initUI()
        self.load_accounts()  # Call load_accounts immediately after initializing the UI

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollContent = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollContent)
        self.scrollContent.setLayout(self.scrollLayout)
        self.scrollArea.setWidget(self.scrollContent)

        self.layout.addWidget(self.scrollArea)

        # Add "+" button
        self.addButton = QPushButton("+", self)
        self.addButton.setFixedSize(40, 40)
        self.addButton.clicked.connect(self.showAddMenu)
        
        # Add red "x" button
        self.closeButton = QPushButton("x", self)
        self.closeButton.setFixedSize(40, 40)
        self.closeButton.setStyleSheet("QPushButton { color: red; }")
        self.closeButton.clicked.connect(self.closeApplication)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.addButton)
        self.buttonLayout.addWidget(self.closeButton)
        self.layout.addLayout(self.buttonLayout)

    def showAddMenu(self):
        menu = QMenu(self)
        
        online_action = menu.addAction("Online Account")
        online_action.triggered.connect(lambda: self.openAddAccountDialog("Online Account"))
        
        bank_action = menu.addAction("Bank Card")
        bank_action.triggered.connect(lambda: self.openAddAccountDialog("Bank Card"))
        
        membership_action = menu.addAction("Membership Card")
        membership_action.triggered.connect(lambda: self.openAddAccountDialog("Membership Card"))
        
        license_action = menu.addAction("Driver's License")
        license_action.triggered.connect(lambda: self.openAddAccountDialog("Driver's License"))

        pin_action = menu.addAction("PIN")
        pin_action.triggered.connect(lambda: self.openAddAccountDialog("PIN"))

        passcode_action = menu.addAction("Passcode")
        passcode_action.triggered.connect(lambda: self.openAddAccountDialog("Passcode"))

        ssn_action = menu.addAction("SSN")
        ssn_action.triggered.connect(lambda: self.openAddAccountDialog("SSN"))

        menu.exec(self.addButton.mapToGlobal(self.addButton.rect().bottomLeft()))

    def openAddAccountDialog(self, account_type):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Add {account_type}")
        
        layout = QFormLayout(dialog)
        name_input = QLineEdit(dialog)
        email_input = QLineEdit(dialog)
        username_input = QLineEdit(dialog)
        secret_input = QLineEdit(dialog)
        business_input = QLineEdit(dialog)
        website_input = QLineEdit(dialog)
        
        layout.addRow("Name:", name_input)
        layout.addRow("Email:", email_input)
        layout.addRow("Username:", username_input)
        layout.addRow("Secret:", secret_input)
        layout.addRow("Business:", business_input)
        layout.addRow("Website:", website_input)
        
        save_button = QPushButton("Save", dialog)
        save_button.clicked.connect(lambda: self.saveNewAccount(account_type, name_input, email_input, username_input, secret_input, business_input, website_input, dialog))
        layout.addRow(save_button)
        
        dialog.exec()

    def saveNewAccount(self, account_type, name_input, email_input, username_input, secret_input, business_input, website_input, dialog):
        account = {
            "Type": account_type,
            "Name": name_input.text(),
            "Email": email_input.text(),
            "Username": username_input.text(),
            "Secret": secret_input.text(),
            "Business": business_input.text(),
            "Website": website_input.text()
        }
        
        account_name = account["Name"]
        account_file_path = os.path.join(self.secrets_dir, f"{account_name}.json")
        
        with open(account_file_path, 'w') as file:
            json.dump(account, file)
        
        self.addAccountWidget(account_name, account)
        dialog.accept()

    def addAccountWidget(self, account_name, account):
        widget = QWidget()
        widget.setFixedHeight(60)  # Set the fixed height for account widget
        layout = QHBoxLayout(widget)
        
        account_label = QLabel(f"{account_name}", self)
        layout.addWidget(account_label)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(spacer)
        
        view_button = QPushButton("View", self)
        view_button.clicked.connect(lambda: self.viewAccountDetails(account_name, account))
        layout.addWidget(view_button)
        
        widget.setLayout(layout)
        self.scrollLayout.addWidget(widget)

    def viewAccountDetails(self, account_name, account):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{account_name} Details")
        
        layout = QFormLayout(dialog)
        for key, value in account.items():
            layout.addRow(f"{key}:", QLabel(value, dialog))
        
        edit_button = QPushButton("Edit", dialog)
        edit_button.clicked.connect(lambda: self.editAccountDetails(account_name, account, dialog))
        layout.addRow(edit_button)
        
        dialog.exec()

    def editAccountDetails(self, account_name, account, dialog):
        dialog.close()
        
        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle(f"Edit {account_name}")
        
        layout = QFormLayout(edit_dialog)
        inputs = {}
        for key, value in account.items():
            input_field = QLineEdit(edit_dialog)
            input_field.setText(value)
            layout.addRow(f"{key}:", input_field)
            inputs[key] = input_field
        
        save_button = QPushButton("Save", edit_dialog)
        save_button.clicked.connect(lambda: self.saveEditedAccount(account_name, inputs, edit_dialog))
        layout.addRow(save_button)
        
        edit_dialog.exec()

    def saveEditedAccount(self, account_name, inputs, dialog):
        account = {key: input_field.text() for key, input_field in inputs.items()}
        
        account_file_path = os.path.join(self.secrets_dir, f"{account_name}.json")
        
        with open(account_file_path, 'w') as file:
            json.dump(account, file)
        
        dialog.accept()
        self.refreshAccountWidgets()

    def refreshAccountWidgets(self):
        # Clear existing widgets
        for i in reversed(range(self.scrollLayout.count())):
            widget = self.scrollLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Load and display updated account widgets
        for filename in os.listdir(self.secrets_dir):
            if filename.endswith(".json"):
                account_name = filename[:-5]  # Remove .json extension
                account_file_path = os.path.join(self.secrets_dir, filename)
                
                try:
                    with open(account_file_path, 'r', encoding='utf-8') as file:
                        account = json.load(file)
                    self.addAccountWidget(account_name, account)
                except (UnicodeDecodeError, json.JSONDecodeError) as e:
                    print(f"Error loading {account_file_path}: {e}")

    def load_accounts(self):
        self.refreshAccountWidgets()

    def closeApplication(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PassSave()
    window.show()
    sys.exit(app.exec())
