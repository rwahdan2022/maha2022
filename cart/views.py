from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from .models import * 
from .utils import cookieCart, cartData, guestOrder
import json
import datetime
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.core.mail import EmailMessage
from .forms import ProductForm, CatForm, DocumentForm

def aboutme(request):
	return render(request,'about.html',{})

def add_cat(request):
	submitted = False

	if request.method=="POST":

		form = CatForm(request.POST or None, request.FILES or None)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add_cat?submitted=True')
		
		else:

			form = CatForm
			
			if 'submitted' in request.GET:
				submitted = True

	return render(request, 'add_cat.html', {'form':form, 'submitted':submitted})

def add_product(request):
	submitted = False

	if request.method=="POST":
		
		form = ProductForm(request.POST or None, request.FILES or None)
		
		if form.is_valid():
			form.save()

		return HttpResponseRedirect('/add_product?submitted=True')
	
	else:
		
		form = ProductForm
		if 'submitted' in request.GET:
			submitted = True

	return render(request, 'add_product.html', {'form':form, 'submitted':submitted})

def transactions(request,order):
	if request.user.is_authenticated:
		total = 0
		done = 0
		filename=""
		fileurl=""
		ext=""
		size=""
		thedate=""
		theimage=""
		theimage2=""
		thequantity=""
		items = []
		product_name = []
		transaction_id = ""
		theconfirmation = False

		order = order
		item_list = OrderItem.objects.filter(order = order)
		
		form = DocumentForm()

		for order in item_list:

			items.append("https://cfe2.ap-south-1.linodeobjects.com" + order.product.imageURL)
			product_name.append(order.product.name)

			if order.order.payment_date:
				done = 1
				thedate = order.order.payment_date 
			else:
				done = 0
				thedate = "Not Paid Yet"
 	
			if order.order.pay_confirm:
				done2 = 0
			else:
				done2 = 1
				theconfirmation = order.order.pay_confirm
			
			total = total + (order.product.price * order.quantity)
			order_id = order.order
			order_date = order.order.date_ordered
			thecustomer = order.order.customer
			theimage = order.order.image
			thequantity = order.quantity
			customer_email = order.order.customer.email
			transaction_id = order.order.transaction_id

		if request.method=='POST':

			if request.user.is_authenticated:

				if request.user.is_superuser:

					subject = "Thank you for your payment!"
					to = customer_email
					template = get_template("email_template3.html")
					context = { 
						'thecustomer':thecustomer,'transaction_id' : transaction_id, 'total':total, 
						'item_list': item_list, 'done2':done2,'theconfirmation':theconfirmation,
					}

					html = template.render(context)
		
					message = EmailMessage(subject, html, settings.EMAIL_HOST_USER, [to])
					message.content_subtype = 'html' # this is required because there is no plain text email message
					message.send()

					item_list2 = Order.objects.filter(id = order.order.id)

					for order in item_list2:

						order.pay_confirm = True
						order.save()

					return redirect('store')

				else:

					form = DocumentForm(request.POST or None, request.FILES or None)

					if form.is_valid():
						item_list2 = Order.objects.filter(id = order.order.id)
						

						for order in item_list2:
							order.image = form.cleaned_data.get('image')
							order.payment_date = datetime.datetime.now()
							order.pay_confirm = False
							order.save()

					subject = "Thank you for your payment!"
					to = request.user.email
					template = get_template("email_template2.html")
					context = {'name': request.user.first_name,'theconfirmation':theconfirmation, 
				    					'transaction_id' : transaction_id, 'total':total, 
				    					'item_list': item_list,}
								
					html = template.render(context)
					message = EmailMessage(subject, html, settings.EMAIL_HOST_USER, [to])
					message.content_subtype = 'html' # this is required because there is no plain text email message
					message.send()

					return redirect('store')

		return render(request, 'transactions/show_transactions.html',
				{'item_list': item_list, 'total': total, 'order_id':order_id, 'order_date':order_date, 
				'thecustomer':thecustomer, 'done':done, 'thedate':thedate, 'filename':filename, 'fileurl':fileurl,
				'ext':ext, 'size':size, 'theimage':theimage, 'thequantity':thequantity, 'done2':done2, 'form':form})

	else:

		return redirect('login')

def BeforeTransactions(request):

	if request.user.is_authenticated:
		if request.user.is_superuser:
			order_list = Order.objects.all()

			for order in order_list:

				if order.pay_confirm == True:
					themessage2 = "There are no awaiting confirmation orders!"
					return render(request, 'transactions/transactions.html',{'order_list':order_list,})
				else:
					return render(request, 'transactions/transactions.html',
						{'order_list': order_list})
		else:
			order_list = Order.objects.filter(customer = request.user.id)
			return render(request, 'transactions/transactions.html',
				{'order_list': order_list})
	else:

		return redirect('login')

def store(request):

	data = cartData(request)
	path = ""

	cartItems = data['cartItems']
	order = data['order']
	items = data['items'] 

	products = Product.objects.all()
	cats = Category.objects.all()

	path = "static/cart/images/"

	category = request.GET.get('category')

	if category == None:
		p = Paginator(products.order_by("category"),2)
	else:
		p = Paginator(products.filter(category__name=category),2)

	page = request.GET.get('page')
	theproducts = p.get_page(page)

	context = {'products':products, 'cats':cats, 'cartItems':cartItems, 'theproducts': theproducts, 'path':path}
	return render(request, 'cart/store.html', context)

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	# send email - working need to add items...

	from django.core.mail import send_mail
	from django.template.loader import render_to_string
	from django.conf import settings

	subject = "Thank you for your purchase!"
	template = render_to_string('cart/email_template.html', {'name': request.user.first_name, 
		'transaction_id' : transaction_id, 'total':total})

	to = request.user.email
	res = send_mail(subject , template , settings.EMAIL_HOST_USER, [to], fail_silently=True)

	return JsonResponse('Payment submitted..', safe=False)