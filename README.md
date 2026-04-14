# PRD Test Generator

Automatically generate test scripts from Product Requirements Documents (PRDs). This tool parses Markdown PRD files and generates unit, integration, E2E, and UAT test cases for Python (pytest), Java (JUnit5), and TypeScript (Jest).

## Features

- 📄 **Markdown PRD Parser**: Extract requirements from structured Markdown documents
- 🐍 **Multi-language Support**: Generate tests in Python, Java, and TypeScript
- 🧪 **Multiple Test Types**: Unit, Integration, E2E, and UAT tests
- 🎯 **Framework Integration**: pytest, JUnit5, and Jest test frameworks
- 🖥️ **GUI & CLI**: Desktop application or command-line interface
- 🔌 **Extensible Architecture**: Easy to add new languages and test frameworks

## Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/prd-test-generator.git
cd prd-test-generator
source venv/bin/activate
pip install -r requirements.txt

# Run with sample PRD
python main.py sample_prd.md

# Or use the GUI (requires system dependencies)
python main.py --gui
```

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment support

### Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `markdown` - Parse Markdown PRD files
- `PyYAML` - YAML parsing support
- `jinja2` - Template rendering (for future enhancements)
- `PyQt6` - GUI application (optional, for desktop mode)

## Usage

### Command Line

```bash
# Basic usage with sample PRD
python main.py sample_prd.md

# Run in console mode (default)
python main.py

# Try GUI mode (may require additional system libraries)
python main.py --gui
```

### Programmatic Usage

```python
from parser.markdown_parser import MarkdownParser
from generator.generator import TestGenerator

# Parse PRD
parser = MarkdownParser()
requirements = parser.parse_file('path/to/prd.md')

# Generate tests
generator = TestGenerator()
test_cases = generator.generate_tests(
    requirements=requirements,
    language='python',  # 'python', 'java', or 'typescript'
    test_type='unit'    # 'unit', 'integration', 'e2e', 'uat'
)

# Access generated tests
for test_case in test_cases:
    print(f"{test_case.name}:")
    print(test_case.code)
```

## PRD Format

Requirements should be formatted in Markdown with the following structure:

```markdown
# Product Requirements Document

## Functional Requirements

### REQ-001 User Login
The system shall allow users to log in using their email and password.

### REQ-002 Data Validation
The system shall validate user input to prevent SQL injection attacks.

## Non-Functional Requirements

### NFR-001 Performance
The system shall respond to user requests within 2 seconds.

### NFR-002 Security
All sensitive data shall be encrypted using AES-256 encryption.
```

Supported requirement prefixes:
- `REQ` - Standard requirement
- `FR` - Functional requirement
- `NFR` - Non-functional requirement
- `REQUIREMENT` - Alternative prefix

## Project Structure

```
prd-test-generator/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── sample_prd.md          # Sample PRD file
├── parser/
│   └── markdown_parser.py  # PRD parsing logic
├── generator/
│   ├── base_generator.py   # Abstract base class
│   ├── generator.py        # Test generation coordinator
│   ├── python/
│   │   └── python_generator.py  # Python test generator
│   ├── java/
│   │   └── java_generator.py    # Java test generator
│   └── typescript/
│       └── ts_generator.py      # TypeScript test generator
├── models/
│   └── requirement.py      # Data models
├── gui/
│   └── main_window.py      # PyQt6 GUI
└── templates/              # Code templates (for future)
```

## Generated Test Examples

### Python (pytest)
```python
def test_req_001_unit():
    """### REQ-001 User Login"""
    # Arrange
    # TODO: Set up test prerequisites
    
    # Act
    # TODO: Execute the functionality being tested
    
    # Assert
    # TODO: Verify the expected outcome
    assert True, "Test not yet implemented"
```

### Java (JUnit5)
```java
@Test
void testReq_001Unit() {
    // ### REQ-001 User Login
    
    // Arrange
    // TODO: Set up test prerequisites
    
    // Act
    // TODO: Execute the functionality being tested
    
    // Assert
    // TODO: Verify the expected outcome
    org.junit.jupiter.api.Assertions.assertTrue(true, "Test not yet implemented");
}
```

### TypeScript (Jest)
```typescript
test('req_001 unit', () => {
    // ### REQ-001 User Login
    
    // Arrange
    // TODO: Set up test prerequisites
    
    // Act
    // TODO: Execute the functionality being tested
    
    // Assert
    // TODO: Verify the expected outcome
    expect(true).toBe(true);
});
```

## Extending the Generator

### Adding a New Language

1. Create `generator/<lang>/<lang>_generator.py`:
```python
from ..base_generator import BaseTestGenerator

class MyLangTestGenerator(BaseTestGenerator):
    def __init__(self):
        super().__init__('mylang', 'myframework')
    
    def generate_tests(self, requirements, test_type):
        # Implement test generation
        pass
```

2. Register in `generator/generator.py`:
```python
from .mylang.mylang_generator import MyLangTestGenerator

self.generators = {
    'mylang': MyLangTestGenerator(),
    # ...
}
```

### Adding Test Types

Add methods to each language generator:
```python
def _generate_e2e_test(self, requirement, clean_req_id):
    # Generate E2E test code
    pass
```

## Development

### Testing

```bash
# Run tests (when available)
python -m pytest tests/
```

### Adding New Features

1. Create a feature branch:
```bash
git checkout -b feature/new-language
```

2. Make changes and commit:
```bash
git add .
git commit -m "Add support for Go testing framework"
```

3. Push and create PR:
```bash
git push origin feature/new-language
```

## Troubleshooting

### Parser Not Finding Requirements
- Ensure requirement lines use proper Markdown headers (#)
- Check that requirement IDs use supported prefixes (REQ, FR, NFR)
- Verify PRD file encoding is UTF-8

### GUI Not Starting
- Install system dependencies:
  ```bash
  sudo apt-get install libegl1-mesa libxcb-xinerama0 \
      libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
      libxcb-randr0 libxcb-render-util0 libxcb-shape0 \
      libxcb-shm0 libxcb-sync1 libxcb-xfixes0 \
      libxcb-xkb1 libxcomposite1 libxcursor1 \
      libxdamage1 libxfixes3 libxi6 libxrandr2 \
      libxrender1 libxtst6 libxss1 libnss3 libasound2
  ```

### Test Generation Issues
- Check that requirements were parsed successfully (look for "Found X requirements")
- Verify language parameter is one of: python, java, typescript
- Check console output for error messages

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Test frameworks: pytest, JUnit5, Jest
- Python ecosystem for making this possible
- All contributors to open-source testing tools

## Future Enhancements

- [ ] Template-based code generation
- [ ] More sophisticated requirement extraction
- [ ] Support for additional test frameworks
- [ ] Visual test case mapping in GUI
- [ ] Test execution and result reporting
- [ ] CI/CD integration
- [ ] Custom test template support
- [ ] Export to various formats (XML, JSON)
