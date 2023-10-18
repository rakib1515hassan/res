from django.urls import path
# from . import views
from checkout import views
app_name = 'checkout'

urlpatterns = [
    # path('', views.main, name='checkout_main'),
    # path('config/', views.stripe_config, name='stripe_config'),
    # path('create-checkout-session', views.create_checkout_session), # new
    # path('webhook/', views.stripe_webhooks), # new
    # path('cancel/', views.payment_cancel, name='payment_cancelled'), # new

    path("create_checkout_session/<int:plan_id>/", views.create_checkout_session, name="create_checkout_session"),
    path('stripe_webhooks/', views.stripe_webhooks, name='stripe_webhooks'),
    path("payment_successful/", views.payment_successful, name="payment_successful"),

]

## stripe listen --forward-to localhost:8000/checkout/stripe_webhooks/
## stripe listen --forward-to localhost:8000/checkout/webhook/

