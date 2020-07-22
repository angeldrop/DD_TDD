from django.shortcuts import render,redirect
from lists.models import Item,List
from lists.forms import ItemForm
from django.core.exceptions import ValidationError


# Create your views here.
def home_page(request):

       return render(request,'lists/home.html',{'form':ItemForm()})


def view_list(request,list_id):
    form=ItemForm()
    list_=List.objects.get(id=list_id)
    if request.method=='POST':
        form=ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'],list=list_)
            return redirect(list_)
    return render(request,'lists/list.html',{'form':form,'list':list_})
    


def new_list(request):
    form=ItemForm(data=request.POST)
    if form.is_valid():
        list_=List.objects.create()
        Item.objects.create(text=request.POST['text'],list=list_)
        return redirect(list_)
    else:
        return render(request,'lists/home.html',{"form":form})
