from .cart import Cart


#  create context processor so that our cart an work on all pages of the site

def cart(request):
    return{'cart': Cart(request)}