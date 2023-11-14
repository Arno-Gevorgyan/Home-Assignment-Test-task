from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from algebra_engine.tests.constance import *
from algebra_engine.models import ExpressionHistory
from algebra_engine.expression_validator import SyntaxValidator
from algebra_engine.serializers import ExpressionHistorySerializer
from algebra_engine.parser import ExpressionFormatter, ExpressionEvaluator


class ExpressionHistoryListViewTests(TestCase):
    """
    Test suite for the ExpressionHistoryList view.
    """

    def setUp(self):
        """
        Set up data for the tests.
        """
        self.client = APIClient()
        ExpressionHistory.objects.create(expression="2 + 2", result="4", status="SUCCESS")
        ExpressionHistory.objects.create(expression="3 + 3", result="6", status="SUCCESS")

    def test_get_all_expressions(self):
        """
        Test retrieving all expression history records.
        """
        response = self.client.get(reverse('algebra_engine:expression-history'))
        expressions = ExpressionHistory.objects.all()
        serializer = ExpressionHistorySerializer(expressions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_empty_expression_list(self):
        """
        Test retrieving an empty list when no expression history records exist.
        """
        ExpressionHistory.objects.all().delete()
        response = self.client.get(reverse('algebra_engine:expression-history'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class ExpressionInputTest(APITestCase):

    def test_valid_expression(self):
        url = reverse('algebra_engine:expression-input')
        response = self.client.post(url, {'expression': '2+2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('result', response.data)

    def test_invalid_expression(self):
        url = reverse('algebra_engine:expression-input')
        response = self.client.post(url, {'expression': '2*/2'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expression_history_creation(self):
        url = reverse('algebra_engine:expression-input')
        self.client.post(url, {'expression': '3+3'})
        self.assertTrue(ExpressionHistory.objects.exists())


class ExpressionFormatterTest(TestCase):

    def test_operator_spacing(self):
        formatter = ExpressionFormatter("2+2*2")
        self.assertEqual(formatter.format_expression(), "2 + 2 * 2")

    def test_multi_character_operator_spacing(self):
        formatter = ExpressionFormatter("2**2//3")
        self.assertEqual(formatter.format_expression(), "2 ** 2 // 3")

    def test_unary_operator_handling(self):
        formatter = ExpressionFormatter("-2 + 3")
        self.assertEqual(formatter.format_expression(), "-2 + 3")

    def test_space_normalization(self):
        formatter = ExpressionFormatter("2  +   2")
        self.assertEqual(formatter.format_expression(), "2 + 2")

    def test_unary_operator_in_complex_expression(self):
        formatter = ExpressionFormatter("3 + -2 * 4")
        self.assertEqual(formatter.format_expression(), "3 + -2 * 4")

    def test_parentheses_handling(self):
        formatter = ExpressionFormatter("(2+3)*(4-5)")
        self.assertEqual(formatter.format_expression(), "(2 + 3) * (4 - 5)")


class ExpressionEvaluatorTest(TestCase):

    def test_basic_evaluation(self):
        evaluator = ExpressionEvaluator("2 + 2")
        self.assertEqual(evaluator.evaluate(), "4")

    def test_complex_expression(self):
        evaluator = ExpressionEvaluator("3 + len('test') * abs(-2) - 4")
        self.assertEqual(evaluator.evaluate(), "7")

    def test_expression_with_parentheses(self):
        evaluator = ExpressionEvaluator("(2 + 3) * (4 - 1)")
        self.assertEqual(evaluator.evaluate(), "15")

    def test_expression_with_nested_functions(self):
        evaluator = ExpressionEvaluator("len('hello') + abs(-5) * 2")
        self.assertEqual(evaluator.evaluate(), "15")

    def test_len_operator(self):
        evaluator = ExpressionEvaluator("len('hello')")
        self.assertEqual(evaluator.evaluate(), "5")

    def test_abs_operator(self):
        evaluator = ExpressionEvaluator("abs(-5)")
        self.assertEqual(evaluator.evaluate(), "5")

    def test_invalid_syntax(self):
        evaluator = ExpressionEvaluator("2 +")
        with self.assertRaises(Exception) as context:
            evaluator.evaluate()
        self.assertIn("Invalid syntax", str(context.exception))

    def test_invalid_len_usage(self):
        evaluator = ExpressionEvaluator("len(a)")
        with self.assertRaises(Exception) as context:
            evaluator.evaluate()
        self.assertIn("Incorrect usage of len(): argument not enclosed in quotes.", str(context.exception))

    def test_invalid_abs_value(self):
        evaluator = ExpressionEvaluator("abs(a)")
        with self.assertRaises(Exception) as context:
            evaluator.evaluate()
        self.assertIn("Invalid value for abs(): a", str(context.exception))

    def test_division_by_zero(self):
        evaluator = ExpressionEvaluator("5 / 0")
        with self.assertRaises(Exception) as context:
            evaluator.evaluate()
        self.assertIn("division by zero", str(context.exception))


class SyntaxValidatorTest(TestCase):

    def test_valid_expression(self):
        for expression in SyntaxValidatorConstants.VALID_EXPRESSIONS:
            expression = ExpressionEvaluator(expression).handle_len_operator(expression)
            expression = ExpressionEvaluator(expression).handle_abs_operator(expression)
            validator = SyntaxValidator(expression)
            self.assertIsNone(validator.validate(), msg=f"Failed on expression: {expression}")

    def test_empty_parentheses(self):
        for expression in SyntaxValidatorConstants.EMPTY_PARENTHESES:
            validator = SyntaxValidator(expression)
            with self.assertRaises(SyntaxError) as context:
                validator.check_empty_parentheses()
            self.assertEqual(str(context.exception), "Syntax error: empty parentheses found.")

    def test_missing_operators(self):
        for expression in SyntaxValidatorConstants.MISSING_OPERATORS:
            validator = SyntaxValidator(expression)
            with self.assertRaises(SyntaxError) as context:
                validator.validate()
            self.assertEqual(str(context.exception), "Missing operator in expression.")

    def test_invalid_characters(self):
        expressions = [
            "3 + $",
            "3 + 3 @ 4",
            "3 _ "
        ]
        for expression in expressions:
            validator = SyntaxValidator(expression)
            with self.assertRaises(SyntaxError) as context:
                validator.validate()
            self.assertIn("Invalid character found in expression:", str(context.exception))

    def test_trailing_operators(self):
        expressions = [
            "7 /",
            "4 + 5 -"
        ]
        for expression in expressions:
            validator = SyntaxValidator(expression)
            with self.assertRaises(SyntaxError) as context:
                validator.validate()
            self.assertEqual(str(context.exception), "Expression ends with an operator, which is invalid.")

    def test_mismatched_parentheses(self):
        validator = SyntaxValidator("(3 + 5")
        with self.assertRaises(SyntaxError) as context:
            validator.validate()
        self.assertEqual(str(context.exception), "Mismatched parentheses.")

    def test_consecutive_operators(self):
        validator = SyntaxValidator("4 ***/ 3")
        with self.assertRaises(SyntaxError) as context:
            validator.validate()
        self.assertEqual(str(context.exception), "Invalid consecutive operators found.")