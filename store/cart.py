from store.models import *
class Cart():
    def __init__(self, request):
        self.session = request.session
        # get the current session key if it exists
        cart = self.session.get('session_key')
        
        # if the customer is new no session key create one
        
        if 'session_key' not in request.session:
            cart = self.session['session_key']={}
            
            
        # make sure that the cart is available on all pages of site    
        self.cart = cart
    
        
    def add(self, product,quantity):
        product_id = str(product.id) 
        product_qty =str(quantity)  
        
        # Logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified= True
        
    def totals(self):
        # get product ids
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in= product_ids)
        # get quantites
        quantities =self.cart
        # start counting at 0
        total = 0
        for key, value in quantities.items():
            #  convert key string into int so we can do the math
            key = int(key)
            for product in products:
                if  product.id == key:
                    total = total + (product.price * value)
        return total
        

        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        # Use ids to lookup products in database models
        products = Product.objects.filter(id__in=product_ids)
        #  Return those looked up products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        try:
            product_qty = int(quantity)
        except ValueError:
            return None  # Handle invalid quantity gracefully, maybe log an error
        
        self.cart[product_id] = product_qty
        self.session['cart'] = self.cart
        self.session.modified = True
        
        return self.cart
    
    def delete(self,product):
        product_id = str(product)
        
        # Delete from dictionary
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True