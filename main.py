#!/usr/bin/env python3
"""
PRD-to-Test-Script Generator
Main application entry point with GUI and CLI support
"""

import sys
import os
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='PRD-to-Test-Script Generator - Convert PRDs to test scripts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py sample_prd.md           # Console mode with file
  python main.py                         # Console mode (interactive)
  python main.py --gui                   # Launch GUI application
  python main.py sample_prd.md --gui     # Launch GUI (load file)

Languages: Python (pytest), Java (JUnit5), TypeScript (Jest)
        """
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='Path to PRD file (Markdown format)'
    )
    parser.add_argument(
        '--gui', '-g',
        action='store_true',
        help='Launch GUI application'
    )
    
    args = parser.parse_args()
    
    # Load file into clipboard-like state if provided
    if args.file:
        os.environ['PRD_FILE'] = args.file
    
    # Launch GUI if requested or no arguments
    if args.gui or not args.file:
        try:
            from gui.main_window import main as gui_main
            print("Launching GUI application...")
            gui_main()
            return
        except ImportError as e:
            print(f"GUI not available: {e}")
            print("Installing GUI dependencies...")
            print("Run: pip install PyQt6")
            console_main(args.file if args.file else None)
            return
    else:
        # Console mode
        console_main(args.file)


def console_main(prd_file=None):
    """Console mode test generation"""
    print("=" * 70)
    print("PRD-to-Test-Script Generator")
    print("=" * 70)
    print()
    
    # Get PRD file
    if prd_file:
        prd_path = prd_file
    else:
        prd_path = input("Enter PRD file path (or press Enter for sample): ").strip()
        if not prd_path:
            prd_path = str(project_root / "sample_prd.md")
    
    prd_path = Path(prd_path)
    if not prd_path.exists():
        print(f"Error: PRD file not found: {prd_path}")
        return
    
    try:
        # Import modules
        from parser.markdown_parser import MarkdownParser
        from generator.generator import TestGenerator
        
        # Parse PRD
        print(f"\nParsing PRD: {prd_path}")
        print("-" * 50)
        parser = MarkdownParser()
        requirements = parser.parse_file(str(prd_path))
        
        if not requirements:
            print("No requirements found in PRD file!")
            return
        
        print(f"Found {len(requirements)} requirements:")
        for req in requirements:
            print(f"  • {req.id}: {req.title}")
            print(f"    Type: {req.requirement_type.value}")
        print()
        
        # Ask for language
        print("Select target language:")
        print("  1. Python (pytest)")
        print("  2. Java (JUnit5)")
        print("  3. TypeScript (Jest)")
        print("  4. All languages")
        
        choice = input("\nYour choice [1-4]: ").strip()
        language_map = {
            '1': 'python',
            '2': 'java',
            '3': 'typescript',
            '4': 'all'
        }
        
        if choice in language_map:
            if language_map[choice] == 'all':
                languages = ['python', 'java', 'typescript']
            else:
                languages = [language_map[choice]]
        else:
            print("Invalid choice. Using Python by default.")
            languages = ['python']
        
        # Ask for test type
        print("\nSelect test type:")
        print("  1. Unit")
        print("  2. Integration")
        print("  3. E2E")
        print("  4. UAT")
        
        test_choice = input("\nYour choice [1-4]: ").strip()
        test_type_map = {
            '1': 'unit',
            '2': 'integration',
            '3': 'e2e',
            '4': 'uat'
        }
        
        test_type = test_type_map.get(test_choice, 'unit')
        
        # Generate tests
        print(f"\nGenerating {test_type} tests for: {', '.join(languages)}")
        print("-" * 50)
        
        generator = TestGenerator()
        
        for lang in languages:
            print(f"\n{'=' * 50}")
            print(f"{lang.upper()} TESTS")
            print(f"{'=' * 50}")
            
            test_cases = generator.generate_tests(requirements, lang, test_type)
            print(f"\nGenerated {len(test_cases)} test cases:")
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n[{i}/{len(test_cases)}] {test_case.name}")
                print(f"    ID: {test_case.id}")
                print(f"    Framework: {test_case.framework}")
                print("\n    Code:")
                # Show first few lines
                lines = test_case.code.strip().split('\n')
                for line in lines[:8]:
                    print(f"      {line}")
                if len(lines) > 8:
                    print(f"      ... ({len(lines) - 8} more lines)")
            
            print()
        
        print("=" * 70)
        print("Generation complete!")
        print("=" * 70)
        
    except ImportError as e:
        print(f"Error: Could not import required modules: {e}")
        print("\nMake sure you have installed the dependencies:")
        print("  pip install markdown PyYAML jinja2")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
