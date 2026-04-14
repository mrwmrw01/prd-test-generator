"""
Java test generator for creating test scripts from requirements
"""

from typing import List, Dict, Any
from ..base_generator import BaseTestGenerator
from models.requirement import Requirement, TestCase, TestType


class JavaTestGenerator(BaseTestGenerator):
    """Generates Java test scripts using JUnit"""
    
    def __init__(self):
        super().__init__("java", "junit5")
    
    def generate_tests(self, requirements: List[Requirement], test_type: str) -> List[TestCase]:
        """Generate Java test cases from requirements"""
        test_cases = []
        
        # Map test type string to TestType enum
        test_type_map = {
            "unit": TestType.UNIT,
            "integration": TestType.INTEGRATION,
            "e2e": TestType.E2E,
            "uat": TestType.UAT
        }
        
        test_type_enum = test_type_map.get(test_type.lower(), TestType.UNIT)
        
        for i, req in enumerate(requirements):
            # Generate test case based on requirement and test type
            test_case = self._generate_test_for_requirement(req, test_type_enum, i)
            test_cases.append(test_case)
        
        return test_cases
    
    def _generate_test_for_requirement(self, requirement: Requirement, test_type: TestType, index: int) -> TestCase:
        """Generate a single test case for a requirement"""
        test_id = self._create_test_case_id(requirement.id, test_type.value, index)
        
        # Generate test name (Java convention: method names in camelCase)
        clean_req_id = requirement.id.lower().replace("-", "_")
        test_name = f"test{clean_req_id.capitalize()}{test_type.value.capitalize()}"
        
        # Generate test description
        description = f"{test_type.value.title()} test for {requirement.title}"
        
        # Generate test code based on test type
        code = self._generate_test_code(requirement, test_type, clean_req_id)
        
        return TestCase(
            id=test_id,
            requirement_id=requirement.id,
            test_type=test_type,
            name=test_name,
            description=description,
            language=self.language,
            framework=self.framework,
            code=code
        )
    
    def _generate_test_code(self, requirement: Requirement, test_type: TestType, clean_req_id: str) -> str:
        """Generate the actual test code"""
        if test_type == TestType.UNIT:
            return self._generate_unit_test(requirement, clean_req_id)
        elif test_type == TestType.INTEGRATION:
            return self._generate_integration_test(requirement, clean_req_id)
        elif test_type == TestType.E2E:
            return self._generate_e2e_test(requirement, clean_req_id)
        elif test_type == TestType.UAT:
            return self._generate_uat_test(requirement, clean_req_id)
        else:
            return self._generate_unit_test(requirement, clean_req_id)  # Default
    
    def _generate_unit_test(self, requirement: Requirement, clean_req_id: str) -> str:
        """Generate a unit test"""
        return f"""    @Test
    void test{clean_req_id.capitalize()}Unit() {{
        // {requirement.description}
        
        // Arrange
        // TODO: Set up test prerequisites
        
        // Act
        // TODO: Execute the functionality being tested
        
        // Assert
        // TODO: Verify the expected outcome
        org.junit.jupiter.api.Assertions.assertTrue(true, "Test not yet implemented");
    }}

"""
    
    def _generate_integration_test(self, requirement: Requirement, clean_req_id: str) -> str:
        """Generate an integration test"""
        return f"""    @Test
    void test{clean_req_id.capitalize()}Integration() {{
        // {requirement.description}
        
        // Arrange
        // TODO: Set up integrated components
        
        // Act
        // TODO: Execute the integrated functionality
        
        // Assert
        // TODO: Verify the integrated outcome
        org.junit.jupiter.api.Assertions.assertTrue(true, "Test not yet implemented");
    }}

"""
    
    def _generate_e2e_test(self, requirement: Requirement, clean_req_id: str) -> str:
        """Generate an end-to-end test"""
        return f"""    @Test
    void test{clean_req_id.capitalize()}E2E() {{
        // {requirement.description}
        
        // Arrange
        // TODO: Set up test environment and data
        
        // Act
        // TODO: Execute the end-to-end user flow
        
        // Assert
        // TODO: Verify the expected user outcome
        org.junit.jupiter.api.Assertions.assertTrue(true, "Test not yet implemented");
    }}

"""
    
    def _generate_uat_test(self, requirement: Requirement, clean_req_id: str) -> str:
        """Generate a user acceptance test"""
        return f"""    @Test
    void test{clean_req_id.capitalize()}Uat() {{
        // {requirement.description}
        
        // Arrange
        // TODO: Set up user scenario and test data
        
        // Act
        // TODO: Execute the user acceptance scenario
        
        // Assert
        // TODO: Verify the user acceptance criteria
        org.junit.jupiter.api.Assertions.assertTrue(true, "Test not yet implemented");
    }}

"""