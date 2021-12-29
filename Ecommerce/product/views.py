from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.template import Context, Template, context
from django.template.loader import render_to_string
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import NewUserForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
import math
from django.contrib.auth.decorators import login_required




# Create your views here.
quantity = 1

def supportPage(request):

	context = {}

	return render(request, "product/support.html", context)
	 

def homePage(request):
	if request.method=='GET':
		# Carousel Slider
		sliderImg = SliderImage.objects.all()

		page_title = "Home Page"
		product_list = ProductImage.objects.all()
		category_list = Category.objects.all()

		#Pagination
		page = request.GET.get('page', 1)
		paginator = Paginator(product_list, 12)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
	    
		except EmptyPage:
			products = paginator.page(paginator.num_pages)

			
	
		context = {
			'product_list': product_list, 
			'page_title': page_title, 
			'sliderImg': sliderImg, 
			'category_list':category_list,
			'products':products,
			
			}

		return render(request, 'product/homePage.html', context)


def productCategory(request, category_slug=None):

	category = None
	category_list = Category.objects.all()
	product_img = ProductImage.objects.all()
	products = Product.objects.all()

# Carousel Slider
	sliderImg = SliderImage.objects.all()


	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		product_img = product_img.filter(category=category)
		#Pagination
		page = request.GET.get('page', 1)
		paginator = Paginator(product_img, 13)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
	    
		except EmptyPage:
			products = paginator.page(paginator.num_pages)
			


		context = {'category':category, 'category_list':category_list, 'products':products,
		
			'sliderImg': sliderImg, 
			'category_list':category_list,}




	return render(request, 'product/homePage.html', context)


def productDetails(request, pk):

	product = Product.objects.get(pk=pk)
	img = ProductImage.objects.filter(product=product)

	review = Review.objects.filter(product=product)

	rate = 1
	i = 1
	for rev in review:
		i = i+1
		rate = rev.rate+rate 

	avg_rate = float(rate/i)

	avg_rate = math.ceil(avg_rate)


	
	template = loader.get_template('product/productDetails.html')
	context = {'product': product, 'img':img, 'review':review, 'avg_rate': avg_rate}
	return HttpResponse(template.render(context, request))


def AddtoCartView(request,id):

	#request.session.set_expiry(120000)

	product_id = get_object_or_404(Product, id=id)
	product_obj = Product.objects.get(id=product_id.id)
	
	#check if the card
	try:
		cart_id = request.session['cart_id']
	except:
		cart_id = None
	if cart_id:
		cart_obj = Cart.objects.get(id=cart_id)
		this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
		
		#item already exists in the cart
		if this_product_in_cart.exists():
			if product_obj.discount > 0:
				cartproduct = this_product_in_cart.first()
				cartproduct.quantity += 1
				cartproduct.subtotal += product_obj.discount_price
				cartproduct.save()
				cart_obj.total += product_obj.discount_price
				cart_obj.save()
			else:
				cartproduct = this_product_in_cart.first()
				cartproduct.quantity += 1
				cartproduct.subtotal += product_obj.price
				cartproduct.save()
				cart_obj.total += product_obj.price
				cart_obj.save()

		#new item is added in the cart
		else:
			if product_obj.discount > 0:
				cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.discount_price, quantity=1, subtotal=product_obj.discount_price)
				cart_obj.total += product_obj.discount_price
				cart_obj.save()
			else:
				cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1, subtotal=product_obj.price)
				cart_obj.total += product_obj.price
				cart_obj.save()
		

	else:
		if product_obj.discount > 0:
			cart_obj = Cart.objects.create(total=0)
			request.session['cart_id'] = cart_obj.id
			cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.discount_price, quantity=1, subtotal=product_obj.discount_price)
			cart_obj.total += product_obj.discount_price
			cart_obj.save()
		else:
			cart_obj = Cart.objects.create(total=0)
			request.session['cart_id'] = cart_obj.id
			cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1, subtotal=product_obj.price)
			cart_obj.total += product_obj.price
			cart_obj.save()

		

	context = {'cart_obj':cart_obj}
	
	return render(request, 'product/addToCart.html', context)





def individualCart(request):
	cart_id = request.session.get("cart_id", None)
	try:
		cart_obj = Cart.objects.get(id=cart_id)
	except Cart.DoesNotExist:
		cart_obj = None

	if Cart.objects.filter(id=cart_id).exists():
		context = {'cart_obj': cart_obj,}
		return render(request, 'product/addToCart.html', context)

	else:
		msg = "Your cart is empty. Please continue shopping."
		context = {'msg':msg}
		return render(request, 'product/empty.html', context)
		



	



class ManageCart(View):
	def get(self, request, *arg, **kwargs):
		item_id = self.kwargs["item_id"]
		action = request.GET.get('action')
		cp_obj = CartProduct.objects.get(id=item_id)
		cart_obj = cp_obj.cart
		
		#print(item_id, action)
		if action == "inc":
			cp_obj.quantity += quantity
			cp_obj.subtotal += cp_obj.rate
			cp_obj.save()
			cart_obj.total += cp_obj.rate
			cart_obj.save()

		elif action == "dec":
			cp_obj.quantity -= 1
			cp_obj.subtotal -= cp_obj.rate
			cp_obj.save()
			cart_obj.total -= cp_obj.rate
			cart_obj.save()
			if cp_obj.quantity == 0:
				cp_obj.delete()
		elif action == "rmv":
			cart_obj.total -= cp_obj.subtotal
			cart_obj.save()
			cp_obj.delete()

		return render(request, 'product/addToCart.html', {'cart_obj':cart_obj})	
		#return HttpResponseRedirect(reverse('viewCart'))
		#return HttpResponseRedirect(request.META.get('add-to-cart'))
		

#Checkout 


@login_required(login_url='/login/')
def checkout(request, cart_id):

	cart_id = request.session.get("cart_id", None)
	if cart_id:
		cart_obj = Cart.objects.get(id=cart_id)
	else:
		cart_obj = None


		
    

	form = OrderForm()
	if request.method=='POST':
		form = OrderForm(request.POST)
		if form.is_valid:
			if cart_id:
				form.instance.cart = cart_obj
				form.instance.subtotal = cart_obj.total
				form.instance.discount = 0
				form.instance.total = cart_obj.total
				form.instance.order_status = "Order Received"
				form.save()
				del request.session['cart_id']




			else:
				return redirect('/')


			

			return render(request, "product/orderConfirmation.html")

	else:
		form = OrderForm()

	context = {'form': form, 'cart_obj':cart_obj,}


	return render(request, 'product/checkout.html', context)


	
#Registration
def registerRequest(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("homePage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="product/register.html", context={"register_form":form})

#Login
def loginRequest(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("homePage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="product/login.html", context={"login_form":form})

#Logout
def logoutRequest(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("homePage")



#Search Operation

def searchOperation(request):
	if request.method == "POST":
		prodImg = ProductImage.objects.all()
		query_name = request.POST.get('name', None)
		if query_name:
			results = Product.objects.filter(name__contains=query_name)

			context={'results':results, 'prodImg':prodImg}
			return render(request, 'product/productSearch.html', context)

	return render(request, 'productSearch.html')
        

        
            
#Review & Rating
@login_required(login_url='/login/')
def reviewRate(request):
	if request.method == "GET":
		prod_id = request.GET.get('prod_id')
		product = Product.objects.get(id=prod_id)
		comment = request.GET.get('comment')
		rate = request.GET.get('rating')
		user = request.user
		if comment and rate != None:
			Review(user=user, product=product, comment=comment, rate=rate).save()



		

		return redirect("productDetails", prod_id)




    
	
            
            

    

	
	
