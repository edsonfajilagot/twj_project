import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twj_project.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
	finance_cat = add_cat('Finance')
	
	add_page(cat=finance_cat,
		title = "Finance 101",
		url = "http://finance101.com/")


	programming_cat = add_cat('Programming')
	
	add_page(cat=programming_cat,
		title = "Programming 101",
		url = "http://docs.python.org/2/tutorial/")

	python_cat = add_cat('Python')
	
	add_page(cat=python_cat,
		title = "Official Python Tutorial",
		url = "http://docs.python.org/2/tutorial/")
		
	add_page(cat=python_cat,
		title="How to Think Like a Computer Scientist",
		url = "http://www.greenteapress.com/thinkpython/")
		
	hana_cat = add_cat('SAP HANA Tests')
			
	add_page(cat=hana_cat,
		title = "SAP HANA Tests",
		url = "http://www.saphana-tests.com/")	
		
	#Print out what we have added
	for c in Category.objects.all():
		for p in Page.objects.filter(category=c):
			print "- {0} - {1}".format(str(c), str(p))		
	

def add_page(cat, title, url, views=0):
	p = Page.objects.get_or_create(category=cat, title=title)[0]
	p.url = url
	p.views = views
	p.save()
	return p	
	
def add_cat(name):
	#c = Category.objects.get_or_create(name=name)[0]
	c = Category.objects.get_or_create(name=name)[0]
	c.save()
	return c	
	
	
if __name__ == '__main__':
	print "Starting Rango population script..."
	populate()	
