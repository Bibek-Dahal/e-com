from django.db.models.deletion import SET_NULL
from user_account.models import MyUser
from django.db import models
from store.models import Customer,Product


class Order(models.Model):
    order_status = (
        
        ('Accepted','Accepted'),
        ('Packed','Packed'),
        ('On The Way','On The Way'),
        ('Delivered','Delivered'),
        ('Reject','Reject')
    )
    user = models.ForeignKey(MyUser,on_delete=SET_NULL,null=True)
    order_id = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,related_name='orders')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,choices=order_status,null=True)

    # def __str__(self):
    #     return self.customer.full_name
    class Meta:
        ordering = ['-created_at']
    


