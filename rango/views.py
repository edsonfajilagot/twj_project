from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm


def add_page(request, category_name_slug):
	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None
		
	if request.method == 'POST':
		form = PageForm(request.POST)
		
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				return category(request, category_name_slug)
		else:
			print form.errors

	else:
		form = PageForm()
		
	context_dict = {'form': form, 'category': cat}
	return render(request, 'rango/add_page.html', context_dict)

def add_category(request):
	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		
		if form.is_valid():
			form.save(commit=True)
			return index(request)
			#return add_category(request)
		else:
			print 'this code is executed'
			print form.errors	
	else:
		form = CategoryForm()

	return render(request, 'rango/add_category.html', {'form': form})
	 

def category(request, category_name_slug):
	context_dict = {}
	
	try:
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		
		context_dict['category'] = category
		
	except Category.DoesNotExist:
		pass	

	return render(request, 'rango/category.html', context_dict)

def index(request):
	# return HttpResponse("Rango says hey there world! <br/> <a href='/rango/about''>About</a>")
	category_list = Category.objects.order_by('-likes')[:3] 
	context_dict = {'boldmessage': "I am bold font from the context",
									'categories': category_list
									}
	
	return render(request, 'rango/index.html', context_dict)
	
def about(request):
	#return HttpResponse("Rango says here is the About page. <a href='/rango'>Index</a>")
	return render(request, 'rango/about.html')
	
def help(request):
	return HttpResponse("Welcome to Rango help. <a href='/rango'>Index</a>")



def register(request):
	# Boolean value will be set to True when registration is successful
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database
			user = user_form.save()

			# Now we hash the password
			user.set_password(user.password)
			user.save()

			# Since we need to set the user attr ourselves, we set the commit to False
			# This delays saving the model until we are ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user

			# Did the user provide the profile picture
			if 'picture' in request.FILES:
				profile.picure = request.FILES['picture']

			# Now save the profile
			profile.save()

			# Update the variable, as template was successful	
			registered = True	

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}	
	return render(request, 'rango/register.html',context_dict)		