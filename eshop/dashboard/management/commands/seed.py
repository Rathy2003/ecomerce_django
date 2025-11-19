import hashlib
import os
import shutil
from django.core.management.base import BaseCommand

from eshop import settings
from global_model.model import User, Slider, Brand, Category, Product, ProductImage


class Command(BaseCommand):
    help = "Seed database with sample data"
    def handle(self, *args, **options):


        users = (
            {
                "email": "admin@gmail.com",
                "username": "Admin",
                "role": "admin",
                "password": hashlib.md5("admin@123".encode()).hexdigest()
            },
        )

        brands = (
            {
                "name": "Nike",
                "description": "Popular global sportswear and footwear brand"
            },
            {
                "name": "Adidas",
                "description": "German sportswear and lifestyle brand"
            },
            {
                "name": "Puma",
                "description": "Sportswear brand known for athletic apparel and shoes"
            },
            {
                "name": "Reebok",
                "description": "Footwear and apparel brand known for fitness-focused products"
            },
            {
                "name": "Under Armour",
                "description": "American athletic brand known for performance gear"
            }
        )

        categories = (
            {
                "name": "Shoes",
                "description": "Footwear category including sneakers, running shoes, and sports shoes"
            },
            {
                "name": "Clothing",
                "description": "Sportswear, casual wear, and performance apparel"
            },
            {
                "name": "Accessories",
                "description": "Bags, caps, socks, and other fashion or sports accessories"
            },
            {
                "name": "Sports Equipment",
                "description": "Balls, training gear, and sport-specific equipment"
            },
            {
                "name": "Outerwear",
                "description": "Jackets, hoodies, and warm sports clothing"
            }
        )

        products = (
            {
                "name": "Nike Air Max 2024",
                "description": "Lightweight running shoes with enhanced cushioning.",
                "quantity": 50,
                "price": "129.99",
                "brand": "Nike",
                "category": "Shoes",
                "images": [
                    {"path": "airmax1.jpg", "is_thumbnail": 1},
                    {"path": "airmax2.jpg", "is_thumbnail": 0},
                    {"path": "airmax3.webp", "is_thumbnail": 0}
                ]
            },
            {
                "name": "Adidas Ultraboost Pro",
                "description": "High-performance running shoes with knit upper.",
                "quantity": 40,
                "price": "139.99",
                "brand": "Adidas",
                "category": "Shoes",
                "images": [
                    {"path": "ultraboost1.jpg", "is_thumbnail": 1},
                    {"path": "ultraboost2.webp", "is_thumbnail": 0}
                ]
            },
            {
                "name": "Puma Sport Hoodie",
                "description": "Comfortable and stylish hoodie for training.",
                "quantity": 60,
                "price": "59.99",
                "brand": "Puma",
                "category": "Clothing",
                "images": [
                    {"path": "puma_hoodie1.webp", "is_thumbnail": 1},
                    {"path": "puma_hoodie2.webp", "is_thumbnail": 0}
                ]
            },
            {
                "name": "Reebok Fitness T-Shirt",
                "description": "Breathable fitness shirt ideal for workouts.",
                "quantity": 80,
                "price": "24.99",
                "brand": "Reebok",
                "category": "Clothing",
                "images": [
                    {"path": "reebok_shirt1.jpg", "is_thumbnail": 1}
                ]
            },
            {
                "name": "Under Armour Backpack",
                "description": "Durable backpack suitable for gym and travel.",
                "quantity": 45,
                "price": "49.99",
                "brand": "Under Armour",
                "category": "Accessories",
                "images": [
                    {"path": "ua_backpack1.jpg", "is_thumbnail": 1},
                    {"path": "ua_backpack2.jpg", "is_thumbnail": 0}
                ]
            },
            {
                "name": "Nike Sweatpants",
                "description": "Soft and comfortable sweatpants for daily wear.",
                "quantity": 70,
                "price": "39.99",
                "brand": "Nike",
                "category": "Clothing",
                "images": [
                    {"path": "nike_pants1.jpg", "is_thumbnail": 1}
                ]
            },
            {
                "name": "Adidas Training Gloves",
                "description": "High-grip gloves perfect for gym workouts.",
                "quantity": 55,
                "price": "19.99",
                "brand": "Adidas",
                "category": "Accessories",
                "images": [
                    {"path": "adidas_gloves1.jpg", "is_thumbnail": 1},
                    {"path": "adidas_gloves2.jpg", "is_thumbnail": 0}
                ]
            },
            {
                "name": "Puma Running Shorts",
                "description": "Lightweight shorts for running and training.",
                "quantity": 90,
                "price": "22.99",
                "brand": "Puma",
                "category": "Clothing",
                "images": [
                    {"path": "puma_shorts1.jpg", "is_thumbnail": 1}
                ]
            },
            {
                "name": "Reebok Yoga Mat",
                "description": "Non-slip yoga mat with extra cushioning.",
                "quantity": 35,
                "price": "29.99",
                "brand": "Reebok",
                "category": "Sports Equipment",
                "images": [
                    {"path": "reebok_yoga1.jpg", "is_thumbnail": 1},
                    {"path": "reebok_yoga2.jpg", "is_thumbnail": 0}
                ]
            },
            {
                "name": "Under Armour Water Bottle",
                "description": "Leak-proof stainless steel bottle for athletes.",
                "quantity": 100,
                "price": "14.99",
                "brand": "Under Armour",
                "category": "Accessories",
                "images": [
                    {"path": "ua_bottle1.webp", "is_thumbnail": 1}
                ]
            }
        )

        sliders = (
            {
                "title": "Summer Collection 2024",
                "description": "Discover our latest skincare essentials for radiant summer skin",
                "link": "/collections/summer-2024",
                "img": "girl1.jpg",
                "order": 1,
                "status": 1
            },
            {
                "title": "Premium Hydration Series",
                "description": "Advanced moisturizing formulas for all-day hydration and glow",
                "link": "/products/hydration-series",
                "img": "girl2.jpg",
                "order": 2,
                "status": 1
            },
            {
                "title": "Anti-Aging Solutions",
                "description": "Science-backed formulas to reduce fine lines and restore youthful radiance",
                "link": "/collections/anti-aging",
                "img": "girl3.jpg",
                "order": 3,
                "status": 1
            }
        )

        # Start Seed users
        for user in users:
            # find is user is already in database
            if len(User.objects.filter(email=user["email"]).all()) == 0:
                User.objects.create(
                    email=user["email"],
                    username=user["username"],
                    password=user["password"],
                    role=user["role"],
                ).save()
                self.stdout.write(self.style.SUCCESS(f"User {user['email']} created successfully!"))
            else:
                self.stdout.write(self.style.WARNING(f"User {user['email']} already exists!"))
        # End Seed users

        # Start Seed sliders
        for slider in sliders:
            if len(Slider.objects.filter(title=slider["title"]).all()) == 0:
                Slider.objects.create(
                    title=slider["title"],
                    description=slider["description"],
                    img=slider["img"],
                    link=slider["link"],
                    status=slider["status"],
                    order=slider["order"],
                ).save()

                media_initial_path = os.path.join('media_initial', 'sliders')
                destination_path = os.path.join(settings.MEDIA_ROOT, 'sliders')

                os.makedirs(destination_path, exist_ok=True)

                for filename in os.listdir(media_initial_path):
                    if filename.endswith('.jpg'):
                        source = os.path.join(media_initial_path, filename)
                        dest = os.path.join(destination_path, filename)
                        shutil.copy2(source, dest)
                        self.stdout.write(self.style.SUCCESS(f"Slider {slider['title']} created successfully!"))
            else:
                self.stdout.write(self.style.WARNING(f"Slider {slider['title']} already exists!"))
        # End Seed Slider

        # Start Brand Seed
        for brand in brands:
            if len(Brand.objects.filter(name=brand["name"]).all()) == 0:
                Brand.objects.create(
                    name=brand["name"],
                    description=brand["description"],
                ).save()

                self.stdout.write(self.style.SUCCESS(f"Brand {brand['name']} created successfully!"))
            else:
                self.stdout.write(self.style.WARNING(f"Brand {brand['name']} already exists!"))
        # End Brand Seed

        # Start Category Seed
        for category in categories:
            if len(Category.objects.filter(name=category["name"]).all()) == 0:
                Category.objects.create(
                    name=category["name"],
                    description=category["description"],
                ).save()

                self.stdout.write(self.style.SUCCESS(f"Category {category['name']} created successfully!"))
            else:
                self.stdout.write(self.style.WARNING(f"Category {category['name']} already exists!"))
        # End Category Seed

        # Start Product Seed
        for product in products:
            if len(Product.objects.filter(name=product["name"]).all()) == 0:
                brand_item = Brand.objects.filter(name__iexact=product["brand"]).first()
                category_item = Category.objects.filter(name__iexact=product["category"]).first()
                image_list = []

                for img in product["images"]:
                    image_list.append(ProductImage(path=img["path"], is_thumbnail=img["is_thumbnail"]))

                Product.objects.create(
                    name=product["name"],
                    description=product["description"],
                    quantity=product["quantity"],
                    price=product["price"],
                    brand=brand_item,
                    category=category_item,
                    images=image_list,
                ).save()

                product_media_initial_path = os.path.join('media_initial', 'products')
                product_destination_path = os.path.join(settings.MEDIA_ROOT, 'products')
                os.makedirs(product_destination_path, exist_ok=True)

                for filename in os.listdir(product_media_initial_path):
                    if filename.endswith(('.jpg','.png','.webp','.jpeg')):
                        source = os.path.join(product_media_initial_path, filename)
                        dest = os.path.join(product_destination_path, filename)
                        shutil.copy2(source, dest)
                        self.stdout.write(self.style.SUCCESS(f"Product {product['name']} created successfully!"))
            else:
                self.stdout.write(self.style.WARNING(f"Product {product['name']} already exists!"))
        # End Product Seed

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))