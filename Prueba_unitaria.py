import requests
import threading
import time

# URL base de la API
BASE_URL = "http://127.0.0.1:5000/items"

# Número de solicitudes a enviar
NUM_REQUESTS = 1000

# Número de hilos (para concurrencia)
NUM_THREADS = 10

# Función para realizar una solicitud POST
def post_item():
    data = {
        "name": "Item Stress Test",
        "description": "This is a stress test item",
        "price": 9.99
    }
    response = requests.post(BASE_URL, json=data)
    if response.status_code == 201:
        print("Item created successfully")
    else:
        print(f"Failed to create item: {response.status_code}")

# Función para realizar una solicitud GET
def get_items():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        print("Items retrieved successfully")
    else:
        print(f"Failed to retrieve items: {response.status_code}")

# Función para realizar la prueba de estrés
def stress_test():
    for _ in range(NUM_REQUESTS):
        post_item()
        get_items()

# Crear múltiples hilos para realizar la prueba en concurrencia
threads = []
for i in range(NUM_THREADS):
    thread = threading.Thread(target=stress_test)
    threads.append(thread)

# Tiempo de inicio
start_time = time.time()

# Iniciar todos los hilos
for thread in threads:
    thread.start()

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()

# Tiempo de fin
end_time = time.time()

# Duración total de la prueba
duration = end_time - start_time
print(f"Prueba de estrés completada en {duration} segundos")