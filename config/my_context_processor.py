from mapshop.models import Order
def my_context_processor(request):
   
   return {'orders':Order.objects.all()} 
