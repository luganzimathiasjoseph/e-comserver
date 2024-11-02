from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User, Business, Customer, CustomPermission
from . models import *
from django.contrib import admin
from .models import Contact
class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class UserAdmin(BaseUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('username', 'email', 'name', 'type', 'is_staff')
    list_filter = ('type', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Type'), {'fields': ('type',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'type', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'name')
    ordering = ('username',)

    def get_form(self, request, obj=None, **kwargs):
        """Modify the form based on the user instance."""
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }

        if (not is_superuser and obj and obj == request.user):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

    def get_fieldsets(self, request, obj=None):
        """Dynamically adjust fieldsets based on the user type."""
        fieldsets = super().get_fieldsets(request, obj)
        if not obj:  # adding user
            return fieldsets

        if obj.type == User.Types.BUSINESS:
            fieldsets += ((_('Business Specific'), {'fields': ('custom_fields_for_business',)}),)
        elif obj.type == User.Types.CUSTOMER:
            fieldsets += ((_('Customer Specific'), {'fields': ('custom_fields_for_customer',)}),)

        # Adjust or add more fieldsets based on your model structure

        return fieldsets
    
class BusinessAdmin(UserAdmin):
    list_display = ['username', 'email', 'name', 'type']
    list_filter = ['type']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'name', 'type', 'is_staff', 'is_superuser'),
        }),
    )

class CustomerAdmin(UserAdmin):
    list_display = ['username', 'email', 'name', 'type']
    list_filter = ['type']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'name', 'type', 'is_staff', 'is_superuser'),
        }),
    )

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'is_published', 'created_at')
    list_display_links = ('id','name') 
    list_filter = ('price',)
    list_editable = ('is_published',)
    search_fields = ('name', 'price')
    ordering = ('price',)
    
# Register your models here.
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)

# admin.site.register(CustomPermission)

