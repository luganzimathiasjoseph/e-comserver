from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import business, customer, staff


urlpatterns = [
    

    path('staff/', include(([
          path('paymentoptions/', staff.paymentoptions, name='paymentoptions'),
          path('returns/', staff.returns, name='returns'),
          path('register/', staff.register, name = 'register'),
          path('login/', staff.login, name = 'login'),
          path('logout/', staff.logout, name = 'logout'),
          path('update_user/', staff.update_user, name = 'update_user'),
          path('FAQS/', staff.FAQS,name='FAQS'),
          path('contact/', staff.contact,name='contact'),
          path('index/', staff.index,name='index'),
          path('about/', staff.about,name='about'),
          path('profile_redirect/', staff.profile_redirect, name = 'profile_redirect'),
          path('account/', staff.account, name = 'account'),
          path('homepage/',staff.homepage,name='homepage'),
          path('services', staff.services, name='services'),
          path('web_settings/', staff.web_settings, name='web_settings'),

      ],'store'), namespace='staff')),

    path('business/', include(([
          
          path('profile/', business.profile, name = 'profile'),
          path('dashboard',business.dashboard,name='dashboard'),
          path('businesscustomer/<str:pk>/',business.businesscustomer,name='businesscustomer'),
          path('upload',business.upload,name='upload'),
          path('updateProduct/<str:pk>/',business.updateProduct,name='updateProduct'),
          path('deleteProduct/<str:pk>/',business.deleteProduct,name='deleteProduct'),
      ],'store'), namespace='business')),
    
    path('customer/', include(([
        path('dashboard', customer.dashboard, name = 'dashboard'),
        path('profile/', customer.profile, name = 'profile'),
        path('product/<int:pk>',customer.product,name='product'),
        path ('category/<str:pa>',customer.category, name='category'),
        path('cart_summary',customer.cart_summary,name='cart_summary'),
        path('checkout/',customer.checkout, name='checkout'),
        path ('cart_add/',customer.cart_add, name='cart_add'),
        path ('cart_update/',customer.cart_update, name='cart_update'),
        path ('cart_delete/',customer.cart_delete, name='cart_delete'),
        path ('search_items/',customer.search_items, name='search'), #search
        path('languages/', customer.languages, name='languages'),
    
    
      ],'store'), namespace='customer')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

   
