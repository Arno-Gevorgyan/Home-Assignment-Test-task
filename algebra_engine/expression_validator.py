import re
from typing import Any

from error_messages import SyntaxErrorMessages


class SyntaxValidator:
    """
    A class responsible for validating the syntax of algebraic expressions.
    """

    def __init__(self, expression: str):
        """
        Initialize the SyntaxValidator with an algebraic expression.

        Args: expression (str): The algebraic expression to be validated.
        """
        self.expression = expression

    def validate(self) -> Any:
        """
        Validate the syntax of the stored expression.

        Returns: Any: Error message if syntax is invalid, None otherwise.
        """
        self.check_empty_parentheses()
        self.check_missing_operators()
        self.check_invalid_characters()
        self.check_for_trailing_operators()
        self.check_mismatched_parentheses()
        self.check_consecutive_operators()

    def check_empty_parentheses(self) -> Any:
        """
        Check for empty parentheses in the expression.

        Returns:  Union[str | None]: Error message if empty parentheses are found, None otherwise.
        """
        if re.search(r'\(\s*\)', self.expression):
            raise SyntaxError(SyntaxErrorMessages.EMPTY_PARENTHESES)

    def check_missing_operators(self) -> Any:
        """
        Check for missing operators in the expression.

        Returns: Any: Error message if missing operators are found, None otherwise.
        """
        patterns = [
            r'\b\d+\s*(?=\()',  # Number immediately followed by an opening parenthesis
            r'\)\s+\d+',  # Closing parenthesis followed by a number
            r'\)\s*(?=\()',  # Closing parenthesis followed directly by an opening parenthesis
            r'\d+\s+\(',  # Number followed by an opening parenthesis
            r'\)\s+\(',  # Closing parenthesis followed by an opening parenthesis
            r'\b\d+\s+\d+',  # Two numbers with only space in between
        ]
        for pattern in patterns:
            if re.search(pattern, self.expression):
                raise SyntaxError(SyntaxErrorMessages.MISSING_OPERATOR)

    def check_invalid_characters(self) -> Any:
        """
        Check for invalid characters in the expression and ensure no trailing operators.

        Returns: Any: Error message if invalid characters or format issues are found, None otherwise.
        """
        # Allow periods for floating-point numbers
        invalid_char_match = re.search(r"[^\s\d\+\-\*\/\(\)\.]", self.expression)
        if invalid_char_match:
            invalid_char = invalid_char_match.group()
            raise SyntaxError(SyntaxErrorMessages.INVALID_CHARACTER.format(invalid_char))

    def check_for_trailing_operators(self) -> Any:
        """
        Check for trailing operators
        return: Any
        """

        if re.search(r'[\+\-\*\/]$', self.expression):
            raise SyntaxError(SyntaxErrorMessages.ENDS_WITH_OPERATOR)

    def check_mismatched_parentheses(self) -> Any:
        stack = []
        for char in self.expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack or stack[-1] != '(':
                    raise SyntaxError(SyntaxErrorMessages.MISMATCHED_PARENTHESES)
                stack.pop()
        if stack:
            raise SyntaxError(SyntaxErrorMessages.MISMATCHED_PARENTHESES)

    def check_consecutive_operators(self) -> Any:
        """
        Check for invalid consecutive operators in the expression.

        Returns: Any: Error message if invalid consecutive operators are found, None otherwise.
        """
        # Check for specific invalid consecutive operators
        invalid_operator_patterns = [
            # Disallow combinations like '*/', '/*', etc.
            r"(?<![*/])\*{1}\s*/{1}|/+\s*\*+",

            # Allow single '*' or double '**', disallow combinations like '** *'
            r"(?<!\*)\*{3,}(?!\*)|(?<!\/)\/{3,}(?!\/)|(\*\*|\*\s+)\s*[\+\-\*\/]|(\/\/|\/\s+)\s*[\+\-\*\/]",

            # Disallow combinations like '+**', '-**', '/-', '+*', '/+', and '+**'
            r"\+\s*\*\*|\-\s*\*\*|/\s*\-|\+\s*\*|/\s*\+"
        ]

        for pattern in invalid_operator_patterns:
            if re.search(pattern, self.expression):
                raise SyntaxError(SyntaxErrorMessages.INVALID_CONSECUTIVE_OPERATORS)
