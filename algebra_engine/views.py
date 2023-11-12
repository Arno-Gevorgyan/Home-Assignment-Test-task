from django.views import View
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


class MainView(View):
    template = 'index.html'

    def get(self, request):
        context = {}
        return render(request, self.template, {'context': context})


@api_view(['GET'])
def api_root(request):
    return Response({
    })
