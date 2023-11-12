from django.urls import path

from algebra_engine.views import api_root

app_name = 'algebra_engine'


urlpatterns = [
    path('', api_root, name='api-root'),
]
