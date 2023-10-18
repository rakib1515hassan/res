from django.urls import path
from . import views

app_name = "coreapp"

urlpatterns = [
    path('', views.dashboard, name="home"),
    path('shop/', views.shop, name="shop"),

    path('signup/', views.signup, name="signup"),
    path('login/', views.signin, name="signin"),
    path('logout/', views.logout, name="logout"),

    path('plan/', views.plan, name="plan"),
    path('users/', views.users, name="users"),
    path('create_shop/', views.create_shop, name="create_shop"),
    path('shop/<int:shop_id>/', views.view_shop, name="view_shop"),
    path('shop-image-slider/<int:shop_id>/', views.view_shop_slider, name="view_shop_slider"),
    path('edit_shop/<int:shop_id>/', views.edit_shop, name="edit_shop"),
    path('delete_shop/', views.delete_shop, name="delete_shop"),

    path('add_category/<int:shop_id>/', views.add_category, name="add_category"),

    path('add_image/', views.add_image, name="add_image"),
    path('delete_image_gallery/<int:img_id>/', views.delete_image_gallery, name="delete_image_gallery"),
    path('shop/<int:shop_id>/<int:gallery_id>/', views.edit_gallery, name='edit_gallery'),

    path("user/<int:user_id>/", views.user, name="user"),
    path("user_update/<int:user_id>/", views.user_update, name="user_update"),
    path("user_delete/<int:user_id>/", views.user_delete, name="user_delete"),

    path("content/", views.content, name="content"),
    path("image/", views.image, name="image"),

    path("shop-signin/", views.shop_signin, name="shop_signin"),

]
