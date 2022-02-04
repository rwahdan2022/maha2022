from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView,PasswordResetView
from .forms import RegisterUserForm, EditProfileForm, PasswordChangingForm
from cart.utils import cookieCart, cartData, guestOrder
from cart.models import *
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.cache import cache_control


class PasswordsChangeView(PasswordChangeView):
	form_class = PasswordChangingForm
	success_url = reverse_lazy('store')

class UserEditView(generic.UpdateView):
	form_class = EditProfileForm
	template_name = 'authenticate/edit_profile.html'
	success_url = reverse_lazy('store')

	def get_object(self):
		return self.request.user

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if user.is_superuser:
				messages.success(request,"Admin login recorded!")
				login(request, user)
				return redirect('store')
			else:			
				login(request, user)
				return redirect('store')
		else:
			messages.success(request,"There was an error! Please check the username/password and try again")
			return redirect('login')
	else:
		return render(request, 'authenticate/login.html', {})

@cache_control(no_cache=True, must_revalidate=True)
def logout_user(request):	
	logout(request)
	messages.success(request,"You were logged off...")
	return redirect('store') 

def register_user(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			the_email = form.cleaned_data['email']
			
			customer, created = Customer.objects.get_or_create(
			email=the_email,
			)
			customer.name = first_name + " " + last_name
			user = authenticate(username=username, password= password)
			customer.user = user
			customer.save()			
			login(request,user)
			messages.success(request,"Registration successful")
			return redirect('store')				
	else:
		form = RegisterUserForm()


	return render(request, 'authenticate/register_user.html', {'form':form,})