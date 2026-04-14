"""
Base generator class for test script generation
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from models.requirement import Requirement, TestCase


class BaseTestGenerator(ABC):
    """Abstract base class for test generators"""
    
    def __init__(self, language: str, framework: str):
        self.language = language
        self.framework = framework
    
    @abstractmethod
    def generate_tests(self, requirements: List[Requirement], test_type: str) -> List[TestCase]:
        """Generate test cases from requirements"""
        pass
    
    def _create_test_case_id(self, requirement_id: str, test_type: str, index: int) -> str:
        """Create a unique test case ID"""
        return f"{requirement_id}_{test_type}_{index:03d}"
    
    def _get_test_framework_info(self, test_type: str) -> Dict[str, str]:
        """Get framework-specific information for test type"""
        # This should be overridden by subclasses
        return {
            'unit': self.framework,
            'integration': self.framework,
            'e2e': self.framework,
            'uat': self.framework
        }.get(test_type, self.framework)