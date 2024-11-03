import random
import mysql.connector
from faker import Faker
from faker.providers import person

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="telegramshopbot"
)
cursor = conn.cursor()

fake = Faker("pt_BR")
fake.add_provider(person)

def populate_users():
    data = []
    for _ in range(10):
        name = fake.name()
        email = fake.email()
        data.append((name, email))

    query = "INSERT INTO users (name, email) VALUES (%s, %s)"

    try:
        cursor.executemany(query, data)
        conn.commit()
        print("Usuários inseridos com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        conn.rollback()


def populate_categories():
    data = [
        ("Frutas",),
        ("Vegetais",),
        ("Carnes",),
        ("Laticínios",),
        ("Grãos e Cereais",),
        ("Doces",),
        ("Bebidas",),
        ("Pães e Massas",),
        ("Condimentos",),
        ("Snacks",),
    ]

    query = "INSERT INTO categories (name) VALUES (%s)"

    try:
        cursor.executemany(query, data)
        conn.commit()
        print("Categorias inseridas com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        conn.rollback()


def populate_products():
    data = []
    for _ in range(1000):
        category_id = random.randint(1, 10)
        photo_url = "https://picsum.photos/200/200"
        name = fake.word().capitalize()
        description = fake.text(max_nb_chars=100)
        price = round(random.uniform(10.00, 100.00), 2)

        data.append((category_id, photo_url, name, description, price))

    query = "INSERT INTO products (category_id, photo_url, name, description, price) VALUES (%s, %s, %s, %s, %s)"

    try:
        cursor.executemany(query, data)
        conn.commit()
        print("Produtos inseridos com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        conn.rollback()


def populate_clients():
    data = []
    for _ in range(100):
        name = fake.name()
        cpf = fake.cpf().replace(".", "").replace("-", "")
        phone_number = fake.phone_number()
        city = fake.city()
        address = fake.address()
        is_active = fake.boolean()

        data.append((name, cpf, phone_number, city, address, is_active))

    query = """
        INSERT INTO clients (name, cpf, phone_number, city, address, is_active)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(query, data)
        conn.commit()
        print("Clientes inseridos com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        conn.rollback()


def populate_orders():
    data = []
    for _ in range(100):
        client_id = random.randint(1, 100)
        created_data = fake.date_time_this_year()
        status = 1
        amount = random.randint(1, 10)

        data.append((client_id, created_data, status, amount))

    query = """
        INSERT INTO orders (client_id, created_date, status, amount)
        VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.executemany(query, data)
        conn.commit()
        print("Pedidos inseridos com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        conn.rollback()


def populate_order_item():
    data = []
    for _ in range(1000):
        order_id = random.randint(1, 100)
        product_id = random.randint(1, 1000)
        quantity = random.randint(1, 10)

        data.append((order_id, product_id, quantity))

    query = """
        INSERT INTO order_items (order_id, product_id, quantity)
        VALUES (%s, %s, %s)
    """

    try:
        cursor.executemany(query, data)
        conn.commit()
        print("Itens do pedido inseridos com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        conn.rollback()


populate_users()
populate_categories()
populate_products()
populate_clients()
populate_orders()
populate_order_item()


cursor.close()
conn.close()
