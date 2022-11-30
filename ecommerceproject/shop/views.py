from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Products


# Create your views here.
# def index(request):
#     return render(request,'base.html')

def allProdCat(request, c_slug=None):
    c_page = None
    products_list = None
    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products_list = Products.objects.all().filter(category=c_page, available=True)
    else:
        products_list = Products.objects.all().filter(available=True)

    paginator = Paginator(products_list, 6)

    try:
        page_number = int(request.GET.get('page', '1'))
    except:
        page_number = 1

    try:
        products = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, "category.html", {'category': c_page, 'products': products})


def proDetail(request, cat_slug, prod_slug):
    try:
        product = Products.objects.get(category__slug=cat_slug, slug=prod_slug)
    except Exception as e:
        raise e

    return render(request, 'product.html', {'product': product})
