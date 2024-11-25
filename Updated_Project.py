import sys
from quiz_data import quiz_data
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QRadioButton,
    QPushButton, QMessageBox, QButtonGroup, QComboBox, QStackedWidget
)
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt

# Define the updated quiz data with more questions and multiple categories


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

        # Initialize quiz state
        self.current_question_index = 0
        self.score = 0
        self.category = ""
        self.correct_answers = 0
        self.incorrect_answers = 0
        
        # Score scheme: +4 for correct answers, -1 for wrong answers
        self.points_correct = 4
        self.points_wrong = -1

        # Track answers for each question
        self.answered_questions = [None] * 5  # Placeholder list for answers, None means unanswered

        # Screens
        self.init_start_screen()
        self.init_quiz_screen()
        self.init_end_screen()
        
        self.stacked_widget.setCurrentWidget(self.start_screen)

    def init_start_screen(self):
        """Create and style the start screen with a background."""
        self.start_screen = QWidget()
        layout = QVBoxLayout(self.start_screen)

        # Apply background
        self.set_background(self.start_screen, "start_background.jpg")

        # Title Label
        title_label = QLabel("Welcome to the Quiz App")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        title_label.setAlignment(Qt.AlignCenter)
        
        # Category selection elements
        category_label = QLabel("Select a category:")
        category_label.setFont(QFont("Arial", 14, QFont.Bold))
        category_label.setStyleSheet("color: #ffffff;")
        category_label.setAlignment(Qt.AlignCenter)
        
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(quiz_data.keys())
        self.category_dropdown.setStyleSheet("font-size: 12pt; padding: 5px;")
        
        # Start button
        start_button = QPushButton("Start Quiz")
        start_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14pt; padding: 8px;")
        start_button.clicked.connect(self.start_quiz)
        
        # Arrange widgets
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addWidget(category_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.category_dropdown, alignment=Qt.AlignCenter)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

        # Add to stack
        self.stacked_widget.addWidget(self.start_screen)

    def init_quiz_screen(self):
        """Create and style the quiz screen with a background."""
        self.quiz_screen = QWidget()
        layout = QVBoxLayout(self.quiz_screen)

        # Apply background
        self.set_background(self.quiz_screen, "kbc_background.jpg")

        # Question label
        self.question_label = QLabel(self)
        self.question_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.question_label.setStyleSheet("color: #2e4a62; padding-top: 15px;")
        self.question_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.question_label)

        # Radio buttons for options
        self.button_group = QButtonGroup(self)
        self.radio_buttons = []
        for i in range(4):
            radio_button = QRadioButton(self)
            radio_button.setStyleSheet("font-size: 12pt; padding: 5px;")
            self.radio_buttons.append(radio_button)
            self.button_group.addButton(radio_button)
            layout.addWidget(radio_button)

        # Navigation buttons: Next, Skip, Previous
        button_layout = QVBoxLayout()
        self.next_button = QPushButton("Next")
        self.next_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14pt; padding: 8px;")
        self.next_button.clicked.connect(self.next_question)
        button_layout.addWidget(self.next_button)

        self.skip_button = QPushButton("Skip")
        self.skip_button.setStyleSheet("background-color: #ff6347; color: white; font-size: 14pt; padding: 8px;")
        self.skip_button.clicked.connect(self.skip_question)
        button_layout.addWidget(self.skip_button)

        self.prev_button = QPushButton("Previous")
        self.prev_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14pt; padding: 8px;")
        self.prev_button.clicked.connect(self.previous_question)
        button_layout.addWidget(self.prev_button)

        layout.addLayout(button_layout)
        
        # Add to stack
        self.stacked_widget.addWidget(self.quiz_screen)

    def init_end_screen(self):
        """Create and style the end screen with a background."""
        self.end_screen = QWidget()
        layout = QVBoxLayout(self.end_screen)

        # Apply background
        self.set_background(self.end_screen, "end_background.jpg")

        # Final score label
        self.score_label = QLabel()
        self.score_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.score_label.setStyleSheet("color: #ffffff;")
        self.score_label.setAlignment(Qt.AlignCenter)
        
        # Restart button
        restart_button = QPushButton("Restart Quiz")
        restart_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14pt; padding: 8px;")
        restart_button.clicked.connect(self.restart_quiz)
        
        layout.addWidget(self.score_label, alignment=Qt.AlignCenter)
        layout.addWidget(restart_button, alignment=Qt.AlignCenter)

        # Add to stack
        self.stacked_widget.addWidget(self.end_screen)

    def set_background(self, widget, image_path):
        """Set background for a given widget."""
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(image_path).scaled(600, 450, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        widget.setPalette(palette)

    def start_quiz(self):
        """Start the quiz based on selected category."""
        self.category = self.category_dropdown.currentText()
        self.questions = random.sample(quiz_data[self.category], len(quiz_data[self.category]))
        self.current_question_index = 0
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.answered_questions = [None] * len(self.questions)

        self.stacked_widget.setCurrentWidget(self.quiz_screen)
        self.load_question()


def load_question(self):
    """Load the current question and options with a background."""
    # Set the background image for the quiz screen
    self.set_background(self.quiz_screen, "kbc_background.jpg")  # Use the uploaded image
    
    # Load current question data
    question_data = self.questions[self.current_question_index]
    self.question_label.setText(question_data["question"])
    
    # Set the options for the current question
    for i, option in enumerate(question_data["options"]):
        self.radio_buttons[i].setText(option)
        self.radio_buttons[i].setChecked(False)
    def next_question(self):
        """Check the answer, load the next question, or finish the quiz."""
        selected_button = self.button_group.checkedButton()
        if selected_button:
            selected_answer = selected_button.text()
            correct_answer = self.questions[self.current_question_index]["answer"]
            
            if self.answered_questions[self.current_question_index] is None:
                if selected_answer == correct_answer:
                    self.score += self.points_correct
                    self.correct_answers += 1
                else:
                    self.score += self.points_wrong
                    self.incorrect_answers += 1
                self.answered_questions[self.current_question_index] = selected_answer

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.load_question()
        else:
            self.show_score()

    def skip_question(self):
        """Skip to the next question without marking the current one."""
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.load_question()
        else:
            self.show_score()

    def previous_question(self):
        """Navigate to the previous question without re-evaluating the answer."""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.load_question()

    def show_score(self):
        """Show the final score, correct and incorrect answers count."""
        self.score_label.setText(f"Your score: {self.score}/{len(self.questions) * self.points_correct}\n"
                                 f"Correct answers: {self.correct_answers}\n"
                                 f"Incorrect answers: {self.incorrect_answers}")
        self.stacked_widget.setCurrentWidget(self.end_screen)

    def restart_quiz(self):
        """Reset the quiz to the start screen."""
        self.stacked_widget.setCurrentWidget(self.start_screen)

# Run the application
app = QApplication(sys.argv)
window = QuizApp()
window.show()
sys.exit(app.exec_())
