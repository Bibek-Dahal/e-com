from django.http.response import HttpResponse, JsonResponse,HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from .models import Catagory, Product, Product_image, ProductInventory
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
import json
from django.core.mail import send_mail


def Home(request):
    query_set = {}
    catagories = Catagory.objects.all()
    for c in catagories:
        if c.cat_prods():
            query_set[c] = c.cat_prods()[:min(len(c.cat_prods()),5)]
    # print(query_set)
    x=ProductInventory.objects.filter(sku = '12888blacknoteredmi')
    
    return render(request,"store/home.html",{'query_set':query_set})
    
     

class ProductDetailView(TemplateView):
    template_name = 'store/product_detail_view.html'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['prod'] = get_object_or_404(Product,slug=slug)
        if self.request.session.get('cart'):
            context['cart_keys'] = [ int(x) for x in self.request.session.get('cart').keys()]
        return context

class CatagoryView(TemplateView):
    template_name = 'store/catagory.html'
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        # cat_name = get_object_or_404(Catagory,slug = slug)
        context['catagory']=get_object_or_404(Catagory,slug = slug)
        return context
    
    # return render(request,'store/catagory.html',{'catagories_list':Product.objects.filter(catagory = cat_name) })

