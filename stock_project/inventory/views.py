from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import stockItem
from.forms import ItemForm, UserRegistrationForm
from django.contrib import messages


# Create your views here.
def is_staff_user(user):
    return user.is_staff

def register_view(request):
    if request.method =='POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('inventory:index')
    else:
        form =UserRegistrationForm()
    return render(request,'inventory/register.html',{'form':form})    

def login_view(request):
    if request.method =='POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request,username=username,password=pwd)
        if user:
            login(request,user)
            return redirect('inventory:item_list')
    else:
        messages.error(request,"invalid username or password")    
    return render(request,'inventory/login.html')
def logout_view(request):
    logout(request)
    return redirect('inventory:login')

@login_required
def item_list(request):
    items =stockItem.objects.all()
    return  render(request,'inventory/item_list.html',{items:items})

@login_required
def item_detail(request,item):
    item = get_object_or_404(stockItem,id=item)
    return render(request,'inventory/item_detail.html',{'item':item})
@login_required
@user_passes_test(is_staff_user)
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:item_list')
        else:
           form = ItemForm() 
        return render(request,'inventory/item_form.html',{'form':form})
    
    @login_required
    @user_passes_test(is_staff_user)
    def item_update(request,item):
        item = get_object_or_404(stockItem,id=item)
        if request.method == 'POST':
            form = ItemForm(request.POST,instance=item)
            if form.is_valid():
                form.save()
                return redirect('inventory:item_list')
        else:
            form = ItemForm(instance=item)
        return render(request,'inventory/item_form.html',{'form':form})
@login_required
@user_passes_test(is_staff_user)    
def item_delete(request,item):
    item = get_object_or_404(stockItem,id=item)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory:item_list')
    return render(request,'inventory/item_confirm_delete.html',{'item':item})




























def index(request):
    items = stockItem.objects.all().order_by('id')
    return render(request, 'inventory/index.html', {'items': items})
def add_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        quantity = request.POST['quantity']
        price = request.POST['price']
        category = request.POST['category']
        stockItem.objects.create(name=name, quantity=quantity, price=price, category=category)
    return render(request, 'inventory/add_item.html')
def edit_item(request,id):
    item = get_object_or_404(stockItem, id=id)
    if request.method == 'POST':
        item.name = request.POST['name']
        item.quantity = request.POST['quantity']
        item.price = request.POST['price']
        item.category = request.POST['category']
        item.save()
        return redirect('index')
    return render(request, 'inventory/index.html', {'items': item})

def delete_item(request,item_id):
    item = get_object_or_404(stockItem, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('index')
    return render(request, 'inventory/index.html', {'items': item})
