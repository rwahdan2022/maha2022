from django import forms
from django.forms import ModelForm
from .models import Product, Category, Order

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('image', )

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ('name','price','category','digital','image','video_name')
		
		labels = {

		'name': '',
		'price':	'',
		'category':	'',
		'digital': 'Digital?',
		'image': 'Upload Image',
		'video_name': '',	

		}

		widgets = {

		'name': forms.TextInput(attrs={'class':"form-control", "placeholder":"Product Name"}),
		'price':	forms.TextInput(attrs={'class':"form-control", "placeholder":"Product Price"}),
		'category':	forms.Select(attrs={'class':"form-control"}),
		'digital': forms.CheckboxInput(attrs={'class':'form-control'}),
		'image': forms.FileInput(attrs={'class':'form-control'}),
		'video_name': 	forms.TextInput(attrs={'class':"form-control", "placeholder":"Video Title"}),
		}

class CatForm(ModelForm):
	class Meta:
		model = Category
		fields = ('name',)
		labels = {'name': '',}
		widgets = {

		'name': forms.TextInput(attrs={'class':"form-control", "placeholder":"Category Name"}), }
