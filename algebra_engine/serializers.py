from .models import ExpressionHistory
from rest_framework import serializers


class ExpressionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpressionHistory
        fields = ['id', 'expression', 'result', 'status', 'created_at', 'evaluated_at']


class ExpressionInputSerializer(serializers.Serializer):
    expression = serializers.CharField()
