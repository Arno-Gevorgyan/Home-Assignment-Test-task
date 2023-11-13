from django.urls import path

from algebra_engine.views import ExpressionHistoryList, ExpressionInput

app_name = 'algebra_engine'


urlpatterns = [
    path('expressions/', ExpressionHistoryList.as_view(), name='expression-history'),
    path('expression-input/', ExpressionInput.as_view(), name='expression-input'),

]
