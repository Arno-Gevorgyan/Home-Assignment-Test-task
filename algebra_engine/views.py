from .models import ExpressionHistory
from .parser import ExpressionEvaluator
from .serializers import ExpressionHistorySerializer, ExpressionInputSerializer

from django.views import View
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response


class MainView(View):
    template = 'index.html'

    def get(self, request):
        context = {}
        return render(request, self.template, {'context': context})


class ExpressionHistoryList(generics.ListAPIView):
    """
    API view to retrieve a list of all expression history records.

    This view extends Django Rest Framework's ListAPIView to provide
    a read-only endpoint that lists all instances of ExpressionHistory.
    It utilizes the ExpressionHistory model and its corresponding serializer
    to return the data in a JSON format.

    The queryset property defines the set of records that will be returned
    by this view, which in this case, includes all records in the ExpressionHistory model.
    The serializer_class property specifies the serializer class to be used
    for formatting the response data.

    Clients can access this endpoint to retrieve the entire history
    of algebraic expressions evaluated, including their results and status.
    """
    queryset = ExpressionHistory.objects.all()
    serializer_class = ExpressionHistorySerializer


class ExpressionInput(generics.CreateAPIView):
    """
    API view to handle input of algebraic expressions and return evaluated results.

    This view accepts an algebraic expression, evaluates it, and returns the result.
    It also stores a record of the expression and its evaluation status in the database.
    """
    serializer_class = ExpressionInputSerializer

    def create(self, request, *args, **kwargs):
        """
        Handle POST request to evaluate an algebraic expression.

        Args:
            request: Django Rest Framework request object containing the expression.

        Returns:
            Response: DRF Response object with the evaluation result or error message.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        expression = serializer.validated_data['expression']
        try:
            result = ExpressionEvaluator(expression).evaluate()
            ExpressionHistory.objects.create(expression=expression, result=result, status="SUCCESS")
            return Response({"result": result}, status=status.HTTP_201_CREATED)
        except Exception as e:
            ExpressionHistory.objects.create(expression=expression, status="FAILED")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
