from django.shortcuts import render,redirect
from lists.models import Item,List
from django.core.exceptions import ValidationError


# Create your views here.
def home_page(request):

       return render(request,'lists/home.html')


def view_list(request,list_id):
    if request.method=='POST':
        list_=List.objects.create()
        Item.objects.create(text=request.POST['item_text'],list=list_)
        return redirect(f'/lists/{list_id}/')
 
    
    list_=List.objects.get(id=list_id)
    items=Item.objects.filter(list=list_)
    return render(request,'lists/list.html',{
        'list':list_
    })


def new_list(request):
    list_=List.objects.create()
    item=Item(text=request.POST['item_text'],list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error="你不能输入空项目"
        return render(request,'lists/home.html',{"error":error})
    return redirect(f'/lists/{list_.id}/')

def add_item(request,list_id):
    list_=List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'],list=list_)
    return redirect(f'/lists/{list_.id}/')