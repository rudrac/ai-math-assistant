import sympy
from sympy import Eq, Symbol


def calculate_math(expression: str) -> str:
    """Calculate a mathematical expression using SymPy."""
    try:
        expression = expression.strip()
        if not expression:
            raise ValueError("Expression cannot be empty.")
        result = sympy.sympify(expression)
        return str(result)
    except Exception as exc:
        raise ValueError(f"Invalid expression: {exc}")


def solve_equation(equation: str, variable: str = "x") -> str:
    """Solve an equation for the specified variable."""
    try:
        equation = equation.strip()
        if not equation or "=" not in equation:
            raise ValueError("Equation must contain an '=' sign.")
        left, right = equation.split("=", 1)
        eq = Eq(sympy.sympify(left), sympy.sympify(right))
        solutions = sympy.solve(eq, Symbol(variable))
        if solutions == []:
            return "No solution found."
        return str(solutions)
    except Exception as exc:
        raise ValueError(f"Invalid equation: {exc}")
