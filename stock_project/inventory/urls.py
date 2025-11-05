from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('items/', views.item_list, name='item_list'),  
    path('', views.index, name='index'),
    path('add/', views.add_item, name='add_item'),
    path('edit/<int:id>/', views.edit_item, name='edit_item'),
    path('delete_item/<int:id>/', views.delete_item, name='delete_item'),

]