import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as signout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.paginator import Paginator

from .decorators import unauthenticated_user, subscribed_user
from coreapp.models import CustomUser, ImageGallery, Shop, Image, Plan
from .forms import AdminShopForm, OwnerShopForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test


def is_subscribed(request):
    get_user_data = CustomUser.objects.get(user=request.user)
    return get_user_data.plan


# Create your views here.
@login_required(login_url='login/')
def dashboard(request):
    castom_users = CustomUser.objects.all()

    if request.user.is_superuser:
        shops = Shop.objects.all()
    else:
        shops = Shop.objects.filter(owner=request.user)

    get_user_data = CustomUser.objects.get(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        castom_user = request.POST.get('castom_user')
        location = request.POST.get('location')
        description = request.POST.get('description')

        if request.user.is_superuser:
            user = User.objects.get(username=castom_user)
            shop = Shop.objects.create(name=name, location=location, description=description, owner=user)
            messages.success(request, 'Successfully created the shop')
            return redirect('coreapp:home')

    # for shop in shops:
    #     shop_categories = ImageGallery.objects.filter(user=request.user, shop=shop)
    #     for category in shop_categories:
    #         if category.gallery_name not in categories:
    #             categories[category.gallery_name] = []
    #         categories[category.gallery_name].extend(category.get_image)
    users = CustomUser.objects.filter(is_verified=True)
    total_price = 0
    for user in users:
        print(f"user = {user}, price = {user.plan.price}")
        total_price += user.plan.price

    context = {
        'get_user_data': get_user_data,
        'shops': shops,
        'castom_users': castom_users,
        'total_price': total_price,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='http://127.0.0.1:8000/login/')
# @login_required(redirect_field_name='signup', login_url=None)
def shop(request):
    if is_subscribed(request) is None:
        return redirect('coreapp:home')
    # ? Create Shop
    if request.method == 'POST' and 'shop_form' in request.POST:
        if request.user.is_superuser:
            shop_form = AdminShopForm(data=request.POST)
        else:
            shop_form = OwnerShopForm(data=request.POST)
        if shop_form.is_valid() and request.user.is_superuser:
            shop_form.save()
            messages.success(request, 'Successfully created the shop')
            return redirect('coreapp:shop')

    # ? Delete Shop
    if request.method == 'POST' and 'delete_shop_form' in request.POST:
        shop_id = request.POST.get('shop_id')
        if request.user.is_superuser:
            shop = get_object_or_404(Shop, pk=shop_id)
        else:
            shop = get_object_or_404(Shop, pk=shop_id, owner=request.user)
        shop.delete()
        messages.success(request, 'Successfully deleted shop')
        return redirect('coreapp:shop')

    # ? Get Shop. If user is a superuser, show all shops otherwise show only shops owned by user
    if request.user.is_superuser:
        shops = Shop.objects.all()
        shop_form = AdminShopForm()
    else:
        shops = None
        s = Shop.objects.filter(owner=request.user)
        castomuser = CustomUser.objects.get(user = request.user)
        if s:
            if castomuser.login_from == 'Account':
                shops = s
            else:
                shop_id = request.session['shop_id']
                shops = Shop.objects.filter(owner=request.user, id = shop_id)
        shop_form = OwnerShopForm(initial={'owner': request.user})

    context = {
        'shops': shops,
        'form': shop_form
    }
    return render(request, 'shop.html', context, )


@unauthenticated_user
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone = request.POST.get('phone')
        company_name = request.POST.get('company_name')
        street_name = request.POST.get('street_name')
        zipcode = request.POST.get('zipcode')
        bank_account = request.POST.get('bank_account')
        kvk = request.POST.get('kvk')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # if password != password2:
        #     messages.error(request, 'Passwords do not match')
        #     return redirect('coreapp:signup')

        while True:
            username = str(random.randint(100000, 999999))
            check = User.objects.filter(username=username).exists()
            if not check:
                break

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already exist.")
                return redirect('coreapp:signup')
            else:
                usr = User.objects.create_user(email=email, password=password, username=username, first_name=name,
                                               last_name=surname)
                verification_code = str(random.randint(100000, 999999))
                castomer = CustomUser.objects.create(
                    user=usr,
                    phone_number=phone,
                    company_name=company_name,
                    street_name=street_name,
                    zip_code=zipcode,
                    kvk=kvk,
                    bank_account_number=bank_account,
                    verification_code=verification_code,
                )

                return redirect('coreapp:signin')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('coreapp:signup')

    return render(request, 'signup.html')


@unauthenticated_user
def signin(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                castomuser = CustomUser.objects.get(user = user)
                castomuser.login_from = 'Account'
                castomuser.save()
                login(request, user)
                return redirect('coreapp:home')

            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('coreapp:signin')

        except ObjectDoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('coreapp:signin')

    return render(request, 'signin.html')


@login_required(login_url='login/')
def logout(request):
    signout(request)
    return redirect('coreapp:signin')


@login_required
def plan(request):
    plans = Plan.objects.all()

    get_users = ""
    if request.user.is_superuser:
        get_users = CustomUser.objects.all().exclude(user=request.user)

    context = {
        'plans': plans,
        'get_users': get_users,
    }

    return render(request, 'pricing.html', context)


@login_required
def users(request):
    if request.user.is_superuser:
        get_users = CustomUser.objects.all().exclude(user=request.user)
        context = {'get_users': get_users}

    return render(request, 'users.html', context)


@login_required
def user(request, user_id):
    user = User.objects.get(pk=user_id)
    print(user)
    if request.user.is_superuser:
        shops = Shop.objects.filter(owner=user)
        context = {'user': user, 'shops': shops}

        return render(request, 'user_view.html', context)


@login_required
def create_shop(request):
    if is_subscribed(request) is None:
        return redirect('coreapp:home')

    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        description = request.POST.get('description')
        print(name, location, description)
        tags = request.POST.get('tags')
        shop = Shop.objects.create(
            name=name,
            location=location,
            description=description,
            owner=request.user
        )
        shop.tags.add(*tags.split(','))
        messages.success(request, 'Successfully created theshop')
        return redirect('coreapp:home')
    return render(request, 'create_shop.html', {'form': OwnerShopForm})


@login_required
def view_shop(request, shop_id):
    if request.method == 'POST' and 'delete_gallary_form' in request.POST:
        img_id = request.POST.get('img_id')
        image = get_object_or_404(ImageGallery, id=img_id)
        image.delete()
        return redirect('coreapp:view_shop', shop_id)

    if request.method == 'POST' and 'remove_img_form' in request.POST:
        img_id = request.POST.get('image_id')
        g_id = request.POST.get('gallery_id')
        gallery = get_object_or_404(ImageGallery, id=g_id)
        image = get_object_or_404(Image, id=img_id)
        image.gallery.remove(gallery)
        return redirect('coreapp:view_shop', shop_id)

    if request.method == 'POST' and 'edit_img_form' in request.POST:
        image_e_id = request.POST.get('image_e_id')
        new_image = request.FILES.get('new_image')

        image_obj = get_object_or_404(Image, id=image_e_id)

        if new_image:
            image_obj.image = new_image
            image_obj.save()
            # messages.success(request, "New Image Is Successfully Set.")
            return redirect('coreapp:view_shop', shop_id)

        return redirect('coreapp:view_shop', shop_id)

    if request.user.is_superuser:
        shop = get_object_or_404(Shop, pk=shop_id)
    else:
        shop = get_object_or_404(Shop, pk=shop_id, owner=request.user)

    # category = Image.objects.filter(category__shop=shop)
    categories = ImageGallery.objects.filter(shop=shop)
    return render(request, 'shop_view.html', {'shop': shop, 'categories': categories})


@login_required
def view_shop_slider(request, shop_id):
    shop = Shop.objects.get(id=shop_id)
    galleries = ImageGallery.objects.filter(shop=shop)
    return render(request, "slider.html", {"galleries": galleries,"shop":shop})


@login_required
def edit_shop(request, shop_id):
    if request.user.is_superuser:
        shop = get_object_or_404(Shop, pk=shop_id)
        shop_form = AdminShopForm(instance=shop)
    else:
        shop = get_object_or_404(Shop, pk=shop_id, owner=request.user)
        shop_form = OwnerShopForm(instance=shop)

    if request.method == 'POST':
        if request.user.is_superuser:
            shop_form = AdminShopForm(data=request.POST, instance=shop)
        else:
            shop_form = OwnerShopForm(data=request.POST, instance=shop)
        if shop_form.is_valid():
            tags = request.POST.get('tags')
            obj = shop_form.save(commit=False)
            if obj.is_verified:
                obj.verified_at = timezone.now()
            obj.tags.add(*tags.split(','))
            obj.save()
            messages.success(request, 'Successfully Updated')
            return redirect('coreapp:shop')

    return render(request, 'edit_shop.html',
                  {'shop': shop, 'form': shop_form})


@login_required
def delete_shop(request):
    shop_id = request.GET.get('shop_id')
    if request.user.is_superuser:
        shop = get_object_or_404(Shop, pk=shop_id)
    else:
        shop = get_object_or_404(Shop, pk=shop_id, owner=request.user)

    shop.delete()
    return redirect('coreapp:shop')


@login_required
def add_category(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)

    if request.method == 'POST':
        category = request.POST.get('category')
        ImageGallery.objects.create(gallery_name=category, shop=shop)
        return redirect('coreapp:view_shop', shop_id)
    return redirect('coreapp:view_shop', shop_id)


@login_required
def edit_gallery(request, shop_id, gallery_id):
    gallery = get_object_or_404(ImageGallery, pk=gallery_id)

    if request.method == 'POST':
        gallery.gallery_name = request.POST.get('gallery_name')
        gallery.save()
        return redirect('coreapp:view_shop', shop_id)

    return render(request, 'edit_gallery.html', {'gallery': gallery})


@login_required
def add_image(request):
    image_obj = Image.objects.all()
    if request.method == 'POST' and request.FILES:
        image_name = request.POST.get('image_name')
        image_file = request.FILES.get('image')

        Image.objects.create(user=request.user, name=image_name, image=image_file)
        return redirect('coreapp:content')
    else:
        return redirect('coreapp:content')


@login_required
def delete_image_gallery(request, img_id):
    image = get_object_or_404(ImageGallery, id=img_id)
    cat = image.image.id
    image.delete()
    return redirect('coreapp:manage_gallery', cat)


@login_required
def user_update(request, user_id):
    user = User.objects.get(id=user_id)
    Status = ''
    if user:
        customUser = CustomUser.objects.get(user=user)
        if customUser.is_verified == True:
            Status = 'Varify'
        else:
            Status = 'Deny'

    if request.method == 'POST':
        name = request.POST.get('name')
        status = request.POST.get('status')

        name_parts = name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        if name:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        if status:
            customUser = CustomUser.objects.get(user=user)
            if status == 'Varify':
                customUser.is_verified = True
                customUser.save()
            elif status == 'Deny':
                customUser.is_verified = False
                customUser.save()
        return redirect('coreapp:plan')

    data = {
        'user': user,
        'Status': Status
    }
    return render(request, "user_update.html", data)


@login_required
def user_delete(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('coreapp:plan')


@login_required
def content(request):
    usr = request.user
    image_obj = ''
    if usr.is_superuser:
        image_obj = Image.objects.all()
    else:
        image_obj = Image.objects.filter(user=request.user)

    paginator = Paginator(image_obj, per_page=8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        if image_id:
            i = Image.objects.get(id=image_id)
            i.delete()

    data = {
        'page_obj': page_obj,
    }
    return render(request, 'content.html', data)


@login_required
def image(request):
    usr = request.user
    image_obj = ''
    if usr.is_superuser:
        image_obj = Image.objects.all()
        galleries = ImageGallery.objects.all()
    else:
        image_obj = Image.objects.filter(user=request.user)
        galleries = ImageGallery.objects.filter(shop__owner=usr)

    paginator = Paginator(image_obj, per_page=8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        if image_id:
            i = Image.objects.get(id=image_id)
            i.delete()

        messages.success(request, 'Image is successfully delete.')

    if request.method == 'POST':
        gallery = ImageGallery.objects.get(id=request.POST.get("gallery"))
        for key in request.POST:
            if key.isdigit():
                image = Image.objects.get(id=int(key))
                image.gallery.add(gallery)

    data = {
        'page_obj': page_obj,
        "galleries": galleries
    }
    return render(request, 'add_image.html', data)


def shop_signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        shop_id = request.POST.get('shop_id')

        try:
            usr = User.objects.get(email=email)
            if usr:
                user = authenticate(request, username=usr.username, password=password)
                if user is not None:
                    try:
                        shop_obj = Shop.objects.get(owner__email=email , id = shop_id)
                        if shop_obj:
                            castomuser = CustomUser.objects.get(user = usr)
                            castomuser.login_from = 'shop'
                            castomuser.save()
                            request.session['shop_id'] = shop_id
                            login(request, user)
                            return redirect('coreapp:shop')
                    except ObjectDoesNotExist:
                        messages.error(request, 'Invalid Shop ID.')
                        return redirect('coreapp:shop_signin')
                else:
                    messages.error(request, 'Invalid password.')
                    return redirect('coreapp:shop_signin')
            
        except ObjectDoesNotExist:
            messages.error(request, 'Invalid email.')
            return redirect('coreapp:shop_signin')
    return render(request, "shop_signin.html")