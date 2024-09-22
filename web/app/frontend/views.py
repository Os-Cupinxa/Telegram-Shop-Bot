from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Importe o modelo de usuário

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