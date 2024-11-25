import matplotlib.pyplot as plt
import random
import sys
from quiz_data import quiz_data  # Assuming your quiz data is available here.
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QRadioButton,
    QPushButton, QButtonGroup, QComboBox, QStackedWidget
)
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt, QTimer
import os

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Quiz Application")
        self.setGeometry(100, 100, 1400, 700)

        self.stacked_widget = QStackedWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)

        self.current_question_index = 0
        self.score = 0
        self.category = ""
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.not_attempted = 0  # Track the number of unanswered questions

        self.points_correct = 4
        self.points_wrong = -1
        self.answered_questions = [None] * 5  # Track answered questions
        self.time_up_questions = [False] * 5  # Track if time is up for a question
        self.time_remaining_questions = [30] * 5  # Track remaining time for each question

        # Timer Initialization
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.init_start_screen()
        self.init_quiz_screen()
        self.init_end_screen()
        self.stacked_widget.setCurrentWidget(self.start_screen)

    def init_start_screen(self):
        self.start_screen = QWidget()
        layout = QVBoxLayout(self.start_screen)

        self.set_background(self.start_screen, "kbc_background.jpg")

        title_label = QLabel("Welcome to the Quiz App")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        title_label.setAlignment(Qt.AlignCenter)

        category_label = QLabel("Select a category:")
        category_label.setFont(QFont("Arial", 14, QFont.Bold))
        category_label.setStyleSheet("color: #ffffff;")
        category_label.setAlignment(Qt.AlignCenter)

        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(quiz_data.keys())
        self.category_dropdown.setStyleSheet("font-size: 12pt; padding: 5px;")

        start_button = QPushButton("Start Quiz")
        start_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14pt; padding: 8px;")
        start_button.clicked.connect(self.start_quiz)

        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addWidget(category_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.category_dropdown, alignment=Qt.AlignCenter)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)
        self.stacked_widget.addWidget(self.start_screen)

    def init_quiz_screen(self):
        self.quiz_screen = QWidget()
        layout = QVBoxLayout(self.quiz_screen)

        self.set_background(self.quiz_screen, "kbc_background.jpg")

        self.question_label = QLabel(self)
        self.question_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.question_label.setStyleSheet("color: #2e4a62; padding-top: 15px;")
        self.question_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.question_label)

        self.button_group = QButtonGroup(self)
        self.radio_buttons = []
        for i in range(4):
            radio_button = QRadioButton(self)
            radio_button.setStyleSheet("font-size: 12pt; padding: 5px;")
            self.radio_buttons.append(radio_button)
            self.button_group.addButton(radio_button)
            layout.addWidget(radio_button)

        # Timer Label (added to quiz screen)
        self.timer_label = QLabel("Time Left: 30s")
        self.timer_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.timer_label.setStyleSheet("color: #ff4500; padding: 5px;")
        self.timer_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.timer_label)

        button_layout = QVBoxLayout()
        self.next_button = QPushButton("Next")
        self.next_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14pt; padding: 8px;")
        self.next_button.clicked.connect(self.next_question)
        button_layout.addWidget(self.next_button)

        self.skip_button = QPushButton("Skip")
        self.skip_button.setStyleSheet("background-color: #f39c12; color: white; font-size: 14pt; padding: 8px;")
        self.skip_button.clicked.connect(self.skip_question)  # Skip the question when clicked
        button_layout.addWidget(self.skip_button)

        self.prev_button = QPushButton("Previous")
        self.prev_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14pt; padding: 8px;")
        self.prev_button.clicked.connect(self.previous_question)
        button_layout.addWidget(self.prev_button)

        layout.addLayout(button_layout)
        self.stacked_widget.addWidget(self.quiz_screen)

    def init_end_screen(self):
        self.end_screen = QWidget()
        layout = QVBoxLayout(self.end_screen)

        self.set_background(self.end_screen, "end_background.jpg")

        self.score_label = QLabel()
        self.score_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.score_label.setStyleSheet("color: #ffffff;")
        self.score_label.setAlignment(Qt.AlignCenter)

        self.pie_chart_label = QLabel()
        self.pie_chart_label.setAlignment(Qt.AlignCenter)

        restart_button = QPushButton("Restart Quiz")
        restart_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14pt; padding: 8px;")
        restart_button.clicked.connect(self.restart_quiz)

        layout.addWidget(self.score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.pie_chart_label, alignment=Qt.AlignCenter)
        layout.addWidget(restart_button, alignment=Qt.AlignCenter)
        self.stacked_widget.addWidget(self.end_screen)

    def set_background(self, widget, image_path):
        """Set background for a given widget."""
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(image_path).scaled(1400, 700, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        widget.setAutoFillBackground(True)
        widget.setPalette(palette)

    def start_quiz(self):
        self.category = self.category_dropdown.currentText()
        self.questions = random.sample(quiz_data[self.category], len(quiz_data[self.category]))
        self.current_question_index = 0
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.not_attempted = 0  # Reset not attempted counter
        self.answered_questions = [None] * len(self.questions)
        self.time_up_questions = [False] * len(self.questions)  # Reset time-up tracking
        self.time_remaining_questions = [30] * len(self.questions)  # Reset remaining time

        self.stacked_widget.setCurrentWidget(self.quiz_screen)
        self.load_question()

    def load_question(self):
        question_data = self.questions[self.current_question_index]
        self.question_label.setText(question_data["question"])

        # Reset radio button selection for every new question
        for i in range(4):
            self.radio_buttons[i].setChecked(False)  # Uncheck all radio buttons for the new question
            self.radio_buttons[i].setEnabled(True)  # Enable all radio buttons for the current question

        # Set the new options
        for i, option in enumerate(question_data["options"]):
            self.radio_buttons[i].setText(option)

        # If the time for this question has expired, show "Time Over"
        if self.time_up_questions[self.current_question_index]:
            self.timer_label.setText("Time Over")
            for radio_button in self.radio_buttons:
                radio_button.setDisabled(True)  # Disable interaction for this question
            self.timer.stop()  # Ensure timer doesn't restart
        else:
            self.time_remaining = self.time_remaining_questions[self.current_question_index]  # Use stored time
            self.timer_label.setText(f"Time Left: {self.time_remaining}s")
            self.timer.start(1000)  # Start the timer for this question

    def update_timer(self):
        """Update the timer and handle time out."""
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.setText(f"Time Left: {self.time_remaining}s")
            self.time_remaining_questions[self.current_question_index] = self.time_remaining  # Update remaining time
        else:
            self.timer_label.setText("Time Over")
            self.time_up_questions[self.current_question_index] = True  # Mark question as time-up
            self.next_question()  # Automatically move to the next question

    def next_question(self):
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
            else:
                self.not_attempted += 1  # Count unanswered questions as not attempted

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.load_question()
        else:
            self.timer.stop()  # Stop the timer when the quiz ends
            self.show_score()

    def skip_question(self):
        """Skip the current question and mark it as 'Not Attempted'."""
        self.not_attempted += 1  # Mark the question as not attempted
        self.current_question_index += 1  # Move to the next question
        if self.current_question_index < len(self.questions):
            self.load_question()
        else:
            self.show_score()

    def previous_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.load_question()

    def show_score(self):
        self.score_label.setText(f"Your score: {self.score}\n"
                                 f"Correct answers: {self.correct_answers}\n"
                                 f"Incorrect answers: {self.incorrect_answers}\n"
                                 f"Not attempted: {self.not_attempted}")
        self.display_pie_chart()
        self.stacked_widget.setCurrentWidget(self.end_screen)

    def display_pie_chart(self):
        labels = ['Correct', 'Incorrect', 'Not Attempted']
        sizes = [self.correct_answers, self.incorrect_answers, self.not_attempted]
        colors = ['#0000FF', '#FF0000', '#808080']  # Blue for correct, Red for incorrect, Grey for not attempted
        explode = (0.1, 0, 0)  # Highlight correct answers

        plt.figure(figsize=(4, 4))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')

        pie_chart_file = 'pie_chart.png'
        plt.savefig(pie_chart_file)
        plt.close()

        pixmap = QPixmap(pie_chart_file)
        self.pie_chart_label.setPixmap(pixmap)
        os.remove(pie_chart_file)  # Remove the temporary file after displaying

    def restart_quiz(self):
        self.stacked_widget.setCurrentWidget(self.start_screen)


# Main loop to start the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())
