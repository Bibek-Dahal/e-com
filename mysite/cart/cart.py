from store.models import Product
from django.http import JsonResponse

class Cart():
    def __init__(self,request):
        self.request = request
        
        
    def add_to_cart(self,request,**kwargs):
        print('#################&&&&&&&')
        cart_products = request.session.get('cart')
        # print('cart products^^^^^^',cart_products)
        # if cart_products is not None:
        if cart_products is not None:
            if kwargs['id'] not in cart_products.keys():
                cart_products[kwargs['id']] = {'price':kwargs['price'],'quantity':kwargs['quantity']}
                request.session['cart'] = cart_products
                request.session.modified = True
            else:
                print('hello')
                request.session['cart'][kwargs['id']]['quantity'] = kwargs['quantity']
                request.session.modified = True
                return JsonResponse({'msg':'successfully updated'})
        else:
           request.session['cart'] = {kwargs['id']:{'price':kwargs['price'],'quantity':kwargs['quantity']}}
           request.session['shipping_charge'] = 300

    def show_quantity(self):
        
        sum = 0
        item = self.request.session.get('cart')
        # print(item)
        if item:
            for x in item.keys():
                sum = sum + int(item[x]['quantity'] )
                # print(sum)
            return sum
                
        return sum

    def show_items(self):
        quantity = []
        products = Product.objects.filter(id__in=self.request.session.get('cart').keys())
        for p in products:
            subtotal = int(self.request.session.get('cart')[str(p.id)]['quantity'])*p.discount_price
            # print(subtotal)
            # print(p.id)
            quantity.append({'product':p,'quantity':self.request.session.get('cart')[str(p.id)]['quantity'],'subtotal':subtotal})
            
        # print('quantity',quantity)
        return(quantity)

    def subTotal(self):
        #return price excluding shipping address
        sum = 0
        products = self.show_items()
        for p in products:
            sum = sum + int(p['subtotal'])
            #sum = sum + self.request.session.get('shipping_charge')
        return sum

    def showShippingCharge(self):
        return self.request.session.get('shipping_charge')

    def total(self):
        #returns the total charge including shipping charge
        return self.subTotal()+self.showShippingCharge()
    

        