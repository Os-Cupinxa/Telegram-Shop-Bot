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

from app.env_config import SERVER_URL

url = f"{SERVER_URL}"


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

        email = request.POST.get('email')
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


async def users_delete(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}
    if request.method == 'POST':
        user_id = request.POST.get('id')
        async with httpx.AsyncClient() as client:
            response = await client.delete(url + f"users/{user_id}", headers=headers)

        if response.status_code == 200:
            return redirect('users_list')
        else:
            return HttpResponse("Erro ao deletar usuário", status=response.status_code)
    return redirect('users_list')


# views.py


async def products_list(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url + "products/", headers=headers)
    if response.status_code == 200:
        products = response.json()

    return render(request, 'main/products/all.html', {'products': products})


@csrf_exempt
async def product_add(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}

    if request.method == 'GET':
        async with httpx.AsyncClient() as client:
            response = await client.get(url + "categories/", headers=headers)

        if response.status_code == 200:
            categories = response.json()
            return render(request, 'main/products/add.html', {'categories': categories})
        else:
            return HttpResponse("Erro ao obter categorias", status=response.status_code)

    if request.method == "POST":
        product = request.POST
        dataProduct = {
            "category_id": product.get('category'),
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


async def product_edit(request, id):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}
    if request.method == 'GET':
        async with httpx.AsyncClient() as client:
            response = await client.get(url + f"products/{id}", headers=headers)

        if response.status_code == 200:
            product = response.json()

        async with httpx.AsyncClient() as client:
            response = await client.get(url + "categories/", headers=headers)

        if response.status_code == 200:
            categories = response.json()
            product['categories'] = categories
            return render(request, 'main/products/edit.html', {'product': product})
        else:
            return HttpResponse("Erro ao obter produto", status=response.status_code)

    if request.method == 'POST':

        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = int(request.POST.get('category', 0))  # Valor padrão como 0 se não fornecido
        price = float(request.POST.get('price', 0))  # Valor padrão como 0.0 se não fornecido
        photo_url = request.POST.get('photo_url')

        dataProduct = {
            "category_id": category_id,
            "photo_url": photo_url,
            "name": name,
            "description": description,
            "price": price
        }
        async with httpx.AsyncClient() as client:
            response = await client.put(url + f"products/?product_id={id}", json=dataProduct, headers=headers)

        if response.status_code == 200:
            return redirect('products_list')
        else:
            return HttpResponse("Erro ao editar produto", status=response.status_code)

    return render(request, 'main/products/edit.html', {'product': product})


@csrf_exempt
async def product_delete(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}

    if request.method == 'POST':
        product_id = request.POST.get('id')
        async with httpx.AsyncClient() as client:
            response = await client.delete(url + f"products/{product_id}", headers=headers)

        if response.status_code == 200:
            return redirect('products_list')
        else:
            return HttpResponse("Erro ao deletar produto", status=response.status_code)

    return redirect('products_list')


# categories views.py
async def categories_list(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')

    async with httpx.AsyncClient() as client:
        headers = {'Authorization': f'Bearer {token}'}
        response = await client.get(url + "categories/", headers=headers)
    if response.status_code == 200:
        categories = response.json()
    return render(request, 'main/categories/all.html', {'categories': categories})


async def category_add(request):
    # Resgatar o token do cookie
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')  # Redireciona para login se não tiver o token

    name = request.POST.get('name')
    emoji = request.POST.get('emoji')
    data = {
        "name": name,
        "category": {"name": name},
        "emoji": emoji
    }

    async with httpx.AsyncClient() as client:
        # Passa o token Bearer no header da requisição
        headers = {'Authorization': f'Bearer {token}'}
        response = await client.post(url + "categories/", json=data, headers=headers)

    if response.status_code == 200:
        return redirect('categories_list')

    return render(request, 'main/categories/add.html')


async def category_edit(request, id):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}

    if request.method == 'GET':
        async with httpx.AsyncClient() as client:
            response = await client.get(url + f"categories/{id}", headers=headers)

        if response.status_code == 200:
            category = response.json()
            return render(request, 'main/categories/edit.html', {'category': category})
        else:
            return HttpResponse("Erro ao obter categoria", status=response.status_code)
    if request.method == 'POST':
        category = request.POST
        dataCategory = {
            "name": category.get('name'),
            "emoji": category.get('emoji')
        }
        async with httpx.AsyncClient() as client:
            response = await client.put(url + f"categories/?category_id={id}", json=dataCategory, headers=headers)

        if response.status_code == 200:
            return redirect('categories_list')
        else:
            return HttpResponse("Erro ao editar categoria", status=response.status_code)

    return render(request, 'main/categories/edit.html', {'category': category})


async def category_delete(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}

    if request.method == 'POST':
        category_id = request.POST.get('id')
        async with httpx.AsyncClient() as client:
            response = await client.delete(url + f"categories/{category_id}", headers=headers)

        if response.status_code == 200:
            return redirect('categories_list')
        else:
            return HttpResponse("Erro ao deletar categoria", status=response.status_code)

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
# @login_required
# def broadcast(request):
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
            
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url + "clients/"+str(order['client_id']), headers=headers)
            
            if response.status_code == 200:
                clientRequest = response.json()
                order['client'] = clientRequest
            return render(request, 'main/orders/edit.html', {'order': order})
        else:
            return HttpResponse("Erro ao obter pedido", status=response.status_code)

    if request.method == 'POST':
        items = []
        for i in range(len(request.POST.getlist('items[0].id'))):
            item = {
                "product_id": request.POST.get(f'items[{i}].product_id'),
                "quantity": request.POST.get(f'items[{i}].quantity'),
            }
            items.append(item)

        dataOrder = {
            "client_id": request.POST.get('client_id'),
            "amount": request.POST.get('amount'),
            "status": request.POST.get('status'),
            "items": items,
        }

        print(dataOrder)

        async with httpx.AsyncClient() as client:
            response = await client.put(url + f"orders/?order_id={id}", json=dataOrder, headers=headers)

        if response.status_code == 200:
            return redirect('orders_list')
        else:
            return HttpResponse("Erro ao editar pedido", status=response.status_code)
    return render(request, 'main/orders/edit.html', {'order': order})



# Exibição da lista de mensagens (via HTTP)
async def messages_list(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url + "messages/", headers=headers)

    if response.status_code == 200:
        messages = response.json()
        print(messages)
        return render(request, 'main/messages/all.html', {'messages': messages})

    return HttpResponse("Erro ao obter mensagens", status=response.status_code)






# Editar mensagem existente
def messages_edit(request, id):
    message = get_object_or_404(Message, id=id)

    if request.method == 'POST':
        message.description = request.POST.get('description')
        message.text = request.POST.get('text')
        message.save()
        return redirect('messages_list')

    return render(request, 'main/messages/edit.html', {'messages': message})

