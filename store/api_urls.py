from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    ProductViewSet, CategoryViewSet, category_products_api,
    search_api, search_suggestions_api,
    api_cart_detail, api_cart_add, api_cart_remove,
    register_api, logout_api,
    OrderListCreateAPI
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),

    # Auth
    path("auth/register/", register_api),
    path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path("auth/logout/", logout_api),

    # Category products
    path("category/<slug:slug>/", category_products_api),

    # Search
    path("search/", search_api),
    path("search/suggestions/", search_suggestions_api),

    # Cart
    path("cart/", api_cart_detail),
    path("cart/add/", api_cart_add),
    path("cart/remove/", api_cart_remove),

    # Orders
    path("orders/", OrderListCreateAPI.as_view()),
]
