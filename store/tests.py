import profile
from django.test import RequestFactory, TestCase

# Create your tests here.
from django.urls import reverse, resolve
from .views import business, customer, staff
from django.test import TestCase, Client
from django.contrib.auth.models import User
from store.models import Product, Customer,User,Contact, Product, OrderItem, Category, Profile
from store.cart import Cart
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from .forms import ContactForm, MyUserCreationForm, MyUserChangeForm, RegistrationForm, ProfileForm, Customer_ProfileForm, UploadForm



# <--TESTS FOR URLS-->
class TestURLs(TestCase):
    def test_staff_urls(self):
        # Test staff URLs
        self.assertEqual(reverse('staff:paymentoptions'), '/staff/paymentoptions/')
        self.assertEqual(reverse('staff:returns'), '/staff/returns/')
        self.assertEqual(reverse('staff:register'), '/staff/register/')
        self.assertEqual(reverse('staff:login'), '/staff/login/')
        self.assertEqual(reverse('staff:logout'), '/staff/logout/')
        self.assertEqual(reverse('staff:update_user'), '/staff/update_user/')
        self.assertEqual(reverse('staff:FAQS'), '/staff/FAQS/')
        self.assertEqual(reverse('staff:contact'), '/staff/contact/')
        self.assertEqual(reverse('staff:index'), '/staff/index/')
        self.assertEqual(reverse('staff:about'), '/staff/about/')
        self.assertEqual(reverse('staff:profile_redirect'), '/staff/profile_redirect/')
        self.assertEqual(reverse('staff:account'), '/staff/account/')
        self.assertEqual(reverse('staff:homepage'), '/staff/homepage/')
        self.assertEqual(reverse('staff:services'), '/staff/services')
        self.assertEqual(reverse('staff:web_settings'), '/staff/web_settings/')
    
    def test_business_urls(self):
        # Test business URLs
        self.assertEqual(reverse('business:profile'), '/business/profile/')
        self.assertEqual(reverse('business:dashboard'), '/business/dashboard')
        self.assertEqual(reverse('business:businesscustomer', args=['123']), '/business/businesscustomer/123/')
        
        self.assertEqual(reverse('business:upload'), '/business/upload')
        self.assertEqual(reverse('business:updateProduct', args=['456']), '/business/updateProduct/456/')
        self.assertEqual(reverse('business:deleteProduct', args=['789']), '/business/deleteProduct/789/')
    
    def test_customer_urls(self):
        # Test customer URLs
        self.assertEqual(reverse('customer:dashboard'), '/customer/dashboard')
        self.assertEqual(reverse('customer:profile'), '/customer/profile/')
        self.assertEqual(reverse('customer:product', args=[123]), '/customer/product/123')
        self.assertEqual(reverse('customer:category', args=['electronics']), '/customer/category/electronics')
        self.assertEqual(reverse('customer:cart_summary'), '/customer/cart_summary')
        self.assertEqual(reverse('customer:checkout'), '/customer/checkout/')
        self.assertEqual(reverse('customer:cart_add'), '/customer/cart_add/')
        self.assertEqual(reverse('customer:cart_update'), '/customer/cart_update/')
        self.assertEqual(reverse('customer:cart_delete'), '/customer/cart_delete/')
        self.assertEqual(reverse('customer:search'), '/customer/search_items/')
        self.assertEqual(reverse('customer:languages'), '/customer/languages/')
        
        
# <--TESTS FOR VIEWS-->





class TestBusinessViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
    
    def test_profile_view(self):
        response = self.client.get(reverse('business:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'business/Profile.html')

    def test_dashboard_view(self):
        response = self.client.get(reverse('business:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'business/dashboard.html')

    
    def test_businesscustomer_view(self):
        customer = Customer.objects.create(name='Test Customer')
        response = self.client.get(reverse('business:businesscustomer', args=[customer.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'business/businesscustomer.html')

    # def test_upload_view(self):
    #     response = self.client.get(reverse('business:upload'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'business/upload.html')

    # def test_updateProduct_view(self):
    #     product = Product.objects.create(name='Test Product', price=10.00)
    #     response = self.client.get(reverse('business:updateProduct', args=[product.pk]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'business/upload.html')

    # def test_deleteProduct_view(self):
    #     product = Product.objects.create(name='Test Product', price=10.00)
    #     response = self.client.get(reverse('business:deleteProduct', args=[product.pk]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'business/delete.html')




class TestCustomerViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_dashboard_view(self):
        response = self.client.get(reverse('customer:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/dashboard.html')

    

    # def test_category_view(self):
    #     category = Category.objects.create(name='Test Category')
    #     response = self.client.get(reverse('customer:category', args=[category.name.replace(' ', '-')]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'customer/category.html')

    def test_checkout_view(self):
        response = self.client.get(reverse('customer:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/checkout.html')

    # def test_product_view(self):
    #     product = Product.objects.create(name='Test Product', price=10.00)
    #     response = self.client.get(reverse('customer:product', args=[product.pk]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'customer/product.html')

    def test_cart_summary_view(self):
        response = self.client.get(reverse('customer:cart_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/cart_summary.html')

    def test_profile_view(self):
        response = self.client.get(reverse('customer:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/Profile.html')

    # def test_cart_add_view(self):
    #     product = Product.objects.create(name='Test Product', price=10.00)
    #     response = self.client.post(reverse('customer:cart_add'), {'product_id': product.pk, 'product_qty': 1}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()['qty'], 1)

    # def test_cart_update_view(self):
    #     product = Product.objects.create(name='Test Product', price=10.00)
    #     cart = Cart(self.client.session)
    #     cart.add(product=product, quantity=1)
    #     response = self.client.post(reverse('customer:cart_update'), {'productid': product.pk, 'product_qty': 2}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()['qty'], 2)

    # def test_cart_delete_view(self):
    
    #     product = Product.objects.create(name='Test Product', price=10.00)
    #     cart = Cart(self.client.session)
    #     cart.add(product=product, quantity=1)
    #     response = self.client.post(reverse('customer:cart_delete'), {'product_id': product.pk}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()['product'], str(product.pk))

    def test_languages_view(self):
        response = self.client.get(reverse('customer:languages'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/languages.html')
        
        
        
# <-- TESTS FOR MODELS--->

class ContactModelTest(TestCase):
    def test_contact_creation(self):
        contact = Contact.objects.create(name='John Doe', email='john@example.com', message='Hello')
        self.assertEqual(contact.name, 'John Doe')
        self.assertEqual(contact.email, 'john@example.com')
        self.assertEqual(contact.message, 'Hello')

# class ProductModelTest(TestCase):
#     def test_product_imageURL(self):
#         product = Product.objects.create(name='Test Product', price=10.00)
#         self.assertEqual(product.imageURL(), ' ')

# class OrderItemModelTest(TestCase):
#     def test_orderitem_creation(self):
#         product = Product.objects.create(name='Test Product', price=10.00)
#         order_item = OrderItem.objects.create(product=product, quantity=2)
#         self.assertEqual(order_item.product, product)
#         self.assertEqual(order_item.quantity, 2)




User = get_user_model()

class ContactFormTest(TestCase):
    def test_contact_form_valid(self):
        form_data = {'name': 'John Doe', 'email': 'john@example.com', 'message': 'Hello'}
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid(self):
        form_data = {'name': '', 'email': 'invalid_email', 'message': ''}
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())




# TESTS FOR FORMS

class TestUploadForm(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_valid_form(self):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'file_content', content_type='image/jpeg')
        form_data = {
            'name': 'Test Product',
            'price': 10.99,
            'image': image,
            'description': 'This is a test product',
            'category': self.category.pk
        }
        form = UploadForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'name': '',  # empty name
            'price': 'invalid price',  # invalid price
            'image': '',  # no image
            'description': '',  # empty description
            'category': ''  # no category
        }
        form = UploadForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

    def test_category_queryset(self):
        form = UploadForm()
        self.assertEqual(list(form.fields['category'].queryset), [self.category])

    def test_form_fields(self):
        form = UploadForm()
        self.assertEqual(len(form.fields), 5)
        self.assertIn('name', form.fields)
        self.assertIn('price', form.fields)
        self.assertIn('image', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('category', form.fields)
        
        
class TestContactForm:
    def test_contact_form_valid(self):
        form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'Hello, this is a test message.'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
        contact = form.save()
        self.assertEqual(contact.name, 'John Doe')
        self.assertEqual(contact.email, 'johndoe@example.com')
        self.assertEqual(contact.message, 'Hello, this is a test message.')


        
class CustomerProfileFormTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')


    def test_profile_authenticated_with_profile(self):
        profile = Profile.objects.create(user=self.user)
        response = self.client.get(reverse('customer:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['profile'], Profile)
        self.assertIsInstance(response.context['form'], Customer_ProfileForm)

    def test_profile_authenticated_without_profile(self):
        response = self.client.get(reverse('customer:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context.get('profile'))
        self.assertIsInstance(response.context['form'], Customer_ProfileForm)

    def test_profile_post_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'type': 'BUSINESS'
        }
        response = self.client.post(reverse('customer:profile'), form_data)
        self.assertEqual(response.status_code, 200)  # Redirect after successful form submission
        

    def test_profile_post_invalid_form(self):
        response = self.client.post(reverse('customer:profile'), {'invalid_data': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
       
class TestRegistrationForm(TestCase):
    def test_registration_form_valid(self):
        """
        Test that the form is valid with correct data
        """
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'type': User.Types.CUSTOMER  # Provide a valid user type
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form is not valid: {form.errors}")
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.type, User.Types.CUSTOMER)

    def test_registration_form_invalid(self):
        """
        Test that the form is invalid with incorrect data
        """
        form_data = {
            'username': '',  # Missing username
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'type': User.Types.CUSTOMER
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class MyUserCreationFormTest(TestCase):

    def test_form_valid(self):
        """Test that the form is valid with correct data."""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'type': 'some_type',
            'name': 'Test Name',
            'password1': 'strong_password',
            'password2': 'strong_password',
        }
        form = MyUserCreationForm(data=form_data)
        if form.is_valid():
            print("Cleaned data:", form.cleaned_data)
            user = form.save()
            self.assertIsInstance(user, User, "The form should create a User instance")


    def test_form_invalid_missing_username(self):
        """Test that the form is invalid if the username is missing."""
        form_data = {
            'email': 'test@example.com',
            'type': 'some_type',
            'name': 'Test Name',
            'password1': 'strong_password',
            'password2': 'strong_password',
        }
        form = MyUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid(), "The form should be invalid without a username")
        self.assertIn('username', form.errors, "The form should raise an error for missing username")



    def test_form_invalid_missing_type(self):
        """Test that the form is invalid if the type is missing."""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'name': 'Test Name',
            'password1': 'strong_password',
            'password2': 'strong_password',
        }
        form = MyUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid(), "The form should be invalid without a type")
        self.assertIn('type', form.errors, "The form should raise an error for missing type")

    def test_form_invalid_missing_name(self):
        """Test that the form is invalid if the name is missing."""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'type': 'some_type',
            'password1': 'strong_password',
            'password2': 'strong_password',
        }
        form = MyUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid(), "The form should be invalid without a name")
        self.assertIn('name', form.errors, "The form should raise an error for missing name")

    def test_form_invalid_password_mismatch(self):
        """Test that the form is invalid if the passwords do not match."""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'type': 'some_type',
            'name': 'Test Name',
            'password1': 'strong_password',
            'password2': 'different_password',
        }
        form = MyUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid(), "The form should be invalid if passwords don't match")
        self.assertIn('password2', form.errors, "The form should raise an error for password mismatch")