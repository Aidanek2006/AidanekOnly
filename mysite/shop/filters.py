from django_filters import FilterSet
from .models import Car, Rating


class CarFilter(FilterSet):
    class Meta:
        model = Car
        fields = {
            'marka': ['exact'],
            'model': ['exact'],
            'price': ['gt', 'lt'],
            'year': ['gt', 'lt']
        }


class RatingFilter(FilterSet):
    class Meta:
        model = Rating
        fields = {
            'stars': ['gt', 'lt']
        }