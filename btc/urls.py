from django.urls import path, include

from . import views

app_name = 'btc'

urlpatterns = [
    path('v1/quotes', views.GetCurrentBTCRate.as_view()),
]
