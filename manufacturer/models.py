from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            token = Token.objects.get(user=self.user)
            if token.key and self.user.is_active:
                self.is_active = True
            else:
                self.is_active = False
        except Token.DoesNotExist:
            self.is_active = False
        super(Employee, self).save(*args, **kwargs)


class Network(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)
    supplier = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="child_networks")
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    def __str__(self):
        return self.name


class NetworkProduct(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.network.name} - {self.product.name}"
