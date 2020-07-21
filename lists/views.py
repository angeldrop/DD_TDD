from django.shortcuts import render,redirect
from lists.models import Item,List
from lists.forms import ItemForm
from django.core.exceptions import ValidationError


# Create your views here.
def home_page(request):

       return render(request,'lists/home.html',{'form':ItemForm()})


def view_list(request,list_id):
    list_=List.objects.get(id=list_id)
    error=None
    
    if request.method=='POST':
        try:
            item=Item(text=request.POST['text'],list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error="你不能输入空项目"
    return render(request,'lists/list.html',{"error":error,'list':list_})
    


def new_list(request):
    list_=List.objects.create()
    item=Item(text=request.POST['text'],list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error="你不能输入空项目"
        return render(request,'lists/home.html',{"error":error})
    return redirect(list_)
