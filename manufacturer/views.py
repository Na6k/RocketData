from rest_framework import viewsets
from .models import Network, Product
from django.contrib.auth.models import User
from .serializers import NetworkSerializer, ProductSerializer, EmployeeSerializer
from django.db.models import Avg
from manufacturer.filter import UserNetworkFilterBackend
from manufacturer.tasks import generate_qr_code_and_send_email
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action



class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    filter_backends = [UserNetworkFilterBackend]

    @action(detail=True, methods=["post"])
    def generate_qr_code_and_send_email(self, request, pk=None):
        try:
            network = self.get_object()
            user_email = request.user.email

            generate_qr_code_and_send_email.delay(network.id, user_email)

            return Response(
                {"message": "QR code generation and email sending task scheduled."}, status=status.HTTP_200_OK
            )
        except Network.DoesNotExist:
            return Response({"message": "Network not found."}, status=status.HTTP_404_NOT_FOUND)


# 4.2
class NetworkByCountry(viewsets.ModelViewSet):
    serializer_class = NetworkSerializer

    def get_queryset(self):  
        country = self.kwargs["country"]
        return Network.objects.filter(country=country)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer



class HighDebtNetworksView(viewsets.ModelViewSet):
    serializer_class = NetworkSerializer

    def get_queryset(self):
        avg_debt = Network.objects.aggregate(avg_debt=Avg("debt"))["avg_debt"]
        return Network.objects.filter(debt__gt=avg_debt)



class NetworksByProductView(viewsets.ModelViewSet):
    serializer_class = NetworkSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        return Network.objects.filter(product=product_id)
