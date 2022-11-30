from django.db.models import Q
from django.shortcuts import render

from shop.models import Products
# Create your views here.

def SearchResults(request):
    products=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        products=Products.objects.all().filter(Q(name__contains=query) | Q(description__contains='q'))
        return render(request,'search.html',{'query':query,'products':products})