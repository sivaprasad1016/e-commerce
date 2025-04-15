from django.http import JsonResponse
from django.shortcuts import redirect, render
from shop.form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json

def home(request):
   products=Product.objects.filter(trending=1)
   return render(request,"shop/index.html",{"products":products})

def favview_page(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("/")
  
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")



def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"shop/cart.html",{"cart":cart})
  else:
    return redirect("/")

def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")

def fav_page(request):
  if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      products_id=data['pid']
      products_status=Product.objects.get(id=products_id)
      if products_status:
        if Favourite.objects.filter(user=request.user.id,products_id=products_id):
          return JsonResponse({'status':'Product already in Favourite'}, status=200)
        else:
          Favourite.objects.create(user=request.user,products_id=products_id)
          return JsonResponse({'status':'Product Added  to Favourite'}, status=200)

    else:
      return JsonResponse({'status':'Login  to Favourite'}, status=200)
  else:
      return JsonResponse({'status':'Invalid Access'}, status=200)
    

def add_to_cart(request):
  if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      products_id=data['pid']
      # print(request.user.id)
      products_status=Product.objects.get(id=products_id)
      if products_status:
        if Cart.objects.filter(user=request.user.id,products_id=products_id):
          return JsonResponse({'status':'Product already in cart'}, status=200)
        else:
          if products_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,products_id=products_id,products_qty=product_qty)
            return JsonResponse({'status':'Product added to cart'}, status=200)
          else:
            return JsonResponse({'status':'Product stock not available'}, status=200)
    else:
          return JsonResponse({'status':'Login to Add Cart'}, status=200)
  else:
      return JsonResponse({'status':'Invalid Access'}, status=200)

def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Login in successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid username or password")
        return redirect("/login")
    return render(request,"shop/login.html")

def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logout in successfully")
  return redirect("/")


def register(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"shop/register.html",{'form':form})

def collections(request):
  
 category=Category.objects.filter(status=0)
 return render(request,"shop/collections.html",{"category": category})

def collectionsview(request,name):

  if(Category.objects.filter(name=name,status=0)):
     products=Product.objects.filter(category__name=name)
     return render(request,"shop/product.html",{"products":products,"category_name":name})
  else:
     messages.warning(request,"No Such Category Found")
     return redirect('collections')
  
def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        products=Product.objects.filter(name=pname,status=0).first()
        return render(request,"shop/product_details.html",{"products":products})
      else:
        messages.error(request,"No Such Category Found")
        return redirect('collections')
    else:
      messages.error(request,"No Such Category Found")
      return redirect('collections')
   



   


