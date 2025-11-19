import decimal
import hashlib
import os.path
import time
from datetime import timedelta
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from account.decorator import login_required, check_isauth
from dashboard.forms import SliderForm, ProductForm
from eshop import settings
from global_model.model import Category, User, Slider, Brand, Product, ProductImage, Order, OrderStatus
from helper.helper import sum_orders_total

# Create your views here.
@login_required
def index(request):
    total_pending_orders = Order.objects(status=OrderStatus.PENDING).count()
    today = timezone.now() # get current day base by user timezone
    start_of_week = today - timedelta(days=today.weekday()) # Monday
    start_of_last_week = start_of_week - timedelta(days=7)
    end_of_last_week = start_of_week

    this_week_order = Order.objects(createdAt__gte=start_of_week)
    last_week_order = Order.objects.filter(createdAt__gte=start_of_last_week, createdAt__lt=end_of_last_week)

    # sale
    this_week_order_total = this_week_order.count()
    last_week_order_total = last_week_order.count() or 1
    sale_change = ((this_week_order_total - last_week_order_total) / last_week_order_total) * 100

    # earning
    this_week_earnings = sum_orders_total(this_week_order)
    last_week_earnings = sum_orders_total(last_week_order) or 1
    earnings_change = ((this_week_earnings - last_week_earnings) / last_week_earnings) * 100

    # new user
    this_week_signup = User.objects(role="user",createdAt__gte=start_of_week)
    last_week_signup = User.objects(role="user",createdAt__gte=start_of_last_week,createdAt__lt=end_of_last_week)
    this_week_signup_total = this_week_signup.count()
    last_week_signup_total = last_week_signup.count() or 1
    signup_change = ((this_week_signup_total - last_week_signup_total) / last_week_signup_total) * 100

    # latest orders
    latest_orders = Order.objects.order_by("-createdAt")
    latest_orders_list = []
    for order in latest_orders:
        total = 0
        for product in order.product_list:
            total += product.price * product.quantity
        latest_orders_list.append({
            "id": order.id,
            "order_by":order.user.username,
            "order_date":order.createdAt,
            "status":order.status.value,
            "total":total,
        })
        total = 0

    context = {
        "active" : "dashboard",
        "total_pending_orders":total_pending_orders,
        "sales_total": this_week_order_total,
        "sales_change": round(sale_change, 2),
        "earnings_total": round(this_week_earnings, 2),
        "earnings_change": round(earnings_change, 2),
        "signup_total": this_week_signup_total,
        "signup_change": round(signup_change, 2),
        "latest_orders": latest_orders_list,
    }

    return  render(request, "ecadmin/index.html",context)

@check_isauth
def login(request):
    # user = User(email="admin@gmail.com", username="Admin", password=hashlib.md5("12345678".encode()).hexdigest())
    # user.save()
    return render(request, "ecadmin/login.html")

# Start Brand
def brand(request):
    search_query = request.GET.get("q",None)
    page = request.GET.get("page",1)
    if search_query:
        brand_listing = Brand.objects.filter(name__icontains=search_query)
    else:
        brand_listing = Brand.objects.all()

    paginator = Paginator(brand_listing,5)
    page_obj = paginator.get_page(page)
    context = {
        "active": "brand",
        "page_obj": page_obj,
        "total_pages": range(paginator.num_pages),
        "search_query": search_query,
    }
    return render(request, "ecadmin/brands/index.html", context)

def brand_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name.strip() != "":
            # check name exist
            is_exist = Brand.objects.filter(name__icontains=name).first()
            if is_exist:
                return JsonResponse(
                    {
                        "status": "failed",
                        "data": {
                            "name": "Brand name is already been taken.",
                        }
                    }
                )

            brand_item = Brand(name=name, description=description)
            brand_item.save()
            return JsonResponse({"status": "success","message": "Brand created successfully"})
        else:
            return JsonResponse(
                {
                    "status": "failed",
                    "data": {
                        "name": "Brand name is required.",
                    }
                }
            )

    return JsonResponse({"success": "failed","message": "Method not allowed"})

def brand_delete(request):
    if request.method == "POST":
        brand_id = request.POST.get("brand_id")
        brand_item = Brand.objects.get(id=brand_id)
        products = Product.objects.filter(brand=brand_item)

        if len(products) > 0:
            messages.error(request,"Can't delete this brand it has products.")
        else:
            brand_item.delete()
            messages.success(request,"Brand deleted successfully")
    return redirect("dashboard.brand")

def brand_update(request):
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name.strip() != "":
            # check name exist
            is_exist = Brand.objects.filter(name__iexact=name).first()
            if is_exist and str(is_exist.id) != id:
                return JsonResponse(
                    {
                        "status": "failed",
                        "data": {
                            "name": "Brand name is already been taken.",
                        }
                    }
                )
            brand_item = Brand.objects.get(id=id)
            if brand_item:
                brand_item.name = name
                brand_item.description = description.strip() if description.strip() != "" else None
                brand_item.save()
            return JsonResponse({"status": "success","message": "Category update successfully"})
        else:
            return JsonResponse(
                {
                    "status": "failed",
                    "data": {
                        "name": "Brand name is required.",
                    }
                }
            )

    return JsonResponse({"success": "failed","message": "Method not allowed"})
# End Brand

# Start Category
@login_required
def category(request):
    search_query = request.GET.get("q", None)
    page = request.GET.get("page", 1)
    if search_query:
        category_list = Category.objects.filter(name__icontains=search_query)
    else:
        category_list = Category.objects.all()
    paginator = Paginator(category_list, 5)
    page_obj = paginator.get_page(page)
    context = {
        "active": "category",
        "page_obj": page_obj,
        "total_pages": range(paginator.num_pages),
        "search_query": search_query,
    }
    return  render(request, "ecadmin/categories/index.html", context)

def category_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name.strip() != "":
            category_item = Category(name=name, description=description)
            category_item.save()
            return JsonResponse({"status": "success","message": "Category created successfully"})
        else:
            return JsonResponse({"status": "failed","message": "Name cannot be empty"})

    return JsonResponse({"success": "failed","message": "Method not allowed"})

def category_update(request):
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name.strip() != "":
            category_item = Category.objects.get(id=id)
            if category_item:
                category_item.name = name
                category_item.description = description.strip() if description.strip() != "" else None
                category_item.save()
            return JsonResponse({"status": "success","message": "Category created successfully"})
        else:
            return JsonResponse({"status": "failed","message": "Name cannot be empty"})

    return JsonResponse({"success": "failed","message": "Method not allowed"})

def category_delete(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        category_item = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category_item)

        if category_item:
            if len(products) > 0:
                messages.error(request, "Can't delete this category it has products.")
            else:
                category_item.delete()
                messages.success(request, "Category deleted successfully")
            return redirect("dashboard.category")
    return redirect("dashboard.category")
# End Category

# Start Slider
@login_required
def slider(request):
    search_query = request.GET.get("q", None)
    page = request.GET.get("page", 1)
    if search_query:
        slider_list = Slider.objects.filter(title__icontains=search_query)
    else:
        slider_list = Slider.objects.order_by("order")
    paginator = Paginator(slider_list, 5)
    page_obj = paginator.get_page(page)
    total_slider = slider_list.count()
    context = {
        "active": "slider",
        "page_obj": page_obj,
        "total_slider": total_slider,
        "total_pages": range(paginator.num_pages),
        "search_query": search_query,
    }
    return render(request, "ecadmin/sliders/slider.html", context)

@login_required
def slider_toggle_status(request,slider_id):
    slider_item = Slider.objects.filter(id=slider_id).first()
    if slider_item:
        slider_item.status = 1 if slider_item.status == 0 else 0
        slider_item.save()
    return redirect('dashboard.slider')

@login_required
def slider_create(request):
    if request.method == "POST":
        form = SliderForm(request.POST,request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            link = form.cleaned_data["link"]
            status = form.cleaned_data["status"]
            image = form.cleaned_data["image"]

            new_image_name = f"{round(time.time() * 1000)}_{image.name}"
            filepath = os.path.join(settings.MEDIA_ROOT,'sliders',new_image_name)
            handle_uploaded_file(image, filepath)

            # get max order number
            last_slider = Slider.objects.order_by('-order').first()
            last_order = last_slider.order if last_slider else 0

            new_slider = Slider(title=title,link=link,status=status,img=new_image_name,order=last_order + 1,description=description)
            new_slider.save()
            messages.success(request, "Slider created successfully")
            return redirect('dashboard.slider.create')
    else:
        form = SliderForm()

    context = {
        "form": form,
        "active":"slider"
    }

    return render(request, "ecadmin/sliders/create.html", context)

@login_required
def slider_edit(request, slider_id):
    slider_item = Slider.objects.get(id=slider_id)

    if request.method == "POST":
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            slider = Slider.objects.get(id=slider_id)
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            link = form.cleaned_data["link"]
            status = form.cleaned_data["status"]
            image = form.cleaned_data["image"]

            # Check duplicate title excluding the current slider
            exist_title = Slider.objects.filter(
                title__iexact=title,
                id__ne=slider_id
            )
            if exist_title:
                form.add_error("title", "Title already exists")
                return render(request, "ecadmin/sliders/edit.html", {
                    "form": form,
                    "slider_item": slider_item,
                    "active": "slider"
                })

            new_image_name = slider.img

            # remove old image
            if image:
                old_file_path = os.path.join(settings.MEDIA_ROOT, 'sliders', slider.img)
                if os.path.isfile(old_file_path):
                    os.remove(old_file_path)
                    # Save new image
                    new_image_name = f"{round(time.time() * 1000)}_{image.name}"
                    filepath = os.path.join(settings.MEDIA_ROOT, 'sliders', new_image_name)
                    handle_uploaded_file(image, filepath)


            slider.title = title
            slider.description = description
            slider.link = link
            slider.status = status
            slider.img = new_image_name
            slider.save()

            messages.success(request, "Slider updated successfully")
            return redirect('dashboard.slider.edit', slider_id=slider_id)

    else:
        form = SliderForm(initial={
            "title": slider_item.title,
            "link": slider_item.link,
            "status": slider_item.status,
            "description": slider_item.description,
        })

    return render(request, "ecadmin/sliders/edit.html", {
        "form": form,
        "slider_item": slider_item,
        "active": "slider"
    })


def slider_move(request,id):
    if request.method == "POST":
        first_slider = Slider.objects.get(id=id)
        temp_first_slider_order = first_slider.order
        if request.POST.get("move_up") is not None:
            first_slider.order = first_slider.order - 1
        elif request.POST.get("move_down") is not None:
            first_slider.order = first_slider.order + 1
        second_slider = Slider.objects.get(order=first_slider.order)
        second_slider.order = temp_first_slider_order
        first_slider.save()
        second_slider.save()

    return redirect("dashboard.slider")
def slider_delete(request):
    if request.method == "POST":
        slider_id = request.POST.get("slider_id")
        slider_item = Slider.objects.get(id=slider_id)
        file_path = os.path.join(settings.MEDIA_ROOT,'sliders',slider_item.img)
        if slider_item and os.path.isfile(file_path):
            os.remove(file_path)
            slider_item.delete()
            # re-index
            for i,s in enumerate(Slider.objects.order_by("order"),start=1):
                s.order = i
                s.save()
    return redirect("dashboard.slider")
# End Slider

# Start Product
@login_required
def product_view(request):
    search_query = request.GET.get("q", None)
    page = request.GET.get("page", 1)
    if search_query:
        product_list = Product.objects.filter(name__icontains=search_query)
    else:
        product_list = Product.objects.order_by("createdAt")
    paginator = Paginator(product_list, 5)
    page_obj = paginator.get_page(page)
    total_slider = product_list.count()
    context = {
        "active": "product",
        "page_obj": page_obj,
        "total_slider": total_slider,
        "total_pages": range(paginator.num_pages),
        "search_query": search_query,
    }
    return render(request, "ecadmin/products/index.html", context)

@login_required
def product_create(request):
    category_list = Category.objects.all().to_json()
    brand_list = Brand.objects.all().to_json()
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        brand_id = request.POST.get("brand_id")
        category_id = request.POST.get("category_id")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        status = request.POST.get("status")
        file = request.FILES.getlist("image")
        feature_image_name = request.POST.get("feature_image")

        image_list = []
        validation_list = []

        # check empty and zero validation rule
        if name.strip() == "":
            validation_list.append({"name":"Product name is required."})
        if category_id.strip() == "":
            validation_list.append({"category":"Category is required."})
        if brand_id.strip() == "":
            validation_list.append({"brand":"Brand is required."})
        if int(quantity) < 1:
            validation_list.append({"quantity":"Quantity must be greater than 0."})
        if len(file) < 1:
            validation_list.append({"image":"Image is required."})
        if description.strip() == "":
            validation_list.append({"description":"Description is required."})
        if decimal.Decimal(price) < 1:
            validation_list.append({"price":"Price must be greater than 0."})

        # check unique validation rule
        is_exist = Product.objects.filter(name__iexact=name).first()
        if is_exist:
            validation_list.append({"name":"Product with this name already exists."})

        if len(validation_list) > 0:
            return JsonResponse({"data": validation_list}, status=400)

        # save image file
        for i in range(len(file)):
            new_image_name = f"{round(time.time() * 1000)}_{file[i].name}"
            os.makedirs(os.path.join(settings.MEDIA_ROOT,'products'),exist_ok=True)
            filepath = os.path.join(settings.MEDIA_ROOT, 'products', new_image_name)
            handle_uploaded_file(file[i], filepath)
            is_thumbnail = 1 if file[i].name == feature_image_name else 0
            image_list.append(ProductImage(path=new_image_name,is_thumbnail=is_thumbnail))
        # if no feature image set
        if feature_image_name is None:
            image_list[0].is_thumbnail = 1    

        # save to database
        brand_item = Brand.objects.get(id=brand_id)
        category_item = Category.objects.get(id=category_id)

        product_item = Product(
            name=name,
            description=description,
            quantity=quantity,
            price=decimal.Decimal(price),
            brand=brand_item,
            category=category_item,
            images=image_list
        )
        product_item.save()
        return JsonResponse({"message":"Product created successfully."},status=201)
    context = {
        "active":"product",
        "category_list":  category_list,
        "brand_list": brand_list,
    }
    return render(request, "ecadmin/products/create.html", context)

@login_required
def product_delete(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        is_has_order = False
        order_id_list = []
        all_orders = Order.objects.all()
        for order in all_orders:
            for item in order.product_list:
                if str(item.product.id) == product_id:
                    is_has_order = True
                    order_id_list.append(order.id)
        if is_has_order:
            messages.error(request, "Can't delete this product it has orders.")
        else:
            for order_id in order_id_list:
                order = Order.objects.get(id=order_id)
                order.delete()
            product = Product.objects.get(id=product_id)
            if product:
                for img in product.images:
                    full_image_path = os.path.join(settings.MEDIA_ROOT, 'products', img.path)
                    if os.path.isfile(full_image_path):
                        os.remove(full_image_path)
                product.delete()
            messages.success(request, "Product has been deleted successfully")
    return redirect('dashboard.product')

@login_required
def product_update(request,id):
    category_list = Category.objects.all().to_json()
    brand_list = Brand.objects.all().to_json()
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product_item = Product.objects.get(id=id)
        product_name = request.POST.get("name")
        description = request.POST.get("description")
        brand_id = request.POST.get("brand_id")
        category_id = request.POST.get("category_id")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        status = request.POST.get("status")
        file = request.FILES.getlist("image")
        feature_image_name = request.POST.get("feature_image")
        remove_image_list = request.POST.getlist("remove_images")
        category = Category.objects.get(id=category_id)
        brand = Brand.objects.get(id=brand_id)
        is_change_feature_image = request.POST.get("is_change_feature_image")

        if is_change_feature_image:
            index = 0
            for img in product_item.images:
                if img.path == is_change_feature_image:
                    product_item.images[index].is_thumbnail = 1

                if img.is_thumbnail == 1 and img.path != is_change_feature_image:
                    product_item.images[index].is_thumbnail = 0
                index += 1

        product_item.name = product_name
        product_item.description = description
        product_item.price = price
        product_item.quantity = quantity
        product_item.status = status
        product_item.brand = brand
        product_item.category = category

        # save image file
        for i in range(len(file)):
            new_image_name = f"{round(time.time() * 1000)}_{file[i].name}"
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'products'), exist_ok=True)
            filepath = os.path.join(settings.MEDIA_ROOT, 'products', new_image_name)
            handle_uploaded_file(file[i], filepath)
            is_thumbnail = 1 if file[i].name == feature_image_name else 0
            if is_thumbnail == 1:
                index = 0
                for img in product_item.images:
                    product_item.images[index].is_thumbnail = 0
                    index += 1
            product_item.images.append(ProductImage(path=new_image_name, is_thumbnail=is_thumbnail))

        # remove image
        for img_name in remove_image_list:
            full_path = os.path.join(settings.MEDIA_ROOT,'products',img_name)
            if os.path.isfile(full_path):
                os.remove(os.path.join(settings.MEDIA_ROOT,'products',img_name))
                product_item.images = [img for img in product_item.images if img.path != img_name]

        product_item.save()
        return JsonResponse({"message": "Product update successfully."}, status=200)
    context = {
        "active": "product",
        "category_list": category_list,
        "brand_list": brand_list,
        "product": product.to_json(),
        "product_id": product.id
    }
    return render(request,"ecadmin/products/edit.html",context)
# End Product

@check_isauth
def process_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        # remember_me = request.POST.get("remember-me")
        remember_me = False
        try:
            user = User.objects.get(email=email, password=hashlib.md5(password.encode()).hexdigest())
            if user and user.role == "admin":
                request.session['user_id'] = str(user.id)
                request.session['user_name'] = user.username
                request.session['user_email'] = user.email

                if remember_me:
                    # 30 days (in seconds)
                    request.session.set_expiry(60 * 60 * 24 * 30)
                else:
                    # Session expires when browser closes
                    request.session.set_expiry(0)
                return redirect('dashboard')

            messages.error(request, 'Incorrect Email or  Password')
            return redirect('dashboard.login')
        except:
            messages.error(request, 'Incorrect Email or  Password')
            return redirect('dashboard.login')
    else:
        return redirect('dashboard.login')

def process_logout(request):
    if 'user_id' in request.session:
        request.session.flush()
    return redirect('dashboard.login')


def handle_uploaded_file(f,path):
    with open(path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
