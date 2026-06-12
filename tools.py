from langchain.tools import tool
import ast
import re
from rag_retriever import retrieve_best_practices

# Helper to count cyclomatic complexity (simplified)
def cyclomatic_complexity(code: str) -> int:
    complexity = 1  # base
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With, ast.FunctionDef)):
            complexity += 1
    return complexity

@tool
def analyze_structure(code: str) -> str:
    """Analyze code structure: number of functions, classes, lines, imports."""
    try:
        tree = ast.parse(code)
        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
        lines = len(code.splitlines())
        return f"Lines: {lines}\nFunctions: {len(functions)}\nClasses: {len(classes)}\nImports: {len(imports)}"
    except SyntaxError as e:
        return f"Syntax error in code: {e}"

@tool
def compute_complexity(code: str) -> str:
    """Compute cyclomatic complexity and nesting depth."""
    try:
        cc = cyclomatic_complexity(code)
        # Nesting depth approximation
        lines = code.splitlines()
        max_indent = 0
        for line in lines:
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            if stripped and not stripped.startswith('#'):
                max_indent = max(max_indent, indent // 4)  # assume 4 spaces per level
        return f"Cyclomatic complexity: {cc}\nMax nesting depth (approx): {max_indent}"
    except SyntaxError as e:
        return f"Syntax error: {e}"

@tool
def check_documentation(code: str) -> str:
    """Check if functions/classes have docstrings."""
    try:
        tree = ast.parse(code)
        missing = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    missing.append(node.name)
        if missing:
            return f"Missing docstrings for: {', '.join(missing)}"
        return "All functions and classes have docstrings."
    except SyntaxError as e:
        return f"Syntax error: {e}"

@tool
def security_scan(code: str) -> str:
    """Scan for common security issues: eval, exec, pickle, etc."""
    issues = []
    dangerous = ['eval(', 'exec(', '__import__', 'pickle.load', 'os.system', 'subprocess.call']
    for pattern in dangerous:
        if pattern in code:
            issues.append(pattern)
    if issues:
        return f"Potentially unsafe patterns found: {', '.join(issues)}"
    return "No obvious security issues detected."

@tool
def rag_retrieve(issue: str) -> str:
    """Retrieve relevant best practices for a given coding issue or concept."""
    return retrieve_best_practices(issue)