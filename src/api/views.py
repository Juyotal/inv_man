from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import datetime
from . serializers import ItemSerializer, StoreSerializer
from .models import Item, Store

# Create your views here.


@api_view(['GET'])
def apiOverview(request):
    # now = datetime.datetime.now()
    # html = "<html><body>It is now %s.</body></html>" % now
    # return HttpResponse(html)
    api_urls = {
        'Store List': '/stores/',
        'Store Detail': '/stores/<str:store_pk>/',
        'Store Create': '/store-create/',
        'Item Detail': '/items/<str:item_pk > /',
        'Item Add': '/item-add/',
        'Item Update': '/item-update/<str:item_pk>/',
        'Item Delete': '/item-delete/<str:item_pk>/',
    }
    return Response(api_urls)


@api_view(['GET'])
def home_page(request):
    stores = Store.objects.all()
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def store_detail(request, store_pk, data={}):
    store = Store.objects.get(_id=store_pk)
    items = Item.objects.filter(store=store)
    item_serializer = ItemSerializer(items, many=True)
    store_serializer = StoreSerializer(store, many=False)
    data['store'] = store_serializer.data
    data['items'] = item_serializer.data
    return Response(data)


@api_view(['GET'])
def item_detail(request, item_pk):
    item = Item.objects.get(_id=item_pk)
    item_serializer = ItemSerializer(item, many=False)

    return Response(item_serializer.data)


@api_view(['POST'])
def item_create(request, store_pk):
    store = Store.objects.get(_id=store_pk)
    data = request.data
    item  =Item.objects.create(
        store = store,
        name = data["name"],
        count_in_stock = int(data["count_in_stock"]),
        cost_price = float(data["cost_price"]),
        category = data["category"],
        markup = float(data["markup"]),
    )

    serializer = ItemSerializer(item, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def store_create(request):
    data = request.data
    store = Store.objects.create(
        name=data["name"]
    )

    serializer = StoreSerializer(store, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def item_update(request, item_pk):
    data = request.data
    item = Item.objects.get(_id=item_pk)

    item.count_in_stock = int(data['count'])
    item.save()
    serializer = ItemSerializer(item, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
def item_delete(request, item_pk):
    item = Item.objects.get(_id=item_pk)
    item.delete()
    return Response('Item Deleted')


# @api_view(['GET'])
# def store_potential_profit(request, store_pk):
#     store = Store.objects.get(_id=store_pk)
#     items = Item.objects.filter(store=store)
#     potential_profit = 0
#     item_inv = 0
#     data ={}
#     for item in items:
#         potential_profit += item.total_profit
#         item_inv += item.count_in_stock

#     data['potential_profit'] = potential_profit
#     data['item_inventory'] = item_inv
#     return Response(data=data)