from .models import ExpressionHistory
from .serializers import ExpressionHistorySerializer

from django.views import View
from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view


class MainView(View):
    template = 'index.html'

    def get(self, request):
        context = {}
        return render(request, self.template, {'context': context})


@api_view(['GET'])
def api_root(request):
    return Response({
    })


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
