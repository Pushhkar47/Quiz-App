import sys
import json
import hashlib
import subprocess  # This is required to run the external Project.py script
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QVBoxLayout, QPushButton, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# File for storing user data
USER_DATA_FILE = "users.json"

# Helper function to hash passwords (using SHA-256 for simplicity)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Quiz Application")
        self.setGeometry(100, 100, 1400, 700)
        
        # Stack widget to manage screens
        self.stacked_widget = QStackedWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)

        # Initialize screens
        self.init_login_screen()
        self.init_signup_screen()
        self.init_welcome_screen()
        self.init_quiz_screen()

        self.stacked_widget.setCurrentWidget(self.login_screen)

    def load_user_data(self):
        """Load user data from file."""
        try:
            with open(USER_DATA_FILE, "r") as file:
                users = json.load(file)
                return users
        except FileNotFoundError:
            return {}

    def save_user_data(self, users):
        """Save user data to file."""
        with open(USER_DATA_FILE, "w") as file:
            json.dump(users, file)

    def init_login_screen(self):
        """Create and style the login screen."""
        self.login_screen = QWidget()
        layout = QVBoxLayout(self.login_screen)

        # Title label
        title_label = QLabel("Login to Start Quiz")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        title_label.setAlignment(Qt.AlignCenter)

        # Username and Password fields
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")

        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Login button
        login_button = QPushButton("Login")
        login_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14pt; padding: 8px;")
        login_button.clicked.connect(self.login)

        # Signup button (navigate to signup screen)
        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("background-color: #ff6347; color: white; font-size: 14pt; padding: 8px;")
        signup_button.clicked.connect(self.show_signup_screen)

        # Arrange widgets
        layout.addWidget(title_label)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(signup_button)

        # Add to stacked widget
        self.stacked_widget.addWidget(self.login_screen)

    def init_signup_screen(self):
        """Create and style the signup screen."""
        self.signup_screen = QWidget()
        layout = QVBoxLayout(self.signup_screen)

        # Title label
        title_label = QLabel("Sign Up to Create an Account")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        title_label.setAlignment(Qt.AlignCenter)

        # Username, Password, and Confirm Password fields
        username_label = QLabel("Username:")
        self.signup_username_input = QLineEdit()
        self.signup_username_input.setPlaceholderText("Enter your username")

        password_label = QLabel("Password:")
        self.signup_password_input = QLineEdit()
        self.signup_password_input.setPlaceholderText("Enter your password")
        self.signup_password_input.setEchoMode(QLineEdit.Password)

        confirm_password_label = QLabel("Confirm Password:")
        self.signup_confirm_password_input = QLineEdit()
        self.signup_confirm_password_input.setPlaceholderText("Confirm your password")
        self.signup_confirm_password_input.setEchoMode(QLineEdit.Password)

        # Signup button
        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14pt; padding: 8px;")
        signup_button.clicked.connect(self.signup)

        # Arrange widgets
        layout.addWidget(title_label)
        layout.addWidget(username_label)
        layout.addWidget(self.signup_username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.signup_password_input)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.signup_confirm_password_input)
        layout.addWidget(signup_button)

        # Add to stacked widget
        self.stacked_widget.addWidget(self.signup_screen)

    def init_welcome_screen(self):
        """Create and style the welcome screen after login."""
        self.welcome_screen = QWidget()
        layout = QVBoxLayout(self.welcome_screen)

        # Title label
        title_label = QLabel("Welcome to the Quiz!")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #ffffff;")

        # Start quiz button
        start_quiz_button = QPushButton("Start Quiz")
        start_quiz_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14pt; padding: 8px;")
        start_quiz_button.clicked.connect(self.start_quiz)

        # Arrange widgets
        layout.addWidget(title_label)
        layout.addWidget(start_quiz_button)

        # Add to stacked widget
        self.stacked_widget.addWidget(self.welcome_screen)

    def init_quiz_screen(self):
        """Create and style the quiz screen."""
        self.quiz_screen = QWidget()
        layout = QVBoxLayout(self.quiz_screen)

        # Apply background to the entire quiz screen
        self.quiz_screen.setStyleSheet(
            "background-image: url('quiz_background.jpg');"
            "background-repeat: no-repeat;"
            "background-position: center;"
            "background-size: cover;"
        )

        # Add a sample label to the quiz screen to check if it displays
        label = QLabel("Quiz Questions Will Go Here!")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 24, QFont.Bold))
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        # Ensure the layout is properly set
        self.quiz_screen.setLayout(layout)

        # Add to stacked widget
        self.stacked_widget.addWidget(self.quiz_screen)

    def login(self):
        """Check login credentials and navigate to welcome screen."""
        username = self.username_input.text()
        password = self.password_input.text()

        # Load user data from file
        users = self.load_user_data()

        # Hash password for comparison
        hashed_password = hash_password(password)

        # Check if username exists and password matches
        if username in users and users[username] == hashed_password:
            print("Login successful!")  # Debug message
            self.stacked_widget.setCurrentWidget(self.welcome_screen)

            # Execute Project.py after successful login
            try:
                subprocess.run(["python", "C:\\Users\\pushh\\OneDrive\\Desktop\\Final_Project\\Project.py"], check=True)  # Run Project.py after login
                print("Project.py executed successfully!")  # Debug message
            except subprocess.CalledProcessError as e:
                self.show_error(f"Failed to run Project.py: {e}")
            
            # Once Project.py is done, show the quiz screen
            self.stacked_widget.setCurrentWidget(self.quiz_screen)
        else:
            self.show_error("Invalid login credentials. Please try again.")

    def start_quiz(self):
        """Navigate to the quiz screen."""
        self.stacked_widget.setCurrentWidget(self.quiz_screen)

    def signup(self):
        """Handle signup and save the user data."""
        username = self.signup_username_input.text()
        password = self.signup_password_input.text()
        confirm_password = self.signup_confirm_password_input.text()

        # Simple signup validation
        if password != confirm_password:
            self.show_error("Passwords do not match. Please try again.")
            return

        # Load existing user data
        users = self.load_user_data()

        # Check if username already exists
        if username in users:
            self.show_error("Username already exists. Please choose a different one.")
            return

        # Hash the password before saving
        hashed_password = hash_password(password)

        # Save the new user data
        users[username] = hashed_password
        self.save_user_data(users)

        # Navigate to the welcome screen after successful signup
        self.stacked_widget.setCurrentWidget(self.welcome_screen)

    def show_signup_screen(self):
        """Switch to the signup screen."""
        self.stacked_widget.setCurrentWidget(self.signup_screen)

    def show_error(self, message):
        """Show error message."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

# Run the application
app = QApplication(sys.argv)
window = QuizApp()
window.show()
sys.exit(app.exec_())
