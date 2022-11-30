from django.db import models
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='category',blank=True)

    class Meta:
        ordering=('name',)
        verbose_name='Category'
        verbose_name_plural='Categories'

    def get_url(self):
        return reverse('shop:products_by_category',args=[self.slug])


    def __str__(self):
        return "{}".format(self.name)

class Products(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True) # slug is used to automatically generate url from name for each record
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='product',blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField(blank=True)
    stock=models.IntegerField(blank=True)
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('name',)
        verbose_name='Product'
        verbose_name_plural='Products'

    def get_url(self):
        return reverse('shop:product_details',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.name

