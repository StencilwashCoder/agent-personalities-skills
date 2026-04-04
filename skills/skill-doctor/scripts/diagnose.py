#!/usr/bin/env python3
"""
skill-doctor: Self-diagnosis tool for OpenClaw skills
Validates skill structure, syntax, and references
"""

import os
import sys
import re
import yaml
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

SKILL_DIRS = [
    "/usr/lib/node_modules/openclaw/skills",
    os.path.expanduser("~/.openclaw/skills"),
    os.path.expanduser("~/.openclaw/workspace/skills"),
]

class SkillDoctor:
    def __init__(self):
        self.issues: List[Dict[str, Any]] = []
        self.skills_checked = 0
        self.skills_ok = 0
        
    def find_all_skills(self) -> List[Path]:
        """Find all skill directories across all skill locations."""
        skills = []
        for skill_dir in SKILL_DIRS:
            path = Path(skill_dir)
            if not path.exists():
                continue
            for item in path.iterdir():
                if item.is_dir() and (item / "SKILL.md").exists():
                    skills.append(item)
        return skills
    
    def validate_yaml_frontmatter(self, content: str, skill_path: Path) -> Tuple[bool, Dict]:
        """Validate YAML frontmatter in SKILL.md."""
        issues = []
        
        # Extract frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return False, {"error": "Missing YAML frontmatter"}
        
        try:
            frontmatter = yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            return False, {"error": f"Invalid YAML: {e}"}
        
        if not frontmatter:
            return False, {"error": "Empty frontmatter"}
        
        # Required fields
        if "name" not in frontmatter:
            issues.append("Missing 'name' field")
        if "description" not in frontmatter:
            issues.append("Missing 'description' field")
        
        # Check for extra fields
        allowed = {"name", "description"}
        extra = set(frontmatter.keys()) - allowed
        if extra:
            issues.append(f"Extra fields in frontmatter: {extra}")
        
        return len(issues) == 0, {"issues": issues, "data": frontmatter}
    
    def check_script_syntax(self, script_path: Path) -> Tuple[bool, str]:
        """Check if a script has valid syntax."""
        content = script_path.read_text()
        
        if script_path.suffix == '.py':
            try:
                compile(content, str(script_path), 'exec')
                return True, "OK"
            except SyntaxError as e:
                return False, f"Syntax error: {e}"
        elif script_path.suffix in ['.sh', '.bash']:
            # Basic bash syntax check
            result = os.system(f"bash -n '{script_path}' 2>/dev/null")
            if result == 0:
                return True, "OK"
            else:
                return False, "Bash syntax error"
        
        return True, "Unknown file type, skipping syntax check"
    
    def check_references(self, skill_path: Path, skill_content: str) -> List[Dict]:
        """Check if referenced files exist."""
        issues = []
        ref_dir = skill_path / "references"
        
        if not ref_dir.exists():
            return issues
        
        # Find all markdown reference links in SKILL.md
        md_links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', skill_content)
        
        for text, link in md_links:
            ref_path = skill_path / link
            if not ref_path.exists():
                # Check if it's in references/
                ref_path = ref_dir / link
                if not ref_path.exists():
                    issues.append({
                        "type": "missing_reference",
                        "file": link,
                        "text": text
                    })
        
        return issues
    
    def diagnose_skill(self, skill_path: Path) -> Dict[str, Any]:
        """Run full diagnosis on a single skill."""
        result = {
            "name": skill_path.name,
            "path": str(skill_path),
            "status": "ok",
            "issues": []
        }
        
        skill_md = skill_path / "SKILL.md"
        content = skill_md.read_text()
        
        # Validate frontmatter
        fm_ok, fm_result = self.validate_yaml_frontmatter(content, skill_path)
        if not fm_ok:
            result["status"] = "error"
            result["issues"].append({
                "type": "frontmatter",
                "details": fm_result
            })
        elif fm_result.get("issues"):
            result["status"] = "warning"
            result["issues"].extend([{
                "type": "frontmatter",
                "details": issue
            } for issue in fm_result["issues"]])
        
        # Check references
        ref_issues = self.check_references(skill_path, content)
        if ref_issues:
            result["status"] = "error" if result["status"] == "ok" else result["status"]
            result["issues"].extend([{
                "type": "reference",
                "details": issue
            } for issue in ref_issues])
        
        # Check scripts
        scripts_dir = skill_path / "scripts"
        if scripts_dir.exists():
            for script in scripts_dir.iterdir():
                if script.is_file():
                    script_ok, script_msg = self.check_script_syntax(script)
                    if not script_ok:
                        result["status"] = "error" if result["status"] == "ok" else result["status"]
                        result["issues"].append({
                            "type": "script",
                            "file": script.name,
                            "details": script_msg
                        })
        
        # Check for extraneous files
        for item in skill_path.iterdir():
            if item.name in ["README.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md", "CHANGELOG.md"]:
                result["issues"].append({
                    "type": "extraneous_file",
                    "file": item.name,
                    "details": "Extraneous documentation file should be removed"
                })
        
        return result
    
    def run(self) -> str:
        """Run full diagnosis and return report."""
        skills = self.find_all_skills()
        results = []
        
        for skill_path in skills:
            self.skills_checked += 1
            result = self.diagnose_skill(skill_path)
            if result["status"] == "ok":
                self.skills_ok += 1
            results.append(result)
        
        return self.format_report(results)
    
    def format_report(self, results: List[Dict]) -> str:
        """Format diagnosis results as a report."""
        lines = [
            "🔧 SKILL DOCTOR DIAGNOSIS REPORT",
            "=" * 50,
            f"Skills checked: {self.skills_checked}",
            f"Healthy: {self.skills_ok}",
            f"Issues found: {self.skills_checked - self.skills_ok}",
            ""
        ]
        
        # Group by status
        errors = [r for r in results if r["status"] == "error"]
        warnings = [r for r in results if r["status"] == "warning"]
        healthy = [r for r in results if r["status"] == "ok"]
        
        if errors:
            lines.append("❌ ERRORS:")
            for r in errors:
                lines.append(f"\n  {r['name']}")
                for issue in r["issues"]:
                    lines.append(f"    - [{issue['type']}] {issue.get('details', issue)}")
        
        if warnings:
            lines.append("\n⚠️  WARNINGS:")
            for r in warnings:
                lines.append(f"\n  {r['name']}")
                for issue in r["issues"]:
                    lines.append(f"    - [{issue['type']}] {issue.get('details', issue)}")
        
        if healthy:
            lines.append(f"\n✅ HEALTHY ({len(healthy)} skills):")
            for r in healthy:
                lines.append(f"  ✓ {r['name']}")
        
        lines.append("\n" + "=" * 50)
        
        if not errors and not warnings:
            lines.append("🎉 All skills are healthy!")
        else:
            lines.append(f"💊 Fix {len(errors)} error(s) and {len(warnings)} warning(s) to get healthy.")
        
        return "\n".join(lines)

if __name__ == "__main__":
    doctor = SkillDoctor()
    report = doctor.run()
    print(report)
    
    # Exit with error code if issues found
    sys.exit(0 if doctor.skills_ok == doctor.skills_checked else 1)