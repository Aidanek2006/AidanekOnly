from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age', 'phone_number',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class MarkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marka
        fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class CarListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    year = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Car
        fields = ['id', 'marka', 'model', 'car_name', 'price', 'average_rating', 'region', 'year']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class CarPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPhotos
        fields = ['image']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Favorite
        fields = '__all__'


class CarDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    owner = UserProfileSimpleSerializer(read_only=True)
    rating = RatingSerializer(read_only=True, many=True)

    class Meta:
        model = Car
        fields = ['marka', 'model', 'category', 'price', 'year', 'mileage', 'body', 'color',
                  'motor', 'condition', 'customs', 'active', 'region', 'accounting', 'owner',
                  'steering_wheel', 'boxes', 'drive', 'description', 'rating', 'average_rating']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

