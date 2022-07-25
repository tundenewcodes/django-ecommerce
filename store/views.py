from itertools import product
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import datetime
from . utils import cookieCart, cartData, guestOrder
# Create your views here.

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products   =  Product.objects.all()
    context = { 'products' : products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)




def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order' : order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)





from  django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order' : order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action:', action)
    print('productId:', productId)
    customer = request.user.customer #get the logged in customer
    product = Product.objects.get(id=productId) # get the particular product that was clicked
    order, created = Order.objects.get_or_create(customer=customer, complete=False) #get order the order if it exit or create dont duplicate order, where customer is loggedin and complete is false
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product) #get orderitem the orderitem if it exit or create dont duplicate orderitem, where product is product and order is order
    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
    orderitem.save()

    if  orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('your item was added', safe=False)

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)



    else:
        customer, order = guestOrder(request, data)

    total = float( data['form']['total'])
    order.transaction_id = transaction_id

    if total  == float(order.get_cart_total_amt):
        order.complete = True
    order.save()
    if  order.shipping == True:
        ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode']

                )
    return JsonResponse('Payment Complete!', safe=False)
