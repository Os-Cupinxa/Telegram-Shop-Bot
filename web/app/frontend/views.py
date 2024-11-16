from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Importe o modelo de usuário
from .models import Product
from django.contrib.auth import logout


from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category  # Assumindo que temos um modelo Product e Category
from django.contrib import messages
from .models import Client
from .models import Order
from .models import Message
from django.http import HttpResponse
from django.http import HttpResponseRedirect


import httpx

url = "http://localhost:8001/"

async def login_view(request):
    token = request.COOKIES.get('access_token')
    if token:
        return redirect('users_list')

    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    dataUser = {
        "email": username,
        "password": password
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url + "login/", json=dataUser)

    if response.status_code == 200:
        # Salvar o token de autenticação de acess token no cookie
        response_json = response.json()
        redirect_response = HttpResponseRedirect('users')
        redirect_response.set_cookie('access_token', response_json['access_token'])
        return redirect_response
    else:
        return render(request, 'login.html')

def logout_view(request):
    # Realiza o logout do usuário
    logout(request)

    # Cria uma resposta de redirecionamento para a página de login
    response = redirect('login')
    

    # Remove o cookie 'access_token'
    response.delete_cookie('access_token', path='/')
    

    return response

async def users_list(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')
    
    headers = {'Authorization': f'Bearer {token}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url + "users/", headers=headers)

    if response.status_code == 200:
        users = response.json()
        return render(request, 'main/users/all.html', {'users': users})
    else:
        return HttpResponse("Erro ao obter usuários", status=response.status_code)

async def users_add(request):
    if request.method == 'POST':
        token = request.COOKIES.get('access_token')
        if not token:
            return redirect('login')
        
        headers = {'Authorization': f'Bearer {token}'}

        email  = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        dataUser = {
            "email": email,
            "password": password,
            "name": username
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url + "users/", json=dataUser, headers=headers)

        if response.status_code == 200:
            return redirect('users_list')
        else:
            return HttpResponse("Erro ao adicionar usuário", status=response.status_code)
    else:
        return render(request, 'main/users/add.html')
    

async def users_edit(request, id):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')
    
    headers = {'Authorization': f'Bearer {token}'}

    if request.method == 'GET':
        async with httpx.AsyncClient() as client:
            response = await client.get(url + f"users/{id}", headers=headers)

        if response.status_code == 200:
            user = response.json()
            return render(request, 'main/users/edit.html', {'user': user})
        else:
            return HttpResponse("Erro ao obter usuário", status=response.status_code)
    
    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        user = request.POST
        dataUser = {
            "email": user.get('email'),
            "password": user.get('password'),
            "name": user.get('name')
        }
        async with httpx.AsyncClient() as client:
            response = await client.put(url + f"users/{id}", json=dataUser, headers=headers)

        if response.status_code == 200:
            return redirect('users_list')
        else:
            return HttpResponse("Erro ao editar usuário", status=response.status_code)

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


async def products_list(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')
    
    headers = {'Authorization': f'Bearer {token}'}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url+"products/", headers=headers)
    if response.status_code == 200:
        products = response.json()
    return render(request, 'main/products/all.html', {'products': products})

@csrf_exempt
async def product_add(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')
    
    headers = {'Authorization': f'Bearer {token}'}

    if request.method == "POST":
        product = request.POST
        dataProduct = {
            "category_id": 1,
            "photo_url": product.get('photo'),
            "name": product.get('name'),
            "description": product.get('description'),
            "price": product.get('price')
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url + "products/", json=dataProduct, headers=headers)

        if response.status_code == 200:
            return redirect('products_list')
        else:
            return HttpResponse("Erro ao adicionar produto", status=response.status_code)
    return render(request, 'main/products/add.html')    
    
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
async def categories_list(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')
    
    async with httpx.AsyncClient() as client:
        headers = {'Authorization': f'Bearer {token}'}
        response = await client.get(url+"categories/", headers=headers)
    if response.status_code == 200:
        categories = response.json()
    return render(request, 'main/categories/all.html', {'categories': categories})

async def category_add(request):
    # Resgatar o token do cookie
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')  # Redireciona para login se não tiver o token

    name = request.POST.get('name')
    data = {
        "name": name,
        "category": {"name": name},
        "emoji": "🍔"
    }

    async with httpx.AsyncClient() as client:
        # Passa o token Bearer no header da requisição
        headers = {'Authorization': f'Bearer {token}'}
        response = await client.post(url + "categories/", json=data, headers=headers)

    if response.status_code == 200:
        return redirect('categories_list')

    return render(request, 'main/categories/add.html')

def category_edit(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        return redirect('categories_list')

    return render(request, 'main/categories/edit.html', {'category': category})

def category_delete(request):
    if request.method == 'POST':
        category_id = request.POST.get('id')
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return redirect('categories_list')
    return redirect('categories_list')

# clients views.py
async def clients_list(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')
    
    headers = {'Authorization': f'Bearer {token}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url + "clients/", headers=headers)

    if response.status_code == 200:
        clients = response.json()
        return render(request, 'main/clients/all.html', {'clients': clients})
    else:
        return HttpResponse("Erro ao obter clientes", status=response.status_code)

async def client_edit(request, id):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')  # Certifique-se de que 'login' é uma rota válida.

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    # Lidar com requisições GET
    if request.method == 'GET':
        async with httpx.AsyncClient() as client:
            response = await client.get(url + f"clients/{id}", headers=headers)

        if response.status_code == 200:
            client = response.json()
            return render(request, 'main/clients/edit.html', {'client': client})
        else:
            return HttpResponse("Erro ao obter cliente", status=response.status_code)

    # Lidar com requisições PUT
    if request.method == 'POST':
        name = request.POST.get('name')
        cpf = request.POST.get('cpf')
        phoneNumber = request.POST.get('phoneNumber')
        city = request.POST.get('city')
        address = request.POST.get('address')
        active = request.POST.get('is_active') == '1'

        # Validação simples para os campos obrigatórios
        errors = {}
        if not name:
            errors['nameError'] = "Name is required."
        if not phoneNumber:
            errors['phoneNumberError'] = "Phone number is required."
        if not city:
            errors['cityError'] = "City is required."
        if not address:
            errors['addressError'] = "Address is required."

        if errors:
            return render(request, 'main/clients/edit.html', {'client': client, **errors})

        # Dados do cliente
        dataClient = {
            "name": name,
            "cpf": cpf,
            "phone_number": phoneNumber,
            "city": city,
            "address": address,
            "is_active": active
        }
        

        # Atualizar cliente na API
        async with httpx.AsyncClient() as client:
            response = await client.put(url + f"clients/?client_id={id}", json=dataClient, headers=headers)

        if response.status_code == 200:
            messages.success(request, "Client updated successfully.")
            return redirect('clients_list')  # Redirecionar para a lista de clientes ou outra rota válida.

        messages.error(request, "Error updating client.")
        return render(request, 'main/clients/edit.html', {'client': dataClient})

    return HttpResponse("Method not allowed", status=405)


# broadcast views.py7
#@login_required
#def broadcast(request):
#    return render(request, 'main/broadcasts/add.html')

# order views.py
async def orders_list(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')
    
    headers = {'Authorization': f'Bearer {token}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url + "orders/", headers=headers)
    
    if response.status_code == 200:
        orders = response.json()

    return render(request, 'main/orders/all.html', {'orders': orders})

# @login_required
# async def order_add(request):
#     token = request.COOKIES.get('access_token')
#     if not token:
#         return redirect('login')
    
#     headers = {'Authorization': f'Bearer {token}'}


#     if request.method == 'POST':
        
#         return redirect('orders_list')

#     clients = Client.objects.all()
#     return render(request, 'main/orders/add.html', {'clients': clients})

async def order_edit(request, id):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')
    
    headers = {'Authorization': f'Bearer {token}'}

    if request.method == 'GET':
        async with httpx.AsyncClient() as client:
            # Obter os detalhes do pedido
            response = await client.get(url + f"orders/{id}", headers=headers)

        if response.status_code == 200:
            order = response.json()

            # Obter itens associados ao pedido
            async with httpx.AsyncClient() as client:
                items_response = await client.get(url + f"orders/items/{id}", headers=headers)

            if items_response.status_code == 200:
                order['items'] = items_response.json()  # Adiciona os itens ao pedido
            else:
                order['items'] = []  # Caso dê erro, atribuir lista vazia

            return render(request, 'main/orders/edit.html', {'order': order})
        else:
            return HttpResponse("Erro ao obter pedido", status=response.status_code)

    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        # Extrair dados do formulário enviado
        order = request.POST
        dataOrder = {
            "client_id": order.get('client_id'),
            "amount": order.get('amount'),
            "status": order.get('status'),
            "items": json.loads(order.get('items', '[]')),  # Garante que itens seja uma lista válida
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(url + f"orders/{id}", json=dataOrder, headers=headers)

        if response.status_code == 200:
            return redirect('orders_list')
        else:
            return HttpResponse("Erro ao editar pedido", status=response.status_code)

@login_required
async def order_delete(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')
    
    headers = {'Authorization': f'Bearer {token}'}

    if request.method == 'POST':
        order_id = request.POST.get('id')
        async with httpx.AsyncClient() as client:
            response = await client.delete(url + f"orders/{order_id}", headers=headers)

        if response.status_code == 200:
            return redirect('orders_list')
    return redirect('orders_list')


# Exibição da lista de mensagens
@login_required
def messages_list(request):
    messages_list = Message.objects.all()
    return render(request, 'main/messages/all.html', {'messages': messages_list})


# Editar mensagem existente
@login_required
@csrf_exempt
def messages_edit(request, id):
    message = get_object_or_404(Message, id=id)

    if request.method == 'POST':
        message.description = request.POST.get('description')
        message.text = request.POST.get('text')
        message.save()
        return redirect('messages_list')

    return render(request, 'main/messages/edit.html', {'messages': message})

# Deletar mensagem
@login_required
def messages_delete(request):
    if request.method == 'POST':
        message_id = request.POST.get('id')
        message = get_object_or_404(Message, id=message_id)
        message.delete()
        return redirect('messages_list')

    return redirect('messages_list')



