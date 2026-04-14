# PRD Test Generator - GUI User Guide

## 🚀 Quick Start

### Option 1: Run GUI Directly

```bash
cd /home/mark/prd-test-generator
source venv/bin/activate
python3 main.py --gui
```

### Option 2: Run with PRD File

```bash
cd /home/mark/prd-test-generator
source venv/bin/activate
python3 main.py sample_prd.md --gui
```

### Option 3: Launch CLI First, Then GUI

```bash
cd /home/mark/prd-test-generator
source venv/bin/activate
python3 main.py                    # Console mode
python3 main.py --gui              # Launch GUI instead
```

---

## 📖 GUI Features

### Left Panel - Input

1. **PRD File**
   - Click "Browse..." to select a PRD file
   - Click "Load Sample" to use the included sample
   - OR drag & drop a file (if supported)

2. **Generate For**
   - ☑ Python (pytest)
   - ☑ Java (JUnit5)
   - ☑ TypeScript (Jest)
   - Check/uncheck languages as needed

3. **Test Type**
   - Unit
   - Integration
   - E2E
   - UAT

4. **Generate Tests**
   - Click to start generation
   - Progress bar shows status
   - Requirements list shows parsed items

5. **Requirements**
   - See all extracted requirements
   - Blue circle: Functional requirement
   - Green circle: Non-functional requirement

### Right Panel - Output

1. **Tabbed View**
   - Python tab: pytest tests
   - Java tab: JUnit5 tests
   - TypeScript tab: Jest tests

2. **Code Display**
   - Dark theme for readability
   - Syntax highlighting (basic)
   - Scrollable for long code

3. **Save All**
   - Export all generated tests
   - Choose destination folder
   - Saves as separate files per language

---

## 🎹 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+O | Open file |
| Ctrl+L | Load sample PRD |
| Ctrl+G | Generate tests |
| Ctrl+S | Save all tests |

---

## 📁 File Formats

### PRD Requirements

```markdown
# My Product Requirements

## Functional Requirements

### REQ-001 Login Feature
The system shall allow users to log in.

### REQ-002 Search Feature
The system shall allow users to search.

## Non-Functional Requirements

### NFR-001 Performance
The system shall respond in under 2 seconds.
```

### Generated Test Files

- `python_tests.py` - Python pytest tests
- `java_tests.java` - Java JUnit5 tests
- `typescript_tests.ts` - TypeScript Jest tests

---

## 🔧 System Requirements

### Required
- Python 3.8+
- PyQt6 6.4+

### Dependencies (automatically installed)
```
markdown>=3.4.0
PyYAML>=6.0
jinja2>=3.1
PyQt6>=6.4
```

### GUI Libraries (Linux)
```bash
sudo apt-get install libegl1 libxcb-cursor0 libxcb-icccm4 \
    libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 \
    libxcb-shape0 libxcomposite1 libxcursor1 libxdamage1 \
    libxi6 libxrandr2 libxtst6 libxss1 libasound2
```

---

## 💡 Tips

1. **Start with sample**: Click "Load Sample" to see how it works
2. **Check requirements**: Review parsed requirements before generating
3. **Save early**: Click "Save All" after generating tests
4. **Customize templates**: Edit generator templates for your needs
5. **Combine modes**: Use console for quick tests, GUI for production

---

## 🐛 Troubleshooting

### "No module named 'PyQt6'"
```bash
pip install PyQt6
```

### "libEGL.so.1: cannot open shared object file"
```bash
# Linux
sudo apt-get install libegl1

# macOS
brew install qt
```

### "No display found"
- Make sure you're on a system with a display server
- For remote sessions, enable X11 forwarding: `ssh -X user@host`
- Use VNC or remote desktop

### GUI opens but stays blank
- Check system logs: `journalctl -xe`
- Verify GPU drivers are working
- Try updating PyQt6: `pip install --upgrade PyQt6`

---

## 📚 Console Mode

For quick testing without GUI:

```bash
# Interactive console mode
python3 main.py

# With specific PRD file
python3 main.py my-prd.md

# Choose language manually
python3 main.py
# Enter: my-prd.md
# Enter: 4 (All languages)
# Enter: 1 (Unit tests)
```

---

## 🔗 Links

- **GitHub**: https://github.com/mrwmrw01/prd-test-generator
- **Sample PRD**: sample_prd.md
- **README**: README.md
- **Project Summary**: PROJECT_SUMMARY.md

---

## 🎉 Enjoy!

The PRD-to-Test-Script Generator makes writing tests effortless. 
Just add your requirements and let the tool generate everything!
