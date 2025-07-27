from django.urls import path
from .views import ReviewCreateView, ReviewUpdateView, ReviewDeleteView
app_name = 'reviews'

urlpatterns = [
path('create/<int:pk>/', ReviewCreateView.as_view(), name='review-create'),
    path('edit/<int:pk>/', ReviewUpdateView.as_view(), name='edit_review'),
    path('delete/<int:pk>/', ReviewDeleteView.as_view(), name='delete_review'),
]
