from django.db import models
from django.urls import reverse
from registration.models import Account
from django.db.models import Avg,Count
from django.core.files.images import ImageFile
from PIL import Image
# Create your models here.




class Category(models.Model):
    category_name    = models.CharField(max_length=50,unique=True)
    slug             = models.SlugField(max_length=50,unique=True)
    description      = models.CharField(max_length=300,blank=True)
    category_image   = models.ImageField(upload_to = 'photos/category')
   

    class Meta:
        verbose_name        = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])    


    def __str__(self):
        return self.category_name
    

    def save(self):
        if self.category_image:          
            super(Category, self).save()
            category_image = Image.open(self.category_image)
            (width , height) = category_image.size     
            size = (720,480)
            image = category_image.resize(size, Image.ANTIALIAS)
            image.save(self.category_image.path)
        # else:
        #     if self.rent_property_category:  
        #         super(SellProperty, self).save()




class Sub_Category(models.Model):
    sub_categoryname = models.CharField(max_length=50,unique=True)
    slug        = models.SlugField(max_length=50,unique=True)
    description      = models.CharField(max_length=300,blank=True)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_category_image       = models.ImageField(upload_to = 'photos/sub_category')


    def get_url(self):
        return reverse('products_by_subcategory',args=[self.category.slug, self.slug])  

    def __str__(self):
        return self.sub_categoryname





class Product(models.Model):
    product_name    = models.CharField(max_length=100,unique=True)
    slug            = models.SlugField(max_length=100,unique=True)
    description     = models.TextField(max_length=300,blank = True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to = 'photos/product')
    images1          = models.ImageField(upload_to = 'photos/product',blank=True,null=True)
    images2          = models.ImageField(upload_to = 'photos/product',blank=True,null=True)
    images3          = models.ImageField(upload_to = 'photos/product',blank=True,null=True)
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    brand        = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    phone_name    = models.ForeignKey(Sub_Category,on_delete=models.CASCADE)  


    def get_url(self):
        return reverse('product_details',args=[self.brand.slug,self.phone_name.slug,self.slug])
     
    def __str__(self) :
        return self.product_name 



    def averageReview(self):
        reviews  = ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg= float(reviews['average'])
        return avg        

    def countReview(self):
        reviews  = ReviewRating.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count= int(reviews['count'])
        return count  

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category = 'color', is_active=True )

    def sizes(self):
        return super(VariationManager,self).filter(variation_category = 'size', is_active=True )

variation_category_choice =  (
    ('color','color'),
    ('size','size'),
)


class Variation(models.Model):
    product     = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category  =   models.CharField(max_length=100,choices= variation_category_choice,)
    variation_value = models.CharField(max_length=100,null=True)
    is_active   = models.BooleanField(default=True )
    created_date    = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

       




class Cart(models.Model):
    cart_id = models.CharField(max_length=100,)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class Cartitems(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product

    def sub_total(self):
        return self.product.price * self.quantity



class ReviewRating(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    subjects = models.CharField(max_length=50,blank = True)
    review = models.TextField(max_length=500,blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
             return self.subjects