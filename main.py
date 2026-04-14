#!/usr/bin/env python3
"""
PRD-to-Test-Script Generator
Main application entry point
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    # Check if we should try GUI or use console
    use_gui = len(sys.argv) > 1 and sys.argv[1] == "--gui"
    
    if use_gui:
        try:
            # Import and run the GUI application
            from gui.main_window import main as gui_main
            gui_main()
            return
        except ImportError as e:
            print(f"GUI not available: {e}")
            print("Falling back to console mode...")
            print("To use GUI, install system dependencies: libegl1-mesa and related libraries")
    
    # Console mode
    console_main()

def console_main():
    print("PRD-to-Test-Script Generator")
    print("============================")
    print("A GUI application that converts PRDs to test scripts")
    print("(Running in console mode - GUI requires additional system dependencies)")
    print()
    
    # Show current directory
    print(f"Working directory: {os.getcwd()}")
    
    # List project structure
    project_root = Path('.')
    print("\nProject structure:")
    for item in sorted(project_root.rglob('*'), key=lambda p: (not p.is_dir(), str(p))):
        if any(part.startswith('.') for part in item.parts if part != '.'):
            continue  # Skip hidden directories except current
        indent = "  " * len(item.relative_to(project_root).parts)
        if item.is_dir():
            print(f"{indent}📁 {item.name}/")
        else:
            print(f"{indent}📄 {item.name}")
    
    print("\n" + "="*50)
    print("NEXT STEPS FOR DEVELOPMENT:")
    print("="*50)
    print("1. Install system dependencies for GUI:")
    print("   sudo apt-get install libegl1-mesa libxcb-xinerama0 libxcb-icccm4 libxcb-image0")
    print("   libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-shm0")
    print("   libxcb-sync1 libxcb-xfixes0 libxcb-xinerame0 libxcb-xkb1 libxcomposite1")
    print("   libxcursor1 libxdamage1 libxfixes3 libxi6 libxrandr2 libxrender1 libxtst6")
    print("   libxss1 libnss3 libasound2")
    print()
    print("2. Or use console mode for development:")
    print("   python main.py          # Console mode")
    print("   python main.py --gui    # Try GUI mode")
    print()
    print("3. Implement core components:")
    print("   - Markdown PRD parser (parser/)")
    print("   - Test generation templates (templates/)")
    print("   - Requirement and test case models (models/)")
    print("   - Generator engine (generator/)")
    print()
    
    # Show what's implemented so far
    print("\nCURRENTLY IMPLEMENTED:")
    print("- Project structure")
    print("- Requirements file (markdown, PyYAML, jinja2, PyQt6)")
    print("- Data models for requirements and test cases")
    print("- GUI main window (requires PyQt6 + system libs)")
    print("- Console fallback mode")
    print("- Markdown PRD parser (basic)")
    print("- Test generators for Python, Java, and TypeScript")
    
    # Demo the generator if a PRD file is provided
    if len(sys.argv) > 2 and sys.argv[1] != "--gui":
        demo_generation(sys.argv[1])

def demo_generation(prd_file_path):
    """Demo the test generation with a sample PRD file"""
    print("\n" + "="*50)
    print("TEST GENERATION DEMO:")
    print("="*50)
    
    try:
        # Import required modules
        from parser.markdown_parser import MarkdownParser
        from generator.generator import TestGenerator
        
        # Check if file exists
        prd_path = Path(prd_file_path)
        if not prd_path.exists():
            print(f"PRD file not found: {prd_file_path}")
            print("Creating a sample PRD for demonstration...")
            create_sample_prd(prd_path)
        
        # Parse the PRD
        parser = MarkdownParser()
        requirements = parser.parse_file(str(prd_path))
        
        if not requirements:
            print("No requirements found in the PRD file.")
            return
        
        print(f"Found {len(requirements)} requirements:")
        for req in requirements:
            print(f"  - {req.id}: {req.title}")
        
        # Generate tests for each language
        generator = TestGenerator()
        languages = generator.get_supported_languages()
        
        for language in languages:
            print(f"\n--- Generating {language.upper()} tests ---")
            try:
                test_cases = generator.generate_tests(requirements, language, "unit")
                for test_case in test_cases:
                    print(f"\n{test_case.name}:")
                    print(f"  Description: {test_case.description}")
                    print(f"  Framework: {test_case.framework}")
                    print("  Code:")
                    # Indent the code for better readability
                    indented_code = "\n  ".join(test_case.code.split("\n"))
                    print(f"  {indented_code}")
            except Exception as e:
                print(f"Error generating {language} tests: {e}")
                
    except ImportError as e:
        print(f"Could not import required modules for demo: {e}")
    except Exception as e:
        print(f"Error during demo: {e}")

def create_sample_prd(file_path):
    """Create a sample PRD file for demonstration"""
    sample_content = """# Sample Product Requirements Document

## Functional Requirements

### REQ-001 User Login
The system shall allow users to log in using their email and password.

### REQ-002 Data Validation
The system shall validate user input to prevent SQL injection attacks.

### REQ-003 Report Generation
The system shall generate monthly reports in PDF format.

## Non-Functional Requirements

### NFR-001 Performance
The system shall respond to user requests within 2 seconds under normal load.

### NFR-002 Security
All sensitive data shall be encrypted using AES-256 encryption.
"""
    
    try:
        with open(file_path, 'w') as f:
            f.write(sample_content)
        print(f"Created sample PRD at: {file_path}")
    except Exception as e:
        print(f"Could not create sample PRD: {e}")

if __name__ == "__main__":
    main()