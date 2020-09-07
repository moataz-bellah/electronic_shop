from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes,action
from rest_framework.authentication import TokenAuthentication
from .models import Order,OrderItem
from rest_framework.authentication import SessionAuthentication
from .serializer import OrderItemSerializer,OrderSerializer,ProductSerializer
from rest_framework import viewsets
import rest_framework
from .models import Product
from django.db.models import Q
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from shop.forms import  SignupForm, SigninForm,Client_Form,CartAdd
from shop.models import Product, Category,Order,Client
from django.contrib.auth.decorators import login_required
from .cart import Cart
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from . import filters
from . import models
import datetime
from rest_framework.authtoken.models import Token

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            #user = form.save(commit=False)
            form.save()
            username=form['username'].value()
            password=form['password1'].value()
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("shop:client")
            messages.success(request, "User saved")
            return redirect("shop:signin")
        else:
            messages.error(request, "Error in form")
    else:
        form = SignupForm()
    context = {"form": form}
    return render(request, "account/signup.html", context)
@login_required
def client_data(request):
    #if request.method=="POST":
        #form=Client_Form(request.POST)
        #if form.is_valid():
    #else:
    #    form=Client_Form()
    #context={'form':form}
    return render(request,'shop/client.html',{})
@login_required
def data_client(request):
    c=models.Client.objects.filter(user=request.user).first()
    c.email = request.POST['email']
    c.phone = request.POST['phone']
    c.save()#form.save()
    messages.success(request,'Client Saved')
    return redirect("/")
def signin(request):
    #form2=SignupForm(request.POST)
    if request.method=="POST":
        form = SigninForm(request.POST)
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("shop:home")
        else:
            messages.error(request, "Invalid Username or Password")
    else:
        form = SigninForm()
    context = {"form": form}
    return render(request, "account/login.html", context)
@login_required()
def signout(request):
    logout(request)
    return redirect("shop:signin")

@login_required
def home(request):
    products = Product.objects.filter(active=True)
    categories = Category.objects.filter(active=True)
    c=models.Client.objects.filter(user=request.user).first()
    # Filters
    productFilter =  filters.ProductFilter(request.GET,queryset = products) # filter products
    products = productFilter.qs # list all data filters
    #pagination
    paginator = Paginator(products,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"products": products, "categories": categories,'c':c,'productFilter':productFilter,'page_obj':page_obj}
    return render(request, "home.html", context)
def testFilter(request):
    products = Product.objects.filter(active=True)
    categories = Category.objects.filter(active=True)
    c=models.Client.objects.filter(user=request.user).first()
    # token = Token.objects.create(user=request.user)
    # print(token.key)
    # print(request.user.id)
    # Filters
    productFilter =  filters.ProductFilter(request.GET,queryset = products) # filter products
    products = productFilter.qs # list all data filters
    return render(request,'test.html',{'productFilter':productFilter,'products':products})
def categoryProducts(request,name):
    category = models.Category.objects.get(name = name)
    products = models.Product.objects.filter(category = category)
    allCategories = models.Category.objects.all()
    paginator = Paginator(products,10)
    page_number = request.GET.get('get')
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{'page_obj':page_obj,'categories':allCategories})
@login_required
def market(request):
    products = Product.objects.filter(active=True)
    categories = Category.objects.filter(active=True)
    c=models.Client.objects.filter(user=request.user).first()
    context = {"products": products,"categories": categories,'c':c}
    return render(request, "shop/NewVersion-market.html", context)

@login_required
def search(request):
    q = request.GET["q"]
    products = Product.objects.filter(active=True, name__icontains=q)
    categories = Category.objects.filter(active=True)
    paginator = Paginator(products,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"products": products,
               "categories": categories,
               "title": q + " - search",'page_obj':page_obj}
    return render(request, "home.html", context)

@login_required()
def categories(request, slug):
    cat = Category.objects.get(slug=slug)
    products = Product.objects.filter(active=True, category=cat)
    categories = Category.objects.filter(active=True)
    context = {"products":products, "categories":categories, "title":cat.name + " - Categories"}
    return render(request, "shop/list.html", context)

@login_required()
def detail(request, product_id):
    product = Product.objects.filter(active=True, id=product_id).first()
    item = Product.objects.filter(id=product_id).first()
    c = Client.objects.filter(user=request.user).first()
    date = datetime.datetime.now().hour
    context = {"product" : product,
               "categories":categories,

               'c':c,
               'date':date
               }
    return render(request, "product.html", context)
@login_required
def mycart(request):
    c = models.Client.objects.filter(user=request.user)[0]
    sess = request.session.get("data", {"items":[],"price":[],"count":0,'quantity':[],'comment':[],'arrive_time':[]})
    cart=Cart(request)
    products = Product.objects.filter(active=True, slug__in=sess["items"])
    categories = Category.objects.filter(active=True)
    total_for_each=0
    tootal=[]
    dt = datetime.datetime.today()
    cart=Cart(request)
    tot=cart.get_total_price()
    dd=models.OrderItem.objects.all()
    context = {"products": products,
                'total':tot,
               "categories": categories,
               "cart":cart,
               "title": "My Cart"}
    return render(request, "order_summary.html", context)
@login_required
def coins_form(request):
    c=models.Client.objects.filter(user=request.user).first()
    return render(request, "shop/coins.html",{'c':c})

@login_required
def cart(request,product_id):
    c = Client.objects.filter(user=request.user).first()
    product = Product.objects.filter(id=product_id).first()
    inital = {}
    session = request.session.get("data", inital)
    date = datetime.datetime.now().hour
    return redirect("shop:detail",product_id)

@login_required()
def bill_page(request):
    cart=Cart(request)
    total=cart.get_total_price()
    order=models.Order(user=request.user,total_price=total)
    data=models.OrderItem()
    c=models.Client.objects.filter(user=request.user).first()
    order.save()
    dat=[]
    for x in cart:
        models.OrderItem.objects.create(user=request.user,orders=order,product=x['product'],quantity=int(x['quantity']),
        total_price=int(x['price']),comment=x['comment'])

    cart.clear()
    order.save()
    dt = datetime.datetime.today()
    order_item=models.OrderItem.objects.filter(user=request.user)
    c=models.Client.objects.filter(user=request.user)
    return render(request,'checkout.html',{'data2':order_item,'c':c})
@login_required()
def checkout(request):
    request.session.pop('data', None)
    return redirect("shop:mycart")


def message_view(request):
    data=models.messages(user=request.user,message=request.POST['message'])
    data.save()
    return redirect("shop:home")
@login_required()
def delete(request,id):
    c = Client.objects.filter(user=request.user)[0]
    sess = request.session.get("data")
    item = Product.objects.filter(pk=id)
    order_item = models.Order.objects.filter(
        id=id,
        user=request.user,
    ).first()
    li=[]
    total = models.total_cost_after_delevry(user=request.user, total_cost=sum(li) + 5)
    if order_item:
        c.coins+=order_item.total_price
        c.save()
        messages.info(request,"Removed...")
        order_item.delete()
    return redirect("shop:bill")
@login_required()
def update_page(request,id):
    cart=Cart(request)
    order_item=models.OrderItem.objects.filter(product=id).first()
    product=models.Product.objects.filter(id=id).first()
    data = cart.getQuantity(id)
    return render(request,'product_update.html',{'data':product,'cart':data,'order_item':order_item})
@login_required()
def update(request,id):
    cart=Cart(request)
    order=models.OrderItem.objects.filter(user=request.user,product=id).first()
    product=models.Product.objects.filter(id=id).first()
    comm = request.POST['comment']
    cart.add(
			product=product,
			quantity=int(request.POST['quantity']),comment=comm,update_quantity=True)
   # order.comment = comm
    #order.quantity=int(request.POST['quantity'])
    #order.save()
    return redirect("shop:mycart")
def updateQuantityPlus(request,product_id):
    cart=Cart(request)
    data = cart.getQuantity(product_id)
    data+=1
    print('dataaaaaaaaaa',data)
    product=models.Product.objects.filter(id=product_id).first()
    order=models.OrderItem.objects.filter(user=request.user,product = product).first()
    #order2 = get_object_or_404(models.OrderItem,user = request.user,product=product)

    newQuantity = 1
    cart.add(
			product=product,
			quantity = data,update_quantity=True)
    return redirect("shop:mycart")
def updateQuantityMinus(request,product_id):
    cart=Cart(request)
    data = cart.getQuantity(product_id)
    if data >=1:
        data-=1
    print('dataaaaaaaaaa',data)
    product=models.Product.objects.filter(id=product_id).first()
    order=models.OrderItem.objects.filter(user=request.user,product = product).first()
    #order2 = get_object_or_404(models.OrderItem,user = request.user,product=product)

    newQuantity = 1
    cart.add(
			product=product,
			quantity = data,update_quantity=True)
    return redirect("shop:mycart")
def cart_remove(request,product_id):
    cart=Cart(request)
    product=get_object_or_404(models.Product,id=product_id)
    cart.remove(product)
    return redirect("shop:detail")
def cart_detail(request):
    cart=Cart(request)
    print("the------------------------<",cart)
    return render(request,'shop/cart.html',{'cart':cart})

def cart_add(request,product_id):
	cart = Cart(request)
	product = get_object_or_404(Product,id=product_id)
	cart.add(
			product=product,
			quantity=int(request.POST['quantity']),comment=request.POST['comment'])

	return redirect('shop:mycart')

def cart_remove(request,product_id):
	cart = Cart(request)
	product = get_object_or_404(Product,id=product_id)
	cart.remove(product)
	return redirect('shop:mycart')
def cart_detail(request):
	cart = Cart(request)
	for item in cart:
		item['update_quantity_form'] = CartAddProductForm(initial={'quantity':item['quantity'],'update':True})

	context = {
		'cart':cart,

	}
	return render(request,'cart/detail.html',context)
#@require_POST
def order_create(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            for item in cart:
                models.OrderItem.objects.create(
					orders=order,
					product=item['product'],
					price=item['price'],
					quantity=item['quantity'])

            cart.clear()
            context = {'order':order}
            request.session['order_id'] = order.id
            return redirect('shop:bill')


        else:
            form = OrderCreateForm()
            context = {'cart':cart,'form':form}

    return render(request,'shop/cart.html',context)

def create_order(request):
    cart=Cart(request)
    order=models.Order(user=request.user)
    data=models.OrderItem()
    for x in cart.cart:
        data.create(orders=order,product=x['product'],price=item['price'],quantity=item['quantity'])
    cart.clear()
    order.save()
    #request.session['order_id'] = order.id
    return HttpResponse('DONES')

########################## API #################################################
@api_view(['GET'])
def api_products(request):
    query = request.GET.get("q", "")
    products = Product.objects.filter(Q(name__contains=query) | Q(description__contains=query))
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
class OrderItemApi(viewsets.ModelViewSet):
    queryset=models.OrderItem.objects.all()
    serializer_class=OrderItemSerializer
class OrderApi2(viewsets.ModelViewSet):
    queryset=models.Order.objects.all()
    serializer_class=OrderSerializer

class OrderApi(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = models.Order.objects.all()
    res={}
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            #if is_single:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            self.res['message']='Done'
            self.res['state']=True
            return Response(self.res, status=status.HTTP_201_CREATED,
                        headers=headers)
        else:
            self.res['message']='Error'
            self.res['state']=False
            return Response(self.res, status=status.HTTP_201_CREATED)
    def update(self, request, pk=None, *args, **kwargs):
        try:
            order = models.OrderItem.objects.get(pk=pk)

            if order.paid:
                raise APIException(detail="You can't update a delivered order.")
            else:
                order.paid = (request.data.get('paid') == 'true')
                #order.isReceived = (request.data.get('isReceived') == 'true')
                order.save()
                return Response(OrderItemApi(order).data)  #
        except models.order.DoesNotExist:
            raise APIException(detail=f"No order with id={pk} found")
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})
class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
def client_data_page(request):
    c=get_object_or_404(models.Client,user=request.user)
    return render(request,'shop/client_data.html',{'c':c})
def update_client_page(request):
    c=models.Client.objects.filter(user=request.user).first()
    return render(request,'shop/update_client.html',{'c':c})
def update_client(request):
    c=models.Client.objects.filter(user=request.user).first()
    c.phone=request.POST['phone']
    c.student_id=request.POST['student_id']
    if request.POST['TA_active']=="TA":
        c.TA_active=True
    else:
        c.TA_active=False
    c.save()
    return redirect('shop:clientdata')
