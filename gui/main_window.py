"""
Main application window for PRD-to-Test-Script Generator
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QComboBox, QTextEdit,
    QGroupBox, QFormLayout, QTabWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PRD-to-Test-Script Generator")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title_label = QLabel("PRD-to-Test-Script Generator")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Input section
        input_group = QGroupBox("PRD Input")
        input_layout = QFormLayout()
        input_group.setLayout(input_layout)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setStyleSheet("border: 1px solid gray; padding: 5px;")
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(self.file_path_label, 3)
        file_layout.addWidget(self.browse_button, 1)
        input_layout.addRow("PRD File:", file_layout)
        
        # Language selection
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Python", "Java", "TypeScript"])
        input_layout.addRow("Target Language:", self.language_combo)
        
        # Test type selection
        self.test_type_combo = QComboBox()
        self.test_type_combo.addItems(["Unit", "Integration", "E2E", "UAT"])
        input_layout.addRow("Test Type:", self.test_type_combo)
        
        main_layout.addWidget(input_group)
        
        # Generate button
        self.generate_button = QPushButton("Generate Test Scripts")
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.generate_button.clicked.connect(self.generate_tests)
        main_layout.addWidget(self.generate_button)
        
        # Output section
        output_group = QGroupBox("Generated Output")
        output_layout = QVBoxLayout()
        output_group.setLayout(output_layout)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Courier", 10))
        output_layout.addWidget(self.output_text)
        
        main_layout.addWidget(output_group)
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
        
        # Initialize
        self.selected_file = None
    
    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, 
            "Select PRD File", 
            "", 
            "Markdown Files (*.md);;All Files (*)"
        )
        if file_path:
            self.selected_file = file_path
            self.file_path_label.setText(file_path)
            self.status_bar.showMessage(f"Selected: {file_path}")
    
    def generate_tests(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Warning", "Please select a PRD file first!")
            return
        
        language = self.language_combo.currentText()
        test_type = self.test_type_combo.currentText()
        
        # For now, show a placeholder - real generation will come later
        output = f"""
PRD-to-Test-Script Generator
============================

Selected PRD: {self.selected_file}
Target Language: {language}
Test Type: {test_type}

This is a placeholder output. 
The actual test generation logic will be implemented in later phases.

Next steps to implement:
1. Markdown PRD parser
2. Requirement extraction logic
3. Test case generation engine
4. Template-based test script generation
        """
        
        self.output_text.setPlainText(output.strip())
        self.status_bar.showMessage(f"Generated {language} {test_type} tests (placeholder)")


def main():
    """Entry point for the GUI application"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()