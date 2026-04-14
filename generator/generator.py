"""
Generator engine that coordinates test script generation
"""

from typing import List, Dict, Any
from models.requirement import Requirement, TestCase
from .base_generator import BaseTestGenerator
from .python.python_generator import PythonTestGenerator
from .java.java_generator import JavaTestGenerator
from .typescript.ts_generator import TypeScriptTestGenerator


class TestGenerator:
    """Main test generator that coordinates language-specific generators"""
    
    def __init__(self):
        self.generators = {
            "python": PythonTestGenerator(),
            "java": JavaTestGenerator(),
            "typescript": TypeScriptTestGenerator()
        }
    
    def generate_tests(self, requirements: List[Requirement], language: str, test_type: str) -> List[TestCase]:
        """Generate test cases for the specified language and test type"""
        language = language.lower()
        
        if language not in self.generators:
            raise ValueError(f"Unsupported language: {language}. Supported languages: {list(self.generators.keys())}")
        
        generator = self.generators[language]
        return generator.generate_tests(requirements, test_type)
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return list(self.generators.keys())
    
    def get_generator_info(self, language: str) -> Dict[str, str]:
        """Get information about a specific generator"""
        language = language.lower()
        if language not in self.generators:
            raise ValueError(f"Unsupported language: {language}")
        
        generator = self.generators[language]
        return {
            "language": generator.language,
            "framework": generator.framework
        }