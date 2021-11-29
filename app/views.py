from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .models import *
from .serializers import *
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
import razorpay
import random
import string



from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context



# Create your views here.
client = razorpay.Client(auth=("rzp_test_lYOMizShZ9dK1d", "FPZAwaMrz7DgYyvbPq1kOXSp"))





def templateemail(subject1,email,plaintext,htmly,d):
	subject, from_email, to = subject1, 'ravikrsngh.rks@gmail.com', email
	text_content = plaintext.render(d)
	html_content = htmly.render(d)
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
	print("Sent")


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




def index(request):
    cart = request.session.get('cart',[])
    wishlist = request.session.get('wishlist',[])
    p = Product.objects.filter(is_featured = True).order_by("-id")[:8]
    print(p)
    context = {
        "p":p,
        'no_of_items_in_wishlist':len(wishlist),
        'no_of_items_in_cart':len(cart),
        'all_categories':Category.objects.all(),
    }
    return render(request,'app/index.html',context)




def products(request):
    return render(request,'app/index.html',context)





def productdetails(request,pk):
    p = Product.objects.get(pk=pk)
    related_products = Product.objects.filter(subcategory__category = p.subcategory.category)
    cart = request.session.get('cart',[])
    wishlist = request.session.get('wishlist',[])
    print(related_products)
    context={
        "p":p,
        "related_products":related_products,
        'no_of_items_in_wishlist':len(wishlist),
        'no_of_items_in_cart':len(cart),
        'all_categories':Category.objects.all(),
    }
    try:
        type = request.GET['type']
        serializer=ProductSerializer(p,many=False)
        print(serializer.data)
        return JsonResponse({"data":serializer.data})
    except Exception as e:
        return render(request,'app/product-details.html',context)










def addtocart(request):
    if request.is_ajax and request.method == "GET":
        id = request.GET['id']
        quantity = int(request.GET['quantity'])
        p = Product.objects.get(id=id)
        cart = request.session.get('cart',[])
        c = [item[0] for item in cart]
        if id in c:
            i = c.index(id)
            cart[i][1] += quantity
            cart[i][2] = p.selling_price*cart[i][1]
        else:
            cart.append([id,quantity,p.selling_price*int(quantity)])
        request.session['cart'] = cart
        print(request.session['cart'])
        if request.GET['from'] == "wishlist":
            w = request.session.get('wishlist',[])
            w.remove(id)
            request.session['wishlist'] = w
    return  JsonResponse({"data":request.session['cart']})




def deletefromcart(request):
    id = request.GET['id']
    request.session['discount'] = 0
    if id == "all":
        request.session['cart'] = []
        return JsonResponse({"message":"Deleted all the items."})
    cart = request.session.get('cart',[])
    c = [item[0] for item in cart]
    i = c.index(id)
    cart.pop(i)
    request.session['cart'] = cart
    return JsonResponse({"message":"Deleted"})



def updatecart(request):
    id = request.GET['id']
    p = Product.objects.get(id=id)
    quantity = request.GET['quantity']
    cart = request.session.get('cart',[])
    c = [item[0] for item in cart]
    i = c.index(id)
    cart[i][1] = quantity
    cart[i][2] = p.selling_price * quantity
    request.session['cart'] = cart
    return JsonResponse(cart[i],safe=True)



def addtowishlist(request):
    id = request.GET['id']
    print(request.GET)
    p = Product.objects.get(id=id)
    wishlist = request.session.get('wishlist',[])
    if id in wishlist:
        return JsonResponse({"data":wishlist,"message":"The Product is already in the wishlist."})
    else:
        wishlist.append(id)
        request.session['wishlist'] = wishlist
        return JsonResponse({"data":wishlist,"message":"Added to wishlist"})







def wishlist(request):
    w = request.session.get('wishlist',[])
    cart = request.session.get('cart',[])
    l =[]
    for i in w:
        l.append(Product.objects.get(id=i))
    context={
        "wishlist":l,
        'no_of_items_in_wishlist':len(w),
        'no_of_items_in_cart':len(cart),
        'all_categories':Category.objects.all(),
    }
    return render(request,'app/wishlist.html',context)





def calculatecartprice(request):
    c = request.session.get('cart',[])
    all =[]
    subtotal = 0
    for i in c:
        l=[]
        l.append(Product.objects.get(id=i[0]))
        l.append(i[1])
        l.append(i[2])
        subtotal = subtotal + i[2]
        all.append(l)

    if subtotal > 360:
        request.session['shippingcharge'] = 0
    total = subtotal + request.session.get('shippingcharge',0) - request.session.get('discount',0)
    return subtotal,total,all




def cart(request):
    w = request.session.get('wishlist',[])
    c = request.session.get('cart',[])
    subtotal,total,all = calculatecartprice(request)

    context={
        "cart":all,
        'no_of_items_in_wishlist':len(w),
        'no_of_items_in_cart':len(c),
        'all_categories':Category.objects.all(),
        'all_states':State.objects.all().order_by("name"),
        'pincode': request.session.get('pincode',""),
        'state': request.session.get('state',""),
        'subtotal':subtotal,
        'total':total,
        'shippingcharge':request.session.get('shippingcharge',0),
        'discount':request.session.get('discount',0),
        'discountcode':request.session.get('discountcode',"")
    }
    return render(request,'app/cart.html',context)



def shop(request):
    w = request.session.get('wishlist',[])
    c = request.session.get('cart',[])

    context = {
        'no_of_items_in_wishlist':len(w),
        'no_of_items_in_cart':len(c),
        'all_categories':Category.objects.all(),
        'productlist': Product.objects.all().order_by("-id")
    }
    return render(request,'app/shop.html',context)


def shoppagedata(request):
    print(request.GET)
    print(request.GET.getlist('data[]'))
    productlist = Product.objects.filter(subcategory__category__name__in = request.GET.getlist('data[]') )
    serializer=ProductSerializer(productlist,many=True)
    html = render_to_string('app/ajax/productlist.html', {'productlist': productlist})
    return HttpResponse(html)




def getshippingquote(request):
    state = State.objects.get(name=request.GET['state'])
    #pincode = request.GET['pincode']
    request.session['state'] = model_to_dict(state)
    #request.session['pincode'] = pincode
    request.session['shippingcharge'] = state.price
    subtotal,total,all = calculatecartprice(request)
    if subtotal > 360:
        request.session['shippingcharge'] = 0

    return JsonResponse({"place":request.session['state'],"shippingcharge":request.session['shippingcharge'],"total":total})




def applycoupon(request):
    name = request.GET['name']
    if CouponCode.objects.filter(name = name).exists():
        obj = CouponCode.objects.get(name = name)
        c = request.session.get('cart',[])
        if len(c) == 0:
            request.session['discount'] = 0
            request.session['discountcode'] = obj.name
            return JsonResponse("No Item in Cart",safe=False)
        else:
            t = 0
            for i in c:
                t = t + i[2]
            print(t)
            request.session['discountcode'] = obj.name
            if t >= obj.above:
                discount = int(t * obj.offer / 100)
                print(discount)
                request.session['discount'] = discount
                subtotal,total,all = calculatecartprice(request)
                return JsonResponse({"total":total,"discount":discount})
            else:
                request.session['discount'] = 0
                return JsonResponse("Not Applicable.Your total order should be more than Rs. "+ str(obj.above),safe=False)
    else:
        return JsonResponse("Invalid Coupon Code",safe=False)





def checkout(request):
    if request.method == "POST":
        print(request.POST)
        request.session['fname'] = request.POST['fname']
        request.session['lname'] = request.POST['lname']
        request.session['phonenumber'] = request.POST['phonenumber']
        request.session['email'] = request.POST['email']
        request.session['addressline1'] = request.POST['addressline1']
        request.session['addressline2'] = request.POST['addressline2']
        request.session['city'] = request.POST['city']
        request.session['pincode'] = request.POST['pincode']
        request.session['ordernote'] = request.POST['ordernote']
        return HttpResponseRedirect('/place-order/')
    w = request.session.get('wishlist',[])
    c = request.session.get('cart',[])
    subtotal,total,all = calculatecartprice(request)


    context={
        "cart":all,
        'no_of_items_in_wishlist':len(w),
        'no_of_items_in_cart':len(c),
        'all_categories':Category.objects.all(),
        'all_states':State.objects.all().order_by("name"),
        'pincode': request.session.get('pincode',""),
        'state': request.session.get('state',""),
        'subtotal':subtotal,
        'total':total,
        'shippingcharge':request.session.get('shippingcharge',0),
        'discount':request.session.get('discount',0),
        'discountcode':request.session.get('discountcode',""),
        'selectedstate':request.session.get('state',{}),
        'selectedpincode':request.session.get('pincode',"")
    }
    return render(request,'app/checkout.html',context)




def placeorder(request):
    subtotal,total,all = calculatecartprice(request)
    order_currency = 'INR'
    order_receipt = "POSTERWA" + random_string_generator()
    request.session['order_receipt'] = order_receipt
    response = client.order.create(dict(amount=total*100, currency=order_currency, receipt=order_receipt, payment_capture='1'))
    order_id= response['id']
    request.session['order_id'] = order_id

    w = request.session.get('wishlist',[])
    c = request.session.get('cart',[])

    context={
        "cart":all,
        'no_of_items_in_wishlist':len(w),
        'no_of_items_in_cart':len(c),
        'all_categories':Category.objects.all(),
        'all_states':State.objects.all().order_by("name"),
        'pincode': request.session.get('pincode',""),
        'state': request.session.get('state',""),
        'subtotal':subtotal,
        'total':total,
        'shippingcharge':request.session.get('shippingcharge',0),
        'discount':request.session.get('discount',0),
        'discountcode':request.session.get('discountcode',""),
        'selectedstate':request.session.get('state',{}),
        'selectedpincode':request.session.get('pincode',""),
        'order_currency':order_currency,
        'order_receipt':order_receipt,
        'order_id':order_id,
        'address':request.session
    }

    return render(request,'app/placeorder.html',context)





def orderplaced(request):
    response = request.POST
    params_dict = {
    'razorpay_payment_id' : response['razorpay_payment_id'],
    'razorpay_order_id' : response['razorpay_order_id'],
    'razorpay_signature' : response['razorpay_signature']
    }
    # VERIFYING SIGNATURE
    try:
        status = client.utility.verify_payment_signature(params_dict)
        subtotal,total,all = calculatecartprice(request)

        product = ""
        product_list = []
        for i,j,k in all:
            product = product + str(i.id) + " - " + str(i.title) + " - "+ str(j) + "  |  "
            i.no_of_orders = i.no_of_orders + int(j)
            i.save()



        order = Order.objects.create(
            order_receipt= request.session['order_receipt'],
            order_id = request.session['order_id'],
            razorpay_payment_id = response['razorpay_payment_id'],
            razorpay_order_id = response['razorpay_order_id'],
            razorpay_signature = response['razorpay_signature'],
            name = request.session['fname'] + " " + request.session['lname'],
            address = request.session['addressline1'] + "\n" + request.session['addressline2'] + "\n Country :- India "  + " State:- " + request.session['state']['name'] + " Pincode :- " + request.session['pincode'],
            phone_number = request.session['phonenumber'],
            email = request.session['email'],
            total = total,
            subtotal = subtotal,
            products = product,
            order_note = request.session['ordernote'],
            shipping_charges = request.session.get('shippingcharge',0),
            couponname = request.session.get('discountcode',""),
            discount = request.session.get('discount',0),
        )
        plaintext = get_template('email/txtfiles/orderplaced.txt')
        htmly= get_template('email/orderplaced.html')
        d = { 'order': order , 'product_list':all , 'total_price':total , 'subtotal_price':subtotal , 'shipping':request.session.get('shippingcharge',0) }
        templateemail("Here's one order for you" , "ravikrsngh.rks@gmail.com" , plaintext , htmly , d)
        templateemail("We received your order" , order.email , plaintext , htmly , d)

        #print(list(request.session.keys()))
        for i in list(request.session.keys()):
            del request.session[i]


        return HttpResponseRedirect('/thank-you/')
    except:
        raise
        return HttpResponse("Payment Failed")





def thankyou(request):
	w = request.session.get('wishlist',[])
	c = request.session.get('cart',[])
	return render(request,'app/thankyou.html',{
		'no_of_items_in_wishlist':len(w),
        'no_of_items_in_cart':len(c),
	})



def contactus(request):
	w = request.session.get('wishlist',[])
	c = request.session.get('cart',[])
	return render(request,'app/contact.html',{
		'no_of_items_in_wishlist':len(w),
        'no_of_items_in_cart':len(c),
	})
