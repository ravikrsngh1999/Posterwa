from django.db import models

# Create your models here.

class Category(models.Model):
    name  = models.CharField(max_length = 30)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    name = models.CharField(max_length = 30)

    def __str__(self):
        return self.category.name + " - " + self.name


class Product(models.Model):

    def upload_image_to(self,flename):
        file = "Posters"
        return f'{file}/{self.title}'

    title = models.CharField(max_length = 100,default="")
    subcategory = models.ForeignKey(SubCategory,on_delete = models.CASCADE,null=True,blank=True)
    description = models.TextField(max_length = 200,default="")
    selling_price = models.IntegerField(default = 0)
    cost_price = models.IntegerField(default = 0)
    on_discount = models.BooleanField(default = False)
    is_featured = models.BooleanField(default=False)
    avg_rating = models.CharField(max_length = 4,default = "")
    no_of_review = models.IntegerField(default = 0)
    no_of_orders = models.IntegerField(default = 0)
    size = models.CharField(max_length = 20)
    image1= models.ImageField(blank=False, upload_to=upload_image_to)
    image2= models.ImageField(blank=False, upload_to=upload_image_to)
    image3= models.ImageField(blank=False, upload_to=upload_image_to)
    image4= models.ImageField(blank=False, upload_to=upload_image_to)
    out_of_stock = models.BooleanField(default=False)

    def __str__(self):
        return self.title




class State(models.Model):
    name = models.CharField(max_length = 20)
    price = models.IntegerField(default = 60)

    def __str__(self):
        return self.name




class CouponCode(models.Model):
    name = models.CharField(max_length=6)
    offer = models.IntegerField(default = 5)
    above = models.IntegerField(default = 150)

    def __str__(self):
        return self.name



class Order(models.Model):
    order_receipt= models.CharField(max_length=50)
    order_id = models.CharField(max_length=50)
    razorpay_payment_id = models.CharField(max_length=50)
    razorpay_order_id = models.CharField(max_length=50)
    razorpay_signature = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    total = models.CharField(max_length=50)
    subtotal = models.CharField(max_length=50)
    products = models.TextField()
    order_note = models.CharField(max_length=200)
    shipping_charges = models.CharField(max_length=50)
    couponname = models.CharField(max_length=50,null=True,blank=True)
    discount = models.CharField(max_length = 5,null=True,blank=True)


    def __str__(self):
        return self.order_id
