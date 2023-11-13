from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from algebra_engine.models import ExpressionHistory
from algebra_engine.parser import ExpressionFormatter
from algebra_engine.serializers import ExpressionHistorySerializer


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
