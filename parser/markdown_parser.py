"""
Markdown PRD Parser
Extracts requirements from Product Requirements Documents in Markdown format
"""

import re
import markdown
from typing import List, Optional
from models.requirement import Requirement, RequirementType


class MarkdownParser:
    """Parses Markdown PRDs to extract requirements"""
    
    def __init__(self):
        self.md = markdown.Markdown(extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.attr_list'
        ])
        
        self.requirement_patterns = [
            r'^(?:#{1,6}\s*)?\[?\s*(REQ|FR|NFR|REQUIREMENT)[\s\-_]*(\d+)\s*[:\-]?\s*(.+?)\s*\]?$',
            r'^\s*[-*]\s*\[\s*\]\s*(.+)$',
            r'^\s*\d+\.\s+(.+)$',
        ]
        
        # Header pattern that excludes requirement ID lines
        self.header_pattern = re.compile(r'^(#{1,6})\s+(?!.*?(?:REQ|FR|NFR|REQUIREMENT)\s*\d+)\s*(.+)$')
    
    def parse_file(self, file_path: str) -> List[Requirement]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_content(content, file_path)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return []
    
    def parse_content(self, content: str, source_location: str = "") -> List[Requirement]:
        requirements = []
        lines = content.split('\n')
        current_section = ""
        
        for line_num, line in enumerate(lines, 1):
            # First try to extract requirements from the line
            requirement = self._extract_requirement_from_line(line, line_num, current_section)
            if requirement:
                requirement.source_location = f"{source_location}:{line_num}"
                requirements.append(requirement)
                continue
            
            # Then check for headers (only if no requirement was found)
            header_match = self.header_pattern.match(line)
            if header_match:
                level = len(header_match.group(1))
                current_section = header_match.group(2).strip()
        
        # Remove duplicates based on ID
        seen_ids = set()
        unique_requirements = []
        for req in requirements:
            if req.id not in seen_ids:
                seen_ids.add(req.id)
                unique_requirements.append(req)
        
        return unique_requirements
    
    def _extract_requirement_from_line(self, line: str, line_num: int, section: str) -> Optional[Requirement]:
        line = line.strip()
        if not line or line.startswith('```') or line.startswith('`'):
            return None
        
        for pattern in self.requirement_patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                return self._create_requirement_from_match(match, line, line_num, section)
        return None
    
    def _create_requirement_from_match(self, match, line: str, line_num: int, section: str) -> Requirement:
        if len(match.groups()) >= 3:
            prefix = match.group(1).upper()
            number = match.group(2).zfill(3)
            title = match.group(3).strip()
            req_id = f"{prefix}-{number}"
        elif len(match.groups()) == 2:
            prefix = match.group(1).upper()
            number = match.group(2).zfill(3)
            title = line.strip()
            req_id = f"{prefix}-{number}"
        else:
            req_id = f"REQ-{line_num:03d}"
            title = line.strip()
        
        title = re.sub(r'^[:\-\\s]+|[:\\-\\s]+$', '', title)
        if not title:
            title = line.strip()
        
        req_type = RequirementType.FUNCTIONAL
        if any(keyword in title.lower() for keyword in ['performance', 'security', 'usability', 'scalability']):
            req_type = RequirementType.NON_FUNCTIONAL
        elif match.lastindex >= 1 and match.group(1).upper() in ['NFR', 'NON-FUNCTIONAL']:
            req_type = RequirementType.NON_FUNCTIONAL
        
        return Requirement(
            id=req_id,
            title=title,
            description=line.strip(),
            requirement_type=req_type,
            priority="medium",
            tags=[section] if section else []
        )
