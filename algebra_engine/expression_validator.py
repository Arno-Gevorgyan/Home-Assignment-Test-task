import re
from typing import Any, Union


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
        checks = [
            self.check_empty_parentheses,
            self.check_missing_operators,
            self.check_invalid_characters,
            self.check_mismatched_parentheses,
            self.check_consecutive_operators
        ]

        for check in checks:
            if error := check():
                raise SyntaxError(error)

    def check_empty_parentheses(self) -> Union[str | None]:
        """
        Check for empty parentheses in the expression.

        Returns:  Union[str | None]: Error message if empty parentheses are found, None otherwise.
        """
        if re.search(r'\(\s*\)', self.expression):
            return "Syntax error: empty parentheses found."

    def check_missing_operators(self) -> Any:
        """
        Check for missing operators in the expression.

        Returns: Any: Error message if missing operators are found, None otherwise.
        """
        patterns = [
            r'\b\d+\s*(?=\()',  # Number immediately followed by an opening parenthesis
            r'\b\d+\s+(?=(len|abs)\b)',  # Number followed by a function name
            r'\)\s*(?=\b(len|abs)\b)',  # Closing parenthesis followed by a function name
            r'\b(len|abs)\b\s*\d+',  # Function name followed by a number
            r'\)\s+\d+',  # Closing parenthesis followed by a number
            r'\d+\s+\(',  # Number followed by an opening parenthesis
            r'\)\s+\(',  # Closing parenthesis followed by an opening parenthesis
        ]
        for pattern in patterns:
            if re.search(pattern, self.expression):
                return "Missing operator in expression."

    def check_invalid_characters(self) -> Any:
        """
        Check for invalid characters in the expression and ensure no trailing operators.

        Returns: Any: Error message if invalid characters or format issues are found, None otherwise.
        """
        # Allow periods for floating-point numbers
        invalid_char_match = re.search(r"[^\s\d\+\-\*\/\(\)\.]", self.expression)
        if invalid_char_match:
            invalid_char = invalid_char_match.group()
            return f"Invalid character found in expression: -> {invalid_char} :"

        # Check for trailing operators
        if re.search(r'[\+\-\*\/]$', self.expression):
            return "Expression ends with an operator, which is invalid."

        # # Check for malformed len() or abs() functions
        # malformed_function_match = re.search(r'(len|abs)\s*\'[^\']*\)', self.expression)
        # if malformed_function_match:
        #     return f"Malformed function found in expression: {malformed_function_match.group()}"

    def check_mismatched_parentheses(self) -> Any:
        if self.expression.count('(') != self.expression.count(')'):
            """
        Check for mismatched parentheses in the expression.

        Returns: Any: Error message if mismatched parentheses are found, None otherwise.
        """
            return "Mismatched parentheses."

    def check_consecutive_operators(self) -> Any:
        """
        Check for invalid consecutive operators in the expression.

        Returns: Any: Error message if invalid consecutive operators are found, None otherwise.
        """
        # Check for specific invalid consecutive operators
        invalid_operator_patterns = [
            # Disallow combinations like '*/', '/*', etc.
            r"(?<![*/])\*{1}\s*/{1}|/+\s*\*+",

            # Allow single '*' or double '**', disallow more than two '*' in a row
            r"(?<!\*)\*{3,}(?!\*)",

            # Allow single '/' or double '//', disallow more than two '/' in a row
            r"(?<!\/)\/{3,}(?!\/)",

            # Disallow consecutive '+' or '-' unless they are the same
            r"(?<!\+)(?<!\-)[\+\-]{2,}(?!\+)(?!\-)"
        ]

        for pattern in invalid_operator_patterns:
            if re.search(pattern, self.expression):
                return "Invalid consecutive operators found."
