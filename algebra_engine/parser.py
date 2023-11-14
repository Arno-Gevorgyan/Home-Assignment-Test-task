import re
import operator
from typing import Any

from error_messages import SyntaxErrorMessages
from algebra_engine.expression_validator import SyntaxValidator


class ExpressionFormatter:
    def __init__(self, expression: str):
        """
        Initialize the ExpressionFormatter with an algebraic expression.

        Args: expression (str): The algebraic expression to be formatted.
        """
        self.expression = expression

    def format_expression(self) -> str:
        """
        Reformat the expression to have consistent spacing around operators.

        This method applies various formatting rules to the expression,
        ensuring that operators are properly spaced for readability and parsing.

        Returns: str: The reformatted expression.
        """
        formatted_expression = self.expression
        formatted_expression = self.handle_multi_character_operators(formatted_expression)
        formatted_expression = self.handle_single_character_operators(formatted_expression)
        formatted_expression = self.normalize_spacing(formatted_expression)
        return formatted_expression.strip()

    @staticmethod
    def handle_multi_character_operators(expression: str) -> str:
        """
        Add spaces around multi-character operators in the expression.

        Specifically handles '**' for exponentiation and '//' for floor division,
        adding spaces around these operators.

        Args: expression (str): The expression to format.

        Returns: str: The expression with formatted multi-character operators.
        """
        return re.sub(r'(\*\*|//)', r' \1 ', expression)

    @staticmethod
    def handle_single_character_operators(expression: str) -> str:
        """
        Add spaces around single-character operators in the expression.

        This method handles the spacing around single-character operators,
        with special consideration for unary operators to prevent incorrect spacing.

        Args: expression (str): The expression to format.

        Returns: str: The expression with formatted single-character operators.
        """
        expression = re.sub(r'(?<=[^\s])([\+\-\*\/])(?=[^\s])', r' \1 ', expression)

        # Handle unary operators by removing space after a binary operator or open parenthesis
        # This will prevent spaces between unary operators and their operands
        expression = re.sub(r'(?<=\b[\*\+\/\-\(])\s+(-|\+)(?=\d)', r'\1', expression)

        return expression

    @staticmethod
    def normalize_spacing(expression: str) -> str:
        """
        Normalize the spacing in the expression.

        This method reduces any instances of multiple consecutive spaces to a single space,
        helping to ensure consistent spacing throughout the expression.

        Args: expression (str): The expression to normalize.

        Returns: str: The expression with normalized spacing.
        """
        return re.sub(r'\s{2,}', ' ', expression)


class ExpressionEvaluator:
    """
    A class responsible for evaluating algebraic expressions.
    """

    def __init__(self, expression: str):
        """
        Initialize the ExpressionEvaluator with an algebraic expression.

        Args:
            expression (str): The algebraic expression to be evaluated.
        """
        self.expression: str = expression
        self.original_expression: str = expression

    def evaluate(self) -> str:
        """
        Evaluate the stored algebraic expression.

        Returns: str: The result of the evaluated expression.

        Raises: Exception: With detailed error messages if the expression is invalid or cannot be evaluated.
        """
        try:
            self.expression = self.handle_unary_operators()
            formatter = ExpressionFormatter(self.expression)
            self.expression = formatter.format_expression()
            self.is_valid_syntax()
            return str(self.safe_eval())

        except SyntaxError as e:
            raise Exception(SyntaxErrorMessages.GLOBAL_SYNTAX_ERROR.format(self.original_expression, str(e)))

        except Exception as e:
            raise Exception(SyntaxErrorMessages.EVALUATING_EXPRESSION_ERROR.format(self.original_expression, str(e)))

    def is_valid_syntax(self) -> Any:
        """
        Validate the syntax of the stored expression.

        Returns: Any: Error message if syntax is invalid, None otherwise.
        """
        validator = SyntaxValidator(self.expression)
        return validator.validate()

    def handle_unary_operators(self) -> str:
        """
        Process unary operators in the stored expression.

        Returns: str: The expression with unary operations processed.
        """
        self.expression = self.handle_len_operator(self.expression)
        self.expression = self.handle_abs_operator(self.expression)
        return self.expression

    @staticmethod
    def handle_len_operator(expression: str) -> str:
        """
        Process 'len' operator in the expression.

        Args: expression (str): The expression containing 'len' operator.

        Returns: str: The expression with 'len' operations processed.
        """

        def replace_len(match):
            return str(len(match.group(1).strip()))

        # Check for incorrect usage of len (e.g., len(a))
        if re.search(r"len\((?!')", expression):
            raise ValueError(SyntaxErrorMessages.LEN_ERROR)

        return re.sub(r"len\('([^']*)'\)", replace_len, expression)

    @staticmethod
    def handle_abs_operator(expression: str) -> str:
        """
        Process 'abs' operator in the expression.

        Args: expression (str): The expression containing 'abs' operator.

        Returns: str: The expression with 'abs' operations processed.
        """
        def replace_abs(match):
            inner_value = match.group(1).strip()
            if inner_value == '':
                raise ValueError(SyntaxErrorMessages.EMPTY_ARGUMENT_ABS)

            # Evaluate the expression inside abs()
            try:
                evaluated_value = eval(inner_value, {"__builtins__": None}, operator.__dict__)
                return str(abs(evaluated_value))
            except SyntaxError:
                raise ValueError(SyntaxErrorMessages.EMPTY_ARGUMENT_ABS.format(inner_value))
            except Exception as e:
                raise ValueError(SyntaxErrorMessages.INVALID_VALUE_ABS.format(inner_value, str(e)))

        return re.sub(r'abs\s*\(\s*(.*?)\s*\)', replace_abs, expression)

    def safe_eval(self) -> Any:
        """
        Safely evaluate the stored expression.

        Returns: Any: The result of the evaluation.

        Raises: Exception: If the evaluation fails.
        """

        return eval(self.expression, {"__builtins__": None}, operator.__dict__)
