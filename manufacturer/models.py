from django.db import models
from django.contrib.auth.models import User


class Network(models.Model):
    Factory = "FA"
    Distributor = "DB"
    DealerCenter = "DC"
    LargeRetailChain = "LRC"
    IndividualEntrepreneur = "IE"
    CHOISES = [
        (Factory, "Factory"),
        (Distributor, "Distributor"),
        (DealerCenter, "Dealer Center"),
        (LargeRetailChain, "Large Retail Chain"),
        (IndividualEntrepreneur, "Individual Entrepreneur"),
    ]
    network_level = models.CharField(max_length=50, choices=CHOISES)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)
    supplier = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="child_networks"
    )
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    employee = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=25)
    model = models.CharField(max_length=255)
    release_date = models.DateField()
    network = models.ManyToManyField(Network)

    def __str__(self):
        return f"{self.network} - {self.name}"
