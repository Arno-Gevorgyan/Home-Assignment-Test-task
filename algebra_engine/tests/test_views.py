from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from algebra_engine.models import ExpressionHistory
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
