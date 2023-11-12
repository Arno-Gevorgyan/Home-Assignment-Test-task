import datetime

from django.test import TestCase

from algebra_engine.models import ExpressionHistory


class ExpressionHistoryModelTest(TestCase):
    """
    Test class for ExpressionHistory model in the algebra_engine app.
    """

    def setUp(self):
        """
        Set up method to create an ExpressionHistory object before each test method is run.
        """
        self.expression = ExpressionHistory.objects.create(expression="2 + 2", result="4")

    def test_expression_content(self):
        """
        Test to verify that the expression field contains the correct content.
        """
        expected_expression = f'{self.expression.expression}'
        self.assertEqual(expected_expression, '2 + 2')

    def test_result_content(self):
        """
        Test to verify that the result field contains the correct content.
        """
        expected_result = f'{self.expression.result}'
        self.assertEqual(expected_result, '4')

    def test_created_at(self):
        """
        Test to ensure that the created_at field is automatically set upon object creation.
        """
        self.assertTrue(isinstance(self.expression.created_at, datetime.datetime))

    def test_status_default(self):
        """
        Test to verify that the default status of a new ExpressionHistory object is 'PENDING'.
        """
        self.assertEqual(self.expression.status, 'PENDING')

    def test_evaluated_at(self):
        """
        Test to ensure that the evaluated_at field is set correctly and is None when the object is created.
        """
        self.assertIsNone(self.expression.evaluated_at)
