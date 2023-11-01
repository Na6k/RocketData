from rest_framework import serializers
from .models import Network, Product
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class NetworkSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[MaxLengthValidator(
            limit_value=50, 
            message="Название не должно превышать 50 символов."
            )
        ]
    )

    class Meta:
        model = Network
        fields = "__all__"


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email"]


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[MaxLengthValidator(
            limit_value=25, 
            message="Название не должно превышать 25 символов."
            )
        ]
    )

    def validate_release_date(self, value):
        if value > timezone.now().date():
            raise ValidationError("Дата выхода продукта на рынок не может быть в будущем.")
        return value

    class Meta:
        model = Product
        fields = "__all__"


class NetworkDetailSerializer(NetworkSerializer):
    employees = EmployeeSerializer(many=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = Network
        fields = "__all__"


class NetworkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = "__all__"
        read_only_fields = ("debt",)
