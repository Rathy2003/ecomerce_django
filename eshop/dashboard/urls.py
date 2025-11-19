from django.contrib import admin
from django.urls import path
from  . import  views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('login/', views.login, name='dashboard.login'),
    path('process_logout/', views.process_logout, name='dashboard.process_logout'),
    path('process_login/', views.process_login, name='dashboard.process_login'),

    # Start Brand
    path('brand/', views.brand, name='dashboard.brand'),
    path('brand/create', views.brand_create, name='dashboard.brand.create'),
    path('brand/update', views.brand_update, name='dashboard.brand.update'),
    path('brand/delete', views.brand_delete, name='dashboard.brand.delete'),
    # End Brand

    # Start Category
    path('category/', views.category, name='dashboard.category'),
    path('category/create', views.category_create, name='dashboard.category.create'),
    path('category/update', views.category_update, name='dashboard.category.update'),
    path('category/delete', views.category_delete, name='dashboard.category.delete'),
    # End Category


    # Start Slider
    path('slider/', views.slider, name='dashboard.slider'),
    path('slider/create', views.slider_create, name='dashboard.slider.create'),
    path('slider/edit/<str:slider_id>', views.slider_edit, name='dashboard.slider.edit'),
    path('slider/toggle-status/<str:slider_id>', views.slider_toggle_status, name='dashboard.slider.toggle-status'),
    path('slider/delete', views.slider_delete, name='dashboard.slider.delete'),
    path('slider_move/<str:id>', views.slider_move, name='dashboard.slider_move'),
    # End Slider

    # Start Product
    path('product/', views.product_view, name='dashboard.product'),
    path('product/create', views.product_create, name='dashboard.product.create'),
    path('product/delete', views.product_delete,name='dashboard.product.delete'),
    path('product/edit/<str:id>', views.product_update, name='dashboard.product.update'),
    # End Product

]
