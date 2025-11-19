import hashlib
import re
from http.client import responses
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from global_model.model import Product, Slider, Category, Brand, User, Cart, Order, OrderInfo, OrderProductList
def index(request):
    slider_list = Slider.objects.filter(status=1).order_by('order')
    feature_product = Product.objects.order_by('createdAt').limit(6)
    category_list = Category.objects.order_by('createdAt').limit(10)
    brands = Brand.objects.order_by('createdAt').limit(10)
    brand_list = []

    product_list_by_category = []
    for category in category_list:
        product_item = Product.objects.filter(category=category).order_by('createdAt').limit(6)
        item = {
            'category': category,
            'product': product_item
        }
        product_list_by_category.append(item)
    for brand in brands:
        total = Product.objects.filter(brand=brand).count()
        new_brand = {
            'id': brand.id,
            'name': brand.name,
            'description': brand.description,
            'total_product': total,
        }
        brand_list.append(new_brand)

    context = {
        'active': 'home',
        'slider_list': slider_list,
        'category_list': category_list,
        'brand_list': brand_list,
        'feature_product_list': feature_product,
        'product_list_by_category': product_list_by_category,
    }
    return render(request, 'eshop/index.html',context)
def contact_us(request):
    return render(request, 'eshop/contact-us.html')
def shop(request):
    category_list = Category.objects.all()
    brands = Brand.objects.all()
    brand_list = []
    page = request.GET.get("page", 1)
    for brand_item in brands:
        total = Product.objects.filter(brand=brand_item).count()
        new_brand = {
            'id': brand_item.id,
            'name': brand_item.name,
            'description': brand_item.description,
            'total_product': total,
        }
        brand_list.append(new_brand)

    product_list = Product.objects.order_by('createdAt')
    paginator = Paginator(product_list, 10)
    page_obj = paginator.get_page(page)

    context = {
        'category_list': category_list,
        'brand_list': brand_list,
        'page_obj': page_obj,
        'total_pages': range(paginator.num_pages),
        'active': 'shop'
    }
    return render(request, 'eshop/shop.html',context)

def shop_by_brand(request,brand_name):
    category_list = Category.objects.all()
    brand = Brand.objects.filter(name__iexact=brand_name).first()
    brands = Brand.objects.order_by('createdAt').limit(10)
    brand_list = []
    page = request.GET.get("page", 1)
    for brand_item in brands:
        total = Product.objects.filter(brand=brand_item).count()
        new_brand = {
            'id': brand_item.id,
            'name': brand_item.name,
            'description': brand_item.description,
            'total_product': total,
        }
        brand_list.append(new_brand)
    if brand:
        product_list = Product.objects.filter(brand=brand)

    paginator = Paginator(product_list, 10)
    page_obj = paginator.get_page(page)

    context = {
        'brand_name': brand_name,
        'brand_list': brand_list,
        'category_list': category_list,
        'active': 'shop',
        'page_obj': page_obj,
        'total_pages': range(paginator.num_pages),
    }
    return render(request, 'eshop/shop_by_brand_or_category.html',context)
def shop_by_category(request,category_name):
    category_list = Category.objects.all()
    category = Category.objects.filter(name__iexact=category_name).first()
    brands = Brand.objects.order_by('createdAt').limit(10)
    brand_list = []
    page = request.GET.get("page", 1)
    for brand_item in brands:
        total = Product.objects.filter(brand=brand_item).count()
        new_brand = {
            'id': brand_item.id,
            'name': brand_item.name,
            'description': brand_item.description,
            'total_product': total,
        }
        brand_list.append(new_brand)
    if category:
        product_list = Product.objects.filter(category=category)

    paginator = Paginator(product_list, 10)
    page_obj = paginator.get_page(page)

    context = {
        'category_name': category_name,
        'brand_list': brand_list,
        'category_list': category_list,
        'active': 'shop',
        'page_obj': page_obj,
        'total_pages': range(paginator.num_pages),
    }
    return render(request, 'eshop/shop_by_brand_or_category.html',context)
def product_details(request):
    return render(request, 'eshop/product-details.html')
def add_to_cart(request):
    product_id = request.POST.get('productId')
    user_id = request.POST.get('userId')

    if user_id and product_id:
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=user_id)
        product_price = product.price

        # check is already add to cart increase quantity
        if Cart.objects.filter(user=user, product=product):
            cart = Cart.objects.get(user=user, product=product)
            cart.quantity += 1
            cart.save()
        else:
            cart_item = Cart(product=product, user=user,price=product_price)
            cart_item.save()
        return JsonResponse({'status': 'success', 'message': 'Item added to cart.'},status=201)
    return JsonResponse({'status': 'fail', 'message': 'Item not added to cart.'},status=400)
def decrease_increase_quantity(request):
    cart_id = request.POST.get('cartId')
    is_decrease = request.POST.get('isDecrease')
    is_increase = request.POST.get('isIncrease')
    if is_decrease:
        cart = Cart.objects.get(id=cart_id)
        cart.quantity -= 1
        cart.save()
        return JsonResponse({'status': 'success', 'message': 'Item decreased.'},status=200)
    if is_increase:
        cart = Cart.objects.get(id=cart_id)
        cart.quantity += 1
        cart.save()
        return JsonResponse({'status': 'success', 'message': 'Item increased.'},status=200)

    return JsonResponse({'status': 'fail',})
def remove_cart(request):
    cart_id = request.POST.get('cartId')
    user_id = request.POST.get('userId')
    if cart_id and user_id:
        cart = Cart.objects.filter(id=cart_id)
        if cart:
            cart.delete()
            return JsonResponse({'status': 'success', 'message': 'Item removed from cart.'},status=200)
        else:
            return JsonResponse({'status': 'fail', 'message': 'Item not found'},status=400)
    return JsonResponse({'status': 'fail', 'message': 'Item not removed from cart.'},status=400)
def check_out(request):
    if not request.session.get('client_user_id') or not request.session.get('client_user_name') or not request.session.get('client_user_email'):
        return redirect('index')
    user_id = request.session.get('client_user_id')
    cart_item = Cart.objects.filter(user=user_id)
    total = 0
    for item in cart_item:
        total += item.price * item.quantity

    context = {
        'cart_item': cart_item,
        'active': 'checkout',
        'total': total,
    }
    return render(request, 'eshop/checkout.html',context)

def process_checkout(request):
    user_id = request.session.get('client_user_id')
    # get checkout info
    first_name = request.POST.get('firstName')
    last_name = request.POST.get('lastName')
    email = request.POST.get('email')
    tel = request.POST.get('phone')
    address = request.POST.get('address')
    address_2 = request.POST.get('address_2')
    shipping_notes = request.POST.get('shippingNotes')

    cart_item_list = Cart.objects.filter(user=user_id)
    user = User.objects.get(id=user_id)
    if not user:
        return JsonResponse({'status': 'fail', 'message': 'User not found'},status=400)
    product_list = []
    for cart in cart_item_list:
        product = Product.objects.get(id=cart.product.id)
        product_list.append(OrderProductList(
            product=product,
            price=cart.price,
            quantity=cart.quantity,
        ))
    order = Order(
        user=user,
        product_list=product_list,
        info=OrderInfo(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            phone=tel,
            additional_address=address_2,
            shipping_notes=shipping_notes,
        )
    )
    order.save()

    # clear cart after success order
    cart_item_list.delete()

    return JsonResponse({'status': 'success', 'message': 'Item processed.'},status=201)

def order_view(request):
    user = User.objects.get(id=request.session.get('client_user_id'))
    order_list = Order.objects.filter(user=user)
    context = {
        "active": "order",
        "order_list": order_list,
    }
    return render(request, 'eshop/order.html',context)

def search_result_view(request):
    q = request.GET.get('q')
    page = request.GET.get("page", 1)
    product_list = Product.objects.filter(name__icontains=q)
    paginator = Paginator(product_list, 10)
    page_obj = paginator.get_page(page)
    context = {
        "active": "search",
        "product_list": product_list,
        'page_obj': page_obj,
        'total_pages': range(paginator.num_pages),
        "query": q,
    }
    return render(request,"eshop/result.html",context)
def login(request):
    context = {
        "active": "login"
    }
    return render(request, 'eshop/login.html',context)
def error_404(request):
    return render(request, 'eshop/404.html')
def cart(request):
    if not request.session.get('client_user_id') or not request.session.get('client_user_name') or not request.session.get('client_user_email'):
        return redirect('index')
    user_id = request.session.get('client_user_id')
    cart_item = Cart.objects.filter(user=user_id)
    context = {
        'cart_item': cart_item,
        'active': 'cart',
    }
    return render(request, 'eshop/cart.html',context)

def process_signup(request):
    username = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    # check if username or email is already exist
    exist_username = User.objects.filter(username__iexact=username.strip())
    if exist_username:
        messages.error(request, 'Username already exists')
        return redirect('login')
    exist_email = User.objects.filter(email__iexact=email.strip())


    if exist_email:
        messages.error(request, 'Email already exists')
        return redirect('login')

    # check username validation
    is_valid = re.search("^[a-zA-Z\\s?]+$", username.strip())
    if not is_valid:
        messages.error(request, 'Username is invalid')
        return redirect('login')

    user = User(username=username.strip(), email=email.strip(), password=hashlib.md5(password.encode()).hexdigest())
    user.save()
    messages.success(request, 'Your account has been created! You are now able to log in.')
    return redirect('login')
def process_signin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = User.objects.get(email=email, password=hashlib.md5(password.encode()).hexdigest())
        if user:
            request.session['client_user_id'] = str(user.id)
            request.session['client_user_name'] = user.username
            request.session['client_user_email'] = user.email
            return redirect('index')
    except:
        messages.error(request, 'Incorrect Email or  Password')
        return redirect('login')

    return redirect('login')
def process_signout(request):
    if 'client_user_id' in request.session:
        del request.session['client_user_id']
        del request.session['client_user_name']
        del request.session['client_user_email']
    return redirect('index')