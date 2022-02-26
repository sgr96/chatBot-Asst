from django.urls import path
from . import views
from documentApi.views import Message

urlpatterns = [
    #path('Message/<str:pk>/', Message.as_view()),
    path('Message/', Message.as_view()),
]
