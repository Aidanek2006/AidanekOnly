from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):

    password = models.CharField(max_length=128, null=True, blank=True)
    age = models.PositiveSmallIntegerField(default=0, null=True, blank=True,
                                           validators=[MinValueValidator(20), MaxValueValidator(100)])
    date_registered = models.DateField(auto_now=True,  null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return self.username


class Marka(models.Model):
    marka_name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.marka_name


class Model(models.Model):
    model_name = models.CharField(max_length=16)

    def __str__(self):
        return self.model_name


class Car(models.Model):
    car_name = models.CharField(max_length=16)
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0, null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    year = models.DateField(auto_now_add=True)
    mileage = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='пробег')
    body = models.CharField(max_length=32, verbose_name='кузов')
    color = models.CharField(max_length=16)
    motor = models.CharField(max_length=32)
    condition = models.CharField(max_length=100, verbose_name='состояние')
    customs = models.CharField(max_length=16, verbose_name='таможня')
    active = models.BooleanField(default=True, verbose_name='в наличии')
    region = models.CharField(max_length=16)
    accounting = models.CharField(max_length=32, verbose_name='учет')
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    STEERING_WHEEL_CHOICES = (
        ('right', 'Right'),
        ('left', 'Left')
    )
    steering_wheel = models.CharField(max_length=32, choices=STEERING_WHEEL_CHOICES, verbose_name='руль')

    BOXES_CHOICES = (
        ('автомат', 'Автомат'),
        ('механик', 'механик')
    )
    boxes = models.CharField(max_length=32,choices=BOXES_CHOICES, verbose_name='каробка')

    DRIVES_CHOICES = (
        ('FWD', 'FWD'),
        ('RWD', 'RWD'),
        ('AWD', 'AWD'),
        ('4WD', '4WD')
    )
    drive = models.CharField(max_length=32, choices=DRIVES_CHOICES, verbose_name='привод')

    def __str__(self):
        return f'{self.car_name}'

    def get_average_rating(self):
        ratings = self.rating.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class CarPhotos(models.Model):
    car = models.ForeignKey(Car, related_name='car', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/')


class Rating(models.Model):
    car = models.ForeignKey(Car, related_name='rating', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings')
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг")
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.car} - {self.user} - {self.stars} stars"


class Favorite(models.Model):
    cart = models.OneToOneField(UserProfile, related_name='favorite', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.cart}'
