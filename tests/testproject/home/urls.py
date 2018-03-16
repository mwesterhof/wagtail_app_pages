from django.urls import path

from .views import TestViewA, TestViewB


urlpatterns = [
    path('test-a/', TestViewA.as_view(), name='testview-a'),
    path('test-b/', TestViewB.as_view(), name='testview-b'),
]
