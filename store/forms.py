       
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile
from .models import *
from django.forms import ModelForm
from django import forms
from .models import Contact
# If you're using Django's built-in User model
# from django.contrib.auth.models import User

User = get_user_model()

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'type', 'name')  # Add custom fields here

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['type'].required = True
        self.fields['name'].required = True
        

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'  # This will include all fields of the user model

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['type'].required = True
        self.fields['name'].required = True


class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, max_length=15)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    type = forms.CharField(label='Type')  # Add 'type' field to the form

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'type']  # Include 'password1' and 'password2'

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.type = self.cleaned_data["type"]
        if commit:
            user.save()
        return user




class ProfileForm(forms.ModelForm):
    image = forms.ImageField(label = 'image')
    gender = forms.CharField(label = 'gender')
    contact = forms.CharField(label = 'contact')
    telephone = forms.CharField(label = 'telephone')
    website = forms.CharField(label = 'website')
    business_name = forms.CharField(label = 'business_name')
    category = forms.CharField(label = 'category')
    address_line_1 = forms.CharField(label = 'address_line_1')
    address_line_2 = forms.CharField(label = ' address_line_2')
    pobox = forms.CharField(label = 'pobox')
    street = forms.CharField(label = 'street')
    state = forms.CharField(label = 'state')
    zip_code = forms.CharField(label = 'zip_code')
    bio = forms.CharField(label = 'bio')
    
    class Meta:
        model = Profile
        fields = ('image', 'gender', 'contact', 'telephone','website','business_name','category', 'address_line_1', 'address_line_2', 'pobox', 'street', 'state', 'zip_code', 'bio')
        
        
class Customer_ProfileForm(forms.ModelForm):
    image = forms.ImageField(label = 'image')
    gender = forms.CharField(label = 'gender')
    contact = forms.CharField(label = 'contact')
    address_line_1 = forms.CharField(label = 'address_line_1')
    address_line_2 = forms.CharField(label = ' address_line_2')
    street = forms.CharField(label = 'street')
    state = forms.CharField(label = 'state')
    zip_code = forms.CharField(label = 'zip_code')
  
    
    class Meta:
        model = Profile
        fields = ('image', 'gender', 'contact', 'address_line_1', 'address_line_2', 'street', 'state', 'zip_code')
        

class UploadForm(forms.ModelForm):
    name = forms.TextInput()
    price = forms.DecimalField()
    image = forms.ImageField()
    description = forms.TextInput()
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'description', 'category']
        

User = get_user_model()


