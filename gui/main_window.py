"""
Main application window for PRD-to-Test-Script Generator
A PyQt6 GUI that converts PRDs to test scripts
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QComboBox, QTextEdit, QGroupBox,
    QTabWidget, QMessageBox, QProgressBar, QSplitter, QListWidget,
    QCheckBox, QGroupBox, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QTextCursor, QKeySequence
from PyQt6.QtGui import QShortcut

try:
    from parser.markdown_parser import MarkdownParser
    from generator.generator import TestGenerator
    from models.requirement import RequirementType
except ImportError as e:
    print(f"Warning: Could not import generator modules: {e}")


class GeneratorWorker(QThread):
    """Background thread for generating tests to keep GUI responsive"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(list, str)
    error = pyqtSignal(str)
    
    def __init__(self, requirements, languages, test_type):
        super().__init__()
        self.requirements = requirements
        self.languages = languages
        self.test_type = test_type
    
    def run(self):
        try:
            generator = TestGenerator()
            results = {}
            
            for i, lang in enumerate(self.languages):
                self.progress.emit(i * 100 // len(self.languages), f"Generating {lang} tests...")
                test_cases = generator.generate_tests(self.requirements, lang, self.test_type)
                results[lang] = test_cases
            
            self.progress.emit(100, "Complete!")
            self.finished.emit(results, "Success")
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PRD-to-Test-Script Generator")
        self.setGeometry(100, 100, 1200, 800)
        
        # Setup UI
        self.selected_file = None
        self.parsed_requirements = []
        self.generated_tests = {}
        
        self.setup_ui()
        self.setup_shortcuts()
    
    def setup_ui(self):
        """Setup the main user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title Bar
        title_container = QWidget()
        title_layout = QHBoxLayout()
        title_container.setLayout(title_layout)
        
        title_label = QLabel("🧪 PRD-to-Test-Script Generator")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        main_layout.addWidget(title_container)
        
        # Create splitter for resizable panes
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left Panel - Input Section
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        # PRD Input Group
        input_group = QGroupBox("📄 PRD File")
        input_layout = QVBoxLayout()
        
        # File selection with browse button
        file_row = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("QLabel { color: gray; padding: 8px; border: 1px dashed #ccc; border-radius: 4px; }")
        self.file_label.setWordWrap(True)
        self.browse_btn = QPushButton("📂 Browse...")
        self.browse_btn.setMinimumWidth(100)
        self.browse_btn.clicked.connect(self.browse_file)
        self.load_sample_btn = QPushButton("📝 Load Sample")
        self.load_sample_btn.clicked.connect(self.load_sample)
        
        file_row.addWidget(self.file_label)
        file_row.addWidget(self.browse_btn)
        file_row.addWidget(self.load_sample_btn)
        input_layout.addLayout(file_row)
        
        input_group.setLayout(input_layout)
        left_layout.addWidget(input_group)
        
        # Language Selection Group
        lang_group = QGroupBox("🌐 Generate For")
        lang_layout = QVBoxLayout()
        
        self.python_check = QCheckBox("Python (pytest)")
        self.python_check.setChecked(True)
        self.java_check = QCheckBox("Java (JUnit5)")
        self.java_check.setChecked(True)
        self.ts_check = QCheckBox("TypeScript (Jest)")
        self.ts_check.setChecked(True)
        
        lang_layout.addWidget(self.python_check)
        lang_layout.addWidget(self.java_check)
        lang_layout.addWidget(self.ts_check)
        lang_group.setLayout(lang_layout)
        left_layout.addWidget(lang_group)
        
        # Test Type Selection
        type_group = QGroupBox("🧪 Test Type")
        type_layout = QVBoxLayout()
        
        self.test_type_combo = QComboBox()
        self.test_type_combo.addItems(["Unit", "Integration", "E2E", "UAT"])
        self.test_type_combo.setMinimumWidth(200)
        type_layout.addWidget(QLabel("Select test type:"))
        type_layout.addWidget(self.test_type_combo)
        type_group.setLayout(type_layout)
        left_layout.addWidget(type_group)
        
        # Generate Button
        self.generate_btn = QPushButton("⚡ Generate Tests")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3d8b40; }
            QPushButton:disabled { background-color: #cccccc; }
        """)
        self.generate_btn.clicked.connect(self.generate_tests)
        left_layout.addWidget(self.generate_btn)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        left_layout.addWidget(self.progress_bar)
        
        # Requirements List
        req_group = QGroupBox(f"📋 Requirements ({len(self.parsed_requirements)})")
        req_layout = QVBoxLayout()
        
        self.req_list = QListWidget()
        self.req_list.setMaximumWidth(300)
        self.req_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        req_layout.addWidget(self.req_list)
        req_group.setLayout(req_layout)
        left_layout.addWidget(req_group, stretch=1)
        
        left_panel_layout = QVBoxLayout()
        left_panel_layout.setContentsMargins(0, 0, 0, 0)
        left_panel_layout.addWidget(input_group)
        left_panel_layout.addWidget(lang_group)
        left_panel_layout.addWidget(type_group)
        left_panel_layout.addWidget(self.generate_btn)
        left_panel_layout.addWidget(self.progress_bar)
        left_panel_layout.addWidget(req_group)
        left_panel_layout.addStretch()
        left_panel.setLayout(left_panel_layout)
        
        # Right Panel - Output Section
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        # Output Header
        output_header = QHBoxLayout()
        output_header.addWidget(QLabel("📝 Generated Code"))
        output_header.addStretch()
        
        # Save All Button
        self.save_all_btn = QPushButton("💾 Save All")
        self.save_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:disabled { background-color: #cccccc; }
        """)
        self.save_all_btn.clicked.connect(self.save_all_tests)
        self.save_all_btn.setDisabled(True)
        output_header.addWidget(self.save_all_btn)
        
        right_layout.addLayout(output_header)
        
        # Tab Widget for different languages
        self.tabs = QTabWidget()
        
        self.python_tab = self.create_code_tab("Python", "pytest")
        self.java_tab = self.create_code_tab("Java", "JUnit5")
        self.ts_tab = self.create_code_tab("TypeScript", "Jest")
        
        self.tabs.addTab(self.python_tab, "🐍 Python")
        self.tabs.addTab(self.java_tab, "☕ Java")
        self.tabs.addTab(self.ts_tab, "📘 TypeScript")
        
        right_layout.addWidget(self.tabs, stretch=1)
        
        # Status Bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("QLabel { padding: 5px; background-color: #f0f0f0; border-radius: 4px; }")
        right_layout.addWidget(self.status_label)
        
        right_panel_layout = QVBoxLayout()
        right_panel_layout.setContentsMargins(0, 0, 0, 0)
        right_panel_layout.addWidget(self.tabs)
        right_panel_layout.addWidget(self.status_label)
        right_panel.setLayout(right_panel_layout)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # Set splitter sizes
        splitter.setSizes([350, 850])
        
        main_layout.addWidget(splitter)
    
    def create_code_tab(self, name, framework):
        """Create a code output tab for a language"""
        container = QWidget()
        layout = QVBoxLayout()
        
        # Language header
        header_label = QLabel(f"{name} Tests - {framework}")
        header_font = QFont()
        header_font.setBold(True)
        header_font.setPointSize(12)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        # Code editor
        code_edit = QTextEdit()
        code_edit.setReadOnly(True)
        code_edit.setFont(QFont("Courier New", 10))
        code_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #333;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        self.code_edit = code_edit
        layout.addWidget(code_edit)
        
        container.setLayout(layout)
        return container
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Ctrl+O: Open file
        open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        open_shortcut.activated.connect(self.browse_file)
        
        # Ctrl+G: Generate
        gen_shortcut = QShortcut(QKeySequence("Ctrl+G"), self)
        gen_shortcut.activated.connect(self.generate_tests)
        
        # Ctrl+S: Save all
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save_all_tests)
        
        # Ctrl+L: Load sample
        load_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        load_shortcut.activated.connect(self.load_sample)
    
    def browse_file(self):
        """Browse for PRD file"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select PRD File", "", "Markdown Files (*.md);;All Files (*)"
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path)
            self.file_label.setStyleSheet("QLabel { color: #333; padding: 8px; border: 1px solid #4CAF50; border-radius: 4px; background-color: #f0fff4; }")
            self.status_label.setText(f"Selected: {os.path.basename(file_path)}")
    
    def load_sample(self):
        """Load the sample PRD"""
        sample_path = str(project_root / "sample_prd.md")
        if os.path.exists(sample_path):
            self.selected_file = sample_path
            self.file_label.setText(sample_path)
            self.file_label.setStyleSheet("QLabel { color: #333; padding: 8px; border: 1px solid #4CAF50; border-radius: 4px; background-color: #f0fff4; }")
            self.status_label.setText("Loaded sample PRD")
            # Auto-parse requirements
            self.parse_requirements()
        else:
            QMessageBox.warning(self, "File Not Found", "Sample PRD file not found!")
    
    def parse_requirements(self):
        """Parse the selected PRD and show requirements"""
        try:
            parser = MarkdownParser()
            self.parsed_requirements = parser.parse_file(self.selected_file)
            
            # Update requirements list
            self.req_list.clear()
            for req in self.parsed_requirements:
                req_type_icon = "🔵" if req.requirement_type == RequirementType.FUNCTIONAL else "🟢"
                item_text = f"{req_type_icon} {req.id}: {req.title}"
                item = self.req_list.addItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, req)
            
            self.req_list.updateGeometry()
            req_group = self.findChild(QGroupBox, "")
            if req_group:
                req_group.setTitle(f"📋 Requirements ({len(self.parsed_requirements)})")
            
            self.status_label.setText(f"Parsed {len(self.parsed_requirements)} requirements")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to parse PRD: {e}")
    
    def get_selected_languages(self):
        """Get list of selected languages"""
        languages = []
        if self.python_check.isChecked():
            languages.append("python")
        if self.java_check.isChecked():
            languages.append("java")
        if self.ts_check.isChecked():
            languages.append("typescript")
        return languages
    
    def generate_tests(self):
        """Generate tests for selected languages"""
        if not self.selected_file:
            QMessageBox.warning(self, "No File Selected", "Please select a PRD file first!")
            return
        
        # Parse requirements first
        self.parse_requirements()
        
        if not self.parsed_requirements:
            QMessageBox.warning(self, "No Requirements", "No requirements found in the PRD file!")
            return
        
        languages = self.get_selected_languages()
        if not languages:
            QMessageBox.warning(self, "No Languages Selected", "Please select at least one language!")
            return
        
        test_type = self.test_type_combo.currentText()
        
        # Disable UI during generation
        self.generate_btn.setDisabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.save_all_btn.setDisabled(True)
        
        # Start background thread
        self.worker = GeneratorWorker(self.parsed_requirements, languages, test_type.lower())
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.start()
    
    def update_progress(self, value, message):
        """Update progress bar"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def on_generation_finished(self, results, status):
        """Handle generation completion"""
        self.generated_tests = results
        
        # Update tabs with code
        for lang, test_cases in results.items():
            code = self.format_code(test_cases, lang)
            if lang == "python":
                self.python_tab.code_edit.setPlainText(code)
            elif lang == "java":
                self.java_tab.code_edit.setPlainText(code)
            elif lang == "typescript":
                self.ts_tab.code_edit.setPlainText(code)
        
        # Re-enable UI
        self.generate_btn.setDisabled(False)
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.save_all_btn.setDisabled(False)
        self.status_label.setText(f"Generated {sum(len(tc) for tc in results.values())} test cases")
        
        QMessageBox.information(self, "Success", "Test generation complete!")
    
    def on_generation_error(self, error_msg):
        """Handle generation error"""
        self.generate_btn.setDisabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Error: {error_msg}")
        QMessageBox.critical(self, "Error", f"Failed to generate tests:\n{error_msg}")
    
    def format_code(self, test_cases, language):
        """Format test cases for display"""
        if not test_cases:
            return f"// No test cases generated for {language}"
        
        lines = []
        lines.append(f"# Generated {len(test_cases)} test cases")
        lines.append(f"# Framework: {self.get_framework_name(language)}")
        lines.append("")
        
        for test_case in test_cases:
            lines.append("")
            lines.append(test_case.code.strip())
            lines.append("")
            lines.append("-" * 60)
            lines.append("")
        
        return "\n".join(lines)
    
    def get_framework_name(self, lang):
        """Get framework name for language"""
        names = {
            "python": "pytest",
            "java": "JUnit5",
            "typescript": "Jest"
        }
        return names.get(lang, lang)
    
    def save_all_tests(self):
        """Save all generated tests to files"""
        if not self.generated_tests:
            QMessageBox.warning(self, "No Tests", "No tests generated yet!")
            return
        
        save_folder = QFileDialog.getExistingDirectory(
            self, "Select folder to save tests", ""
        )
        if not save_folder:
            return
        
        try:
            for lang, test_cases in self.generated_tests.items():
                filename = f"{lang}_tests.py" if lang == "python" else \
                          f"{lang}_tests.java" if lang == "java" else \
                          f"{lang}_tests.ts"
                
                filepath = os.path.join(save_folder, filename)
                code = self.format_code(test_cases, lang)
                
                with open(filepath, 'w') as f:
                    f.write(code)
            
            QMessageBox.information(self, "Success", f"Tests saved to:\n{save_folder}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save tests:\n{e}")


def main():
    """Entry point for the GUI application"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Set palette for better colors
    from PyQt6.QtGui import QPalette, QColor
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
