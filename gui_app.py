import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QLineEdit, QScrollArea
)
from PySide6.QtWidgets import QTextBrowser
import markdown
from PySide6.QtCore import Qt
from get_response_gemeni import AskGemeni

class AIQAApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ask AI - Q&A")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6f8;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                background-color: #fff;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.question_label = QLabel("What do you want to know about AUTOSAR ?")
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Type your question here...")

        self.ask_button = QPushButton("Ask")
        self.ask_button.clicked.connect(self.ask_ai)

        self.answer_label = QLabel("Answer:")
        self.answer_output = QTextBrowser()
        self.answer_output.setReadOnly(True)
        self.answer_output.setPlaceholderText("AI response will appear here...")

        layout.addWidget(self.question_label)
        layout.addWidget(self.question_input)
        layout.addWidget(self.ask_button)
        layout.addWidget(self.answer_label)
        layout.addWidget(self.answer_output)

        self.setLayout(layout)

    def ask_ai(self):
        question = self.question_input.text().strip()
        if not question:
            self.answer_output.setPlainText("Please enter a question.")
            return
        try:
            response_md = AskGemeni(question)
            response_html = markdown.markdown(response_md)
            self.answer_output.setHtml(response_html)
        except Exception as e:
            self.answer_output.setPlainText(f"Error: {str(e)}")
        finally:
            self.question_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIQAApp()
    window.show()
    sys.exit(app.exec())
