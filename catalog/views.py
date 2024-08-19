from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        color = self.request.query_params.get('color')
        category = self.request.query_params.get('category')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        search = self.request.query_params.get('search')

        if color:
            queryset = queryset.filter(color=color)
        if category:
            queryset = queryset.filter(category__id=category)
        if price_min and price_max:
            queryset = queryset.filter(price__gte=price_min, price__lte=price_max)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

        return queryset

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product__id=product_id).order_by('-rate')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        grouped_reviews = {}

        for review in queryset:
            rate = review.rate
            if rate not in grouped_reviews:
                grouped_reviews[rate] = []
            grouped_reviews[rate].append(ReviewSerializer(review).data)

        return Response([{'rate': rate, 'items': items} for rate, items in grouped_reviews.items()])
