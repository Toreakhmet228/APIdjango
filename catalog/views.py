from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters
from typing import Dict, List, Any
from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer

class ProductFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = filters.NumberFilter(field_name="price", lookup_expr='lte')
    color = filters.CharFilter(field_name="color")
    category = filters.NumberFilter(field_name="category__id")
    search = filters.CharFilter(method='filter_by_search')

    class Meta:
        model = Product
        fields = ['price_min', 'price_max', 'color', 'category', 'search']

    def filter_by_search(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_queryset(self) -> QuerySet:
        return Product.objects.all()

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self) -> QuerySet:
        product_id: int = self.kwargs['product_id']
        return Review.objects.filter(product__id=product_id).order_by('-rate')

    def list(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        queryset: QuerySet = self.get_queryset()
        grouped_reviews: Dict[int, List[Dict[str, Any]]] = {}

        for review in queryset:
            rate: int = review.rate
            if rate not in grouped_reviews:
                grouped_reviews[rate] = []
            grouped_reviews[rate].append(ReviewSerializer(review).data)

        return Response([{'rate': rate, 'items': items} for rate, items in grouped_reviews.items()])
