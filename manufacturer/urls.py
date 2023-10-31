from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NetworkViewSet,
    ProductViewSet,
    EmployeeViewSet,
    NetworkByCountry,
    HighDebtNetworksView,
    NetworksByProductView,
)
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()

router.register(r"networks", NetworkViewSet)
router.register(r"products", ProductViewSet)
router.register(r"employees", EmployeeViewSet)
router.register(r"networks/high-debt", HighDebtNetworksView, basename="network-high-debt")
router.register(r"networks/contry/(?P<country>[A-Z]+)", NetworkByCountry, basename="network-by-country")
router.register(r"networks/product/1", NetworksByProductView, basename="networks-by-product")
# router.register(r"networks/(?P<country>[A-Z]+)", NetworkByCountry, basename="network-by-country")


urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path("networks/high-debt/", HighDebtNetworksView.as_view({"get": "list"}), name="network-high-debt"),
    path("networks/contry/<str:country>/", NetworkByCountry.as_view({"get": "list"}), name="network-by-country"),
    path( "networks/product/<int:product_id>/", NetworksByProductView.as_view({"get": "list"}), name="networks-by-product"),
    path("networks/generate-qr-code-and-email/<int:pk>/",NetworkViewSet.as_view({"post": "generate_qr_code_and_send_email"}), name="network-generate-qr-code-and-email",),
    path("", include(router.urls)),
    path("api-auth", include('rest_framework.urls'))
]
