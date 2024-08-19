from django.urls import path
from .views import ProductListView, ReviewListView

urlpatterns = [
    path('product_list/', ProductListView.as_view(), name='product-list'),
    path('reviews/<int:product_id>/', ReviewListView.as_view(), name='review-list'),
]
