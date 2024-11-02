from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.urls import reverse
from django.contrib.postgres.fields import JSONField  # Import this for JSONField
from PIL import Image
from datetime import datetime

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

class User(AbstractUser):
    class Types(models.TextChoices):
        BUSINESS = "BUSINESS", "BUSINESS"
        CUSTOMER = "CUSTOMER", "CUSTOMER"
    
    type = models.CharField(
        ('Type'), max_length=50, choices=Types.choices, default=Types.BUSINESS)
    
    name = models.CharField(("Name of User"), blank=True, max_length=225)
    
    # Custom fields for storing additional info
    custom_fields_for_business = models.JSONField(blank=True, null=True)
    custom_fields_for_customer = models.JSONField(blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

class BusinessManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.BUSINESS)

class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)

class CustomPermission(models.Model):
    BUSINESS_PERMISSIONS = [
        ('Can add products', 'Can delete products'),
        ('Can view products', 'Can update products'),
        
    ]

    CUSTOMER_PERMISSIONS = [
        ('can view products', 'Can select products'),
         ('can comment', 'Can make payment'),
    ]
    
    # Add a method to retrieve permissions based on user type
    @staticmethod
    def get_permissions_for_user_type(user_type):
        if user_type == User.Types.BUSINESS:
            return CustomPermission.BUSINESS_PERMISSIONS
        elif user_type == User.Types.CUSTOMER:
            return CustomPermission.CUSTOMER_PERMISSIONS
        else:
            return []

class Business(User):
    objects = BusinessManager()
    
    class Meta:
        proxy = True
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.BUSINESS
        return super().save(*args, **kwargs)
    
    def get_permissions(self):
        return CustomPermission.get_permissions_for_user_type(self.type)

class Customer(User):
    objects = CustomerManager()
    
    class Meta:
        proxy = True
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.CUSTOMER
        return super().save(*args, **kwargs)
    
    def get_permissions(self):
        return CustomPermission.get_permissions_for_user_type(self.type)

class StaffUser(User):
    class Meta:
        proxy = True

    def get_permissions(self):
        return CustomPermission.get_permissions_for_user_type(self.type)

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        
        verbose_name_plural = 'categories'
class Product(models.Model):
    
    image = models.ImageField(upload_to='Products')
    name = models.CharField(max_length=200, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category,null=True, on_delete=models.SET_NULL, default=1)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name
    
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=" "
        return url
    
    
    
class Comment(models.Model):
    product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
    commenter_name = models.CharField(max_length=200)
    comment_body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.product.name, self.commenter_name)




    
class Order(models.Model):
    
   
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True, blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=True)
    transaction_id=models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    
class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity=models.IntegerField(default=0,null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
       total = self.product.price * self.quantity
       return total 



class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address=models.CharField(max_length=200,null=False) 
    district=models.CharField(max_length=200,null=False)
    town=models.CharField(max_length=200,null=False)
    
    def __str__(self) -> str:
        return self.address

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default_pic.jpg', upload_to="profile_pics")
    gender = models.CharField(default='', max_length=10, blank=False)
    contact = models.CharField(max_length=10, blank=False)
    telephone = models.CharField(max_length=10, blank=False)
    website = models.CharField(max_length=70, blank=False)
    business_name = models.CharField(max_length=20, blank=False)
    category = models.CharField(max_length=50, blank=False)
    address_line_1 = models.CharField(max_length=100, blank=False)
    address_line_2 = models.CharField(max_length=100, blank=False)
    pobox = models.CharField(max_length=10, blank=False)
    street = models.CharField(max_length=10, blank=False)
    state = models.CharField(max_length=50, blank=False)
    zip_code = models.CharField(max_length=10, blank=False)
    bio = models.CharField(default='', max_length=400, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    

class Customer_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default_pic.jpg', upload_to="profile_pics")
    gender = models.CharField(default='', max_length=10, blank=False)
    contact = models.CharField(max_length=10, blank=False)
    address_line_1 = models.CharField(max_length=100, blank=False)
    address_line_2 = models.CharField(max_length=100, blank=False)
    street = models.CharField(max_length=10, blank=False)
    state = models.CharField(max_length=50, blank=False)
    zip_code = models.CharField(max_length=10, blank=False)
  
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    