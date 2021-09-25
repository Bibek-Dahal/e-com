from django.http import response,HttpResponseRedirect
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView, View
import json
from .cart import Cart
from store.models import Product, Customer
import requests
from .models import Order
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.mail import send_mail
import uuid
x = 0

class FailuereOrderView(View):
    def get(self,request):
        messages.info(request, 'Sorry, Your Order Could Not Be Placed. Thank You!')
        return HttpResponseRedirect('/')

class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        #print('args', args)
        #print('kwargs', kwargs)
        #print(request.POST.get('quantity'))
        cart_obj = Cart(request)
        cart_obj.add_to_cart(request, id=request.POST.get(
            'id'), quantity=request.POST.get('quantity'), price=request.POST.get('price'))
        items = cart_obj.show_items()
        # current_obj = Product.objects.get(id=request.POST.get('id'))
        current_obj =  get_object_or_404(Product,id=request.POST.get('id'))
        obj = [p for p in items if p['product'] == current_obj]
        #print(obj)
        #print(request.POST.get('quantity'))
        #print(cart_obj.subTotal())
        # #print(request.session.get('cart'))

        return JsonResponse({'data': obj[0]['subtotal'],'length':cart_obj.show_quantity(), 's_price': cart_obj.subTotal(), 'length': cart_obj.show_quantity(), 'total_charge': cart_obj.total(), 'shipping_charge': cart_obj.showShippingCharge()})


@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class CartDetailView(TemplateView):
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, *args, **kwargs):
        #print('args', args)
        #print('kwargs', kwargs)
        if self.request.session.get('cart'):
            #print(self.request.session.get('cart'))
            context = super().get_context_data(**kwargs)
            cart_obj = Cart(self.request)
            #print(cart_obj.show_items())
            #print()
            #print(cart_obj.subTotal())
            context['sub_total'] = int(cart_obj.subTotal())
            context['products'] = cart_obj.show_items()
            context['length'] = cart_obj.show_quantity()
            context['shipping_charge'] = cart_obj.showShippingCharge()
            context['total'] = cart_obj.total()

            return context
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class RemoveCartView(View):

    def post(self, request, *args, **kwargs):
        cart_obj = Cart(self.request)
        #print('args', args)
        #print('kwargs', kwargs)
        #print(request.POST.get('pk'))
        pk = request.POST.get('pk')
        #print(request.session.get('cart'))
        items = request.session.get('cart')
        items.pop(request.POST.get('pk'))
        request.session['cart'] = items
        request.session.modefied = True
        request.session.clear_expired()

        return JsonResponse({'id':pk, 's_price': cart_obj.subTotal(), 'length': cart_obj.show_quantity(), 'total_charge': cart_obj.total(), 'shipping_charge': cart_obj.showShippingCharge()})


class VerifyKhalthiView(View):
    def post(self, request, *args, **kwargs):
        #print(self.request.POST.get('token'))
        #print(self.request.POST.get('amount'))
        # #print('data: ', request.POST.get('token'))
        # #print('amount',request.POST.get('amount'))
        token = self.request.POST.get('token')
        amount = self.request.POST.get('amount')
        # #print('amount', request.POST.get('name[amount]'))
        # #print(token)

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": "Key test_secret_key_b9ca176c98c84c3abc37b9a5ad2bd401"
        }

        response = requests.post(url, payload, headers=headers)
        # res = [r for r in response]
        #print(response)
        #print(response.text)
        #print(json.loads(response.text))
        res = json.loads(response.text)
        # #print('response', response)
        # #print()
        # #print()
        # #print(res.get('idx'))
        if res.get('idx'):
            return JsonResponse({'msg': 'success'})
        else:
            return JsonResponse({'msg':'failed'})


      

order_id = None
@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class BuyProducts(View):
    def generate_uuid(self):
            return(uuid.uuid4())

    def get(self, request):
        cart_obj = Cart(request)
        customer = Customer.objects.filter(customer=request.user)
        

        if customer:
            if request.session.get('cart'):
                order = self.request.COOKIES.get('order')
                #print('order',order)
                if order == None:
                    order = self.generate_uuid()
                    #print(order)
                context = {
                    'products': cart_obj.show_items(),
                    'total': cart_obj.subTotal(),
                    'customers': Customer.objects.filter(customer=self.request.user),
                    'uuid':order
                }
                response =  render(request, 'cart/checkout.html', context)
                response.set_cookie('order',order)
                return response
            else:
                return render(request, 'cart/add_to_cart_info.html')
        else:
            return redirect('account:customer_reg')

class VerifyEsewa(View):
    def get(self,request):
        #print('rid',request.GET.get('refId'))
        #print('pid',request.GET.get('oid'))
        url ="https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': 100,
            'scd': 'EPAYTEST',
            'rid': request.GET.get('refId'),
            'pid':request.GET.get('oid'),
        }
        resp = requests.post(url, d)
        #print('inside e-sewa')
        #print(resp.text)
        #print()
        #print('status_code',resp.status_code)
        if resp.status_code == 200:
            # order_url = 'http://127.0.0.1:8000/cart/order/'
            # cstoken =  request.COOKIES['csrftoken']
            # headers =  { "X-CSRFToken": cstoken }
            # payload = json.dumps({'id':request.GET.get('cid'),'order':request.GET.get('oid')})
            # requests.post(order_url,payload,headers=headers)
            # #print(self.request.COOKIES['csrftoken'])
            id = request.GET.get('cid')
            order_id = request.GET.get('oid')
            #print(order_id)
            cart_obj = Cart(request)
            user = request.user
            customer = Customer.objects.get(id=id)
            #print('inside order')
            #print(cart_obj.show_items())
            
            products = cart_obj.show_items()
            for p in products:
                Order.objects.create(user=user, customer=customer,order_id=order_id,
                                    product=p['product'], quantity=p['quantity'])
                
            del request.session['cart']
            response = HttpResponseRedirect('/')
            # response.delete_cookie['order']
            messages.info(request, 'Your Order Has Been Successfully Placed.')
            response.delete_cookie('order')
            #print(user.email)
            return response
        return HttpResponse('error')

        

@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class OrderView(View):
    def post(self, request):
        order_id = request.POST.get('order')
        #print(order_id)
        cart_obj = Cart(request)
        user = request.user
        # customer = Customer.objects.get(id=request.POST.get('id'))
        customer = get_object_or_404(Customer,id=request.POST.get('id'))
        #print('inside order')
        #print(cart_obj.show_items())
        #print(request.POST.get('id'))
        products = cart_obj.show_items()
        for p in products:
            Order.objects.create(user=user, customer=customer,order_id=order_id,
                                 product=p['product'], quantity=p['quantity'])
            
        del request.session['cart']
        response = HttpResponseRedirect('/')
        messages.info(request, 'Your Order Has Been Successfully Placed.')
        response.delete_cookie('order')
        #print(user.email)
        return response


@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class MyOrderView(TemplateView):
    template_name = 'cart/my_order.html'
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data()
        context['orders']  = Order.objects.filter(user=self.request.user)
        return context
        