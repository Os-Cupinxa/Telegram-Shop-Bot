from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Importe o modelo de usuário
from .models import Product

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category  # Assumindo que temos um modelo Product e Category
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('users_list')  # Redireciona para a aba de usuários
        else:
            return HttpResponseRedirect('/?error=true')  # Redireciona com erro

    return render(request, 'login.html')

@login_required
def users_list(request):
    users = User.objects.all()  # Obtenha todos os usuários
    return render(request, 'main/users/all.html', {'users': users})

@login_required
def users_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect('users_list')

    return render(request, 'main/users/add.html')

@login_required
def users_edit(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('users_list')

    return render(request, 'main/users/edit.html', {'user': user})

@login_required
def users_delete(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('users_list')
    return redirect('users_list')


# views.py


@login_required
def products_list(request):
    products = Product.objects.all()
    return render(request, 'main/products/all.html', {'products': products})

@login_required
@csrf_exempt
def product_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        category = get_object_or_404(Category, id=category_id)
        photoUrl = request.POST.get('photo')

        product = Product(name=name, description=description, category=category, price=price, photoUrl=photoUrl)
        product.save()
        return redirect('products_list')

    categories = Category.objects.all()
    return render(request, 'main/products/add.html', {'categories': categories})

@login_required
@csrf_exempt
def product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        category_id = request.POST.get('category')
        product.category = get_object_or_404(Category, id=category_id)
        product.price = request.POST.get('price')

        if 'photo' in request.FILES:
            product.photo = request.FILES['photo']

        product.save()
        return redirect('products_list')

    categories = Category.objects.all()
    return render(request, 'main/products/edit.html', {'product': product, 'categories': categories})

@login_required
@csrf_exempt
def product_delete(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        messages.success(request, "Product deleted successfully")
        return redirect('products_list')
    return redirect('products_list')


# categories views.py
@login_required
def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'main/categories/all.html', {'categories': categories})

@login_required
def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = Category(name=name)
        category.save()
        return redirect('categories_list')

    return render(request, 'main/categories/add.html')

@login_required
def category_edit(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        return redirect('categories_list')

    return render(request, 'main/categories/edit.html', {'category': category})

@login_required
def category_delete(request):
    if request.method == 'POST':
        category_id = request.POST.get('id')
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return redirect('categories_list')
    return redirect('categories_list')
