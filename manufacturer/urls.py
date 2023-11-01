from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    NetworkViewSet,
    ProductViewSet,
    EmployeeViewSet,
    NetworkByCountry,
    HighDebtNetworksView,
    NetworksByProductView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()

router.register(r"networks", NetworkViewSet)
router.register(r"products", ProductViewSet)
router.register(r"employee", EmployeeViewSet)
router.register(r"networks/high-debt", HighDebtNetworksView, basename="network-high-debt")


urlpatterns = [
    path("networks/", NetworkViewSet.as_view({"get": "list"}), name="networks"),
    path("networks/high-debt/", HighDebtNetworksView.as_view({"get": "list"}), name="network-high-debt"),
    path("networks/contry/<str:country>/", NetworkByCountry.as_view({"get": "list"}), name="network-by-country"),
    path(
        "networks/product/<int:product_id>/", NetworksByProductView.as_view({"get": "list"}), name="networks-by-product"
    ),
    path(
        "networks/generate-qr-code-and-email/<int:pk>/", NetworkViewSet.as_view({"post": "generate_qr_code_and_send_email"}), name="generate-qr",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("", include(router.urls)),
]
