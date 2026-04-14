"""
Data models for PRD requirements and test cases
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class RequirementType(Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non-functional"


class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    UAT = "uat"


@dataclass
class Requirement:
    """Represents a single requirement extracted from a PRD"""
    id: str
    title: str
    description: str
    requirement_type: RequirementType
    acceptance_criteria: List[str] = field(default_factory=list)
    priority: str = "medium"  # high, medium, low
    tags: List[str] = field(default_factory=list)
    source_location: Optional[str] = None  # e.g., "PRD.md:15-25"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "requirement_type": self.requirement_type.value,
            "acceptance_criteria": self.acceptance_criteria,
            "priority": self.priority,
            "tags": self.tags,
            "source_location": self.source_location
        }


@dataclass
class TestCase:
    """Represents a generated test case"""
    id: str
    requirement_id: str
    test_type: TestType
    name: str
    description: str
    language: str  # python, java, typescript
    framework: str  # pytest, junit, jest, etc.
    code: str
    setup_code: str = ""
    teardown_code: str = ""
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "requirement_id": self.requirement_id,
            "test_type": self.test_type.value,
            "name": self.name,
            "description": self.description,
            "language": self.language,
            "framework": self.framework,
            "code": self.code,
            "setup_code": self.setup_code,
            "teardown_code": self.teardown_code,
            "dependencies": self.dependencies
        }