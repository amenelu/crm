from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("userpage/", views.userPage, name="userpage"),
    path("account/", views.accountSettings, name="account"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("", views.home, name="home"),
    path("products", views.products, name="products"),
    path("customer/<str:pk_test>/", views.customer, name="customer"),
    path("create_order/<str:pk>/", views.createOrder, name="create_order"),
    path("update_order/<int:pk>/", views.updateOrder, name="update_order"),
    path("delete_order/<str:pk>/", views.deleteOrder, name="delete_order"),
    path("reset_password/", auth_views.PasswordResetView.as_view(), name="reset_view"),
    path(
        "reset_password_sent/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uid64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset_complete",
    ),
]
