from django.urls import path

from algebra_engine.views import api_root, ExpressionHistoryList

app_name = 'algebra_engine'


urlpatterns = [
    path('', api_root, name='api-root'),
    path('expressions/', ExpressionHistoryList.as_view(), name='expression-history'),
]
