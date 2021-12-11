from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="basis"),
    path('store-list/', views.home_page, name="stores"),
    path('stores/<int:store_pk>/', views.store_detail, name="store"),
    path('items/<str:item_pk>/', views.item_detail, name="item"),
    path('<int:store_pk>/item-add/', views.item_create, name="item-add"),
    path('item-update/<str:item_pk>/', views.item_update, name="item-update"),
    path('item-delete/<str:item_pk>/', views.item_delete, name="item-delete"),
    # path('store-inventory/<str:store_pk>/', views.store_potential_profit, name="store-inventory"),

]

