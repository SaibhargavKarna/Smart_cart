from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import datetime
from website.models import Product,Order,OrderItem,ShippingAddress,paymentDetails
import razorpay
from django.conf import settings

# Create your views here.
def home(request):
    data=cartData(request)
    cartItems=data['cartItems']

    context={'cartItems':cartItems}
    return render(request,'index.html',context)


def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        c=User.objects.create_user(username=username,email=email,password=password)
        c.save()
        messages.success(request,'Your account has been created successfully! Please Login to Continue...')
        return redirect('login')
    return render(request,'register.html')


def login_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or password didn't match!")
            
    return render(request,'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')
 

#Main function is used to simplify code in all product functions
def shopping_item(request,product):
    #Assigning all products as values to Filters(& filter required product)
    selected_brands=Product.objects.filter(product_category=product)
    price_range=Product.objects.filter(product_category=product)
    selected_ratings=Product.objects.filter(product_category=product)
    products = selected_brands & price_range & selected_ratings

    #Assigning filter values from user to variables
    search_items=request.GET.get('Search-box')
    brands=request.GET.getlist('brand')
    price_min=request.GET.get('price_min')
    price_max=request.GET.get('price_max')
    ratings = request.GET.getlist('rating')
    sort_by=request.GET.get('sort-by')

    #Filtering-brands
    if brands:
        selected_brands=products.filter(product_brand__in=brands)
    else:
        if request.GET.get('clearFilters'):
            brands=[]

    #Filtering-pricerange    
    if price_min and price_max:
        price_range=products.filter(product_price__gte=price_min, product_price__lte=price_max)
    elif price_min:
        price_range=products.filter(product_price__gte=price_min)
    elif price_max:
        price_range=products.filter(product_price__lte=price_max)

    #Filtering-ratings
    if ratings:
        for rating in ratings:
            if rating == '4':
                selected_ratings=products.filter(product_rating__range=(4.0,5.0))
            elif rating == '3':
                selected_ratings=products.filter(product_rating__range=(3.0,4.0))
            elif rating == '2':
                selected_ratings=products.filter(product_rating__range=(2.0,3.0))
            elif rating == '1':
                selected_ratings=products.filter(product_rating__range=(1.0,2.0))
            elif rating == '0':
               selected_ratings=products.filter(product_rating__range=(0,1.0))
    
    products = selected_brands & price_range & selected_ratings

    #Appending filter values to a variable to send to frontend
    applied_filters=[]
    if brands:
        for brand in brands:
            applied_filters.append(brand)
   
    if price_min and price_max:
        applied_filters.append('price_min:'+price_min+' & price_max:'+price_max)
    elif price_min:
        applied_filters.append('price_min:'+price_min)
    elif price_max:
        applied_filters.append('price_max:'+price_max)

    if ratings:
        for rating in ratings:
            if rating == '4':
                applied_filters.append('Rating: 4.0-5.0')
            elif rating == '3':
                applied_filters.append('Rating: 3.0-4.0')
            elif rating == '2':
                applied_filters.append('Rating: 2.0-3.0')
            elif rating == '1':
                applied_filters.append('Rating: 1.0-2.0')
            elif rating == '0':
               applied_filters.append('Rating: 0-1.0')    

    
    products = selected_brands & price_range & selected_ratings

    #Search-box
    if search_items!=None:
        products=products.filter(product_name__icontains=search_items)
    

    #Sort-by
    if sort_by!=None:
        if sort_by=='price_maxTomin':
            products=products.order_by('-product_price')
        if sort_by=='price_minTomax':
            products=products.order_by('product_price')
        if sort_by=='rating_highTolow':
            products=products.order_by('-product_rating')
        if sort_by=='rating_lowTohigh':
            products=products.order_by('product_rating')

  

    return {'products':products,'applied_filters':applied_filters}


def mobiles(request):
    shopping_items=shopping_item(request,'Mobiles')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'mobiles.html',context)



def laptops(request):
    shopping_items=shopping_item(request,'Laptops')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'laptops.html',context)


def headphones(request):
    shopping_items=shopping_item(request,'Headphones')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'headphones.html',context)


def tv(request):
    shopping_items=shopping_item(request,'TVs')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'tv.html',context)


def ac(request):
    shopping_items=shopping_item(request,'ACs')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'ac.html',context)


def washing_mc(request):
    shopping_items=shopping_item(request,'Washing Machines')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'washing_mc.html',context)


def menswear(request):
    shopping_items=shopping_item(request,'Mens Wear')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'menswear.html',context)


def womenswear(request):
    shopping_items=shopping_item(request,'Womens wear')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'womenswear.html',context)


def kidswear(request):
    shopping_items=shopping_item(request,'Kids Wear')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'kidswear.html',context)


def watches(request):
    shopping_items=shopping_item(request,'Smart Watches')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'watches.html',context)


def shoes(request):
    shopping_items=shopping_item(request,'Shoes')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'shoes.html',context)


def books(request):
    shopping_items=shopping_item(request,'Books')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'books.html',context)


def bags(request):
    shopping_items=shopping_item(request,'Bags')
    products=shopping_items['products']
    applied_filters=shopping_items['applied_filters']

    data=cartData(request)
    cartItems=data['cartItems']
    
    context={'products':products,'applied_filters':applied_filters,'cartItems':cartItems}
    return render(request,'bags.html',context)


@login_required(login_url='login')
def cart(request):
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'cart.html',context)


@login_required(login_url='login')
def checkout(request):
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']


    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'checkout.html',context)


#This function is used to update(add/remove) products to/from Cart
def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']

    print('Action:',action)
    print('productId:',productId)

    user=request.user
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(user=user,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

    if action=='add':
        orderItem.quantity=(orderItem.quantity + 1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity -1)
    
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)


#This function is used to send data from checkout page to backend.
def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        user=request.user
        order,created=Order.objects.get_or_create(user=user,complete=False)
        total=float(data['shipping']['total'])
        order.transaction_id=transaction_id

        # if total==order.get_cart_total:
        #     order.complete=True
        # order.save()

        if order.shipping== True:
            ShippingAddress.objects.create(
                user=user,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                pincode=data['shipping']['pincode'],
            )

    else:
        print('User is not logged in...')

    return JsonResponse('Payment completed!',safe=False)


#This function is used to simply code in other views
def cartData(request):
    if request.user.is_authenticated:
        user=request.user
        order,created=Order.objects.get_or_create(user=user,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items

    else:
        items={}
        order={}
        cartItems={}

    return {'items':items,'order':order,'cartItems':cartItems}    


#Footer elements
def about(request):
    data=cartData(request)
    cartItems=data['cartItems']

    context={'cartItems':cartItems}

    return render(request,'about.html',context)


def support(request):
    data=cartData(request)
    cartItems=data['cartItems']

    context={'cartItems':cartItems}

    return render(request,'support.html',context)


def consumer_policy(request):
    data=cartData(request)
    cartItems=data['cartItems']

    context={'cartItems':cartItems}

    return render(request,'consumer_policy.html',context)


def connect(request):
    data=cartData(request)
    cartItems=data['cartItems']

    context={'cartItems':cartItems}

    return render(request,'connect.html',context)


def contact(request):
    data=cartData(request)
    cartItems=data['cartItems']

    context={'cartItems':cartItems}

    return render(request,'contact.html',context)


#Razorpay pyment integrtion
client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def razorpay(request):
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    # context={'items':items,'order':order,'cartItems':cartItems}

    if request.method=='POST':
        name=request.user
        amount=int(order.get_cart_total)*100
        
        DATA = {
            "amount": amount,
            "currency": "INR"
            }
    
        payment_response=client.order.create(data=DATA)

        order_id=payment_response['id']
        order_status=payment_response['status']

        if order_status=='created':
            payment_details=paymentDetails(
                name=name,
                amount=amount,
                order_id=order_id
            )
            payment_details.save()

            payment_response['name']=name

            # form=paymentDetailsForm(request.POST or None)
            # return render(request,'razorpay.html',{'payment_response':payment_response,'form':form})
            return render(request,'razorpay.html',{'payment_response':payment_response,'order':order,'cartItems':cartItems})
    # form=paymentDetailsForm()
    # return render(request,'razorpay.html',{'form':form})
    return render(request,'razorpay.html',{'order':order,'cartItems':cartItems})



@csrf_exempt
def payment_status(request):
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    # context={'items':items,'order':order,'cartItems':cartItems}
    
    response=request.POST
    print(response)
    params_dict={
        "razorpay_payment_id": response['razorpay_payment_id'],
        "razorpay_order_id": response['razorpay_order_id'],
        "razorpay_signature": response['razorpay_signature']
        }

    
    try:
        status=client.utility.verify_payment_signature(params_dict)
        payment_details=paymentDetails.objects.get(order_id=response['razorpay_order_id'])
        payment_details.razorpay_payment_id=response['razorpay_payment_id']
        payment_details.paid=True
        payment_details.save()

        if payment_details.paid==True:
            order.complete=True
            order.save()
        
        cartItems=0            
       
        return render(request,'paymentstatus.html',{'status':True,'cartItems':cartItems})
    
    except:    
        return render(request,'paymentstatus.html',{'status':False,'cartItems':cartItems})


