from django.urls import path
from .import views

urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('login/', views.login_with_otp, name='login'),
    path('verify_otp/', views.verify_otp,name='verify_otp'),

    path('',views.product_list,name='product_list'),
    path('add',views.add_product,name='add_product'),
    path('edit/<int:pk>/',views.edit_product,name='edit_product'),
    path('delete/<int:pk>/',views.delete_product,name='delete_product'),  


]