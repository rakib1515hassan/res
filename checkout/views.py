import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Stripe Payment Getway------------------------
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from  coreapp.models import Plan, CustomUser
import stripe
import time
import coreapp
import json
from django.utils import timezone



# Create your views here.
YOUR_DOMAIN = 'http://127.0.0.1:8000'
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_checkout_session(request, plan_id):
    user = request.user
    plan = Plan.objects.get(id = plan_id)
    if request.method== 'POST':
        checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                payment_method_types=['card'],
                line_items=[{
                        'price': plan.stripe_price_id,
                        'quantity': 1,
                }],
                # customer=user.email,
                metadata = { "plan_id": plan.id },
                mode='subscription',

                success_url= YOUR_DOMAIN + '/checkout/payment_successful',
                cancel_url= YOUR_DOMAIN + '/plan',
            )

        return redirect(checkout_session.url, code=303)

import coreapp
## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
    return redirect('coreapp:shop')



@csrf_exempt
def stripe_webhooks(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET 

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event based on its type-----------------------------------------------
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        customer_email = session["customer_details"]["email"]
        plan_id = session["metadata"]["plan_id"]

        print("----------------------------")
        print(f"client_reference_id :{client_reference_id}, stripe_customer_id: {stripe_customer_id}, stripe_subscription_id: {stripe_subscription_id}")
        print(f"customer_email :{customer_email}, plan_id: {plan_id}")
        print("----------------------------")

        # Process the payment and perform additional actions
        user = User.objects.get(id=client_reference_id)
        plan = Plan.objects.get(id = plan_id)

        print("----------------------------")
        print(f"User: {user}, Plan: {plan}")
        print("----------------------------")

        customer_obj = CustomUser.objects.get(user=user)
        customer_obj.is_verified = True
        customer_obj.subscribed_at = timezone.now()
        customer_obj.plan = plan
        customer_obj.save()

    return HttpResponse(status=200)