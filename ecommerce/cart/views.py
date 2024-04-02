from django.shortcuts import render
from shop.models import Product
from cart.models import Cart, Order, Account
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def cart_view(request):
    u = request.user
    total = 0
    c = Cart.objects.filter(user=u)
    for i in c:
        total = total+i.quantity*i.product.price

    return render(request, 'cart.html',{'c': c, 'total':total})

@login_required
def addtocart(request, p):
    p = Product.objects.get(id=p)  # getting the particular product
    u = request.user  # to get the details and records of the current user login

    try:
        cart = Cart.objects.get(user=u,product=p)  # this is to check if the cart has that particular product already for the user.
        if (p.stock > 0):  # only increment till stock is available
            cart.quantity += 1  # if the cart already has the product for the user, then increment quantity by '1'.
            cart.save()  # save the cart details.
            p.stock -= 1  # to decrement the stock value when products are added to the cart
            p.save()  # save p

    except:  # if cart doesnt have that product for the user then create a new record for the cart.
        if (p.stock > 0):
            cart = Cart.objects.create(product=p, user=u,quantity=1)  # creates a new record in the cart table with product,user,and quantity as '1' initially.
            cart.save()
            p.stock-= 1
            p.save()

    return cart_view(request)

def cart_remove(request,p):
    p = Product.objects.get(id=p)  # getting the particular product
    u = request.user  # to get the details and records of the current user login

    try:
        cart = Cart.objects.get(user=u,product=p)  # this is to check if the cart has that particular product already for the user.
        if (cart.quantity > 1):
            cart.quantity -= 1  # it decrements the quantity
            cart.save()  # save the cart details.
            p.stock += 1  # it increments the available the stock.
            p.save()  # save p
        else:
            cart.delete()
            p.stock += 1
            p.save()

    except:
        pass

    return cart_view(request)

def full_remove(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.stock += cart.quantity
        p.save()
    except:
        pass

    return cart_view(request)

@login_required()
def orderform(request):
    if (request.method == "POST"):
        print('hello')
        a = request.POST['a']
        p = request.POST['p']
        n = request.POST['n']
        u = request.user
        c = Cart.objects.filter(user=u)
        total = 0
        for i in c:
            total = total + i.quantity * i.product.price
        try:
            ac = Account.objects.get(acctnum=n)
            if (ac.amount >= total):
                ac.amount = ac.amount-total
                ac.save()
                for i in c:
                    o = Order.objects.create(user=u, product=i.product, address=a, phone=p, no_of_items=i.quantity, order_status="paid")
                    o.save()

                c.delete()
                msg = "Order Placed Successfully"
                return render(request, 'orderdetail.html', {'message': msg})
            else:
                msg = "Insufficient Amount. You can't Place Order"
                return render(request, 'orderdetail.html', {'message': msg})
        except:
            pass
    return render(request, 'orderform.html')

def order_view(request):
    u = request.user
    o = Order.objects.filter(user=u)
    return render(request, 'orderview.html', {'o':o, 'u':u.username})