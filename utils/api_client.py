import requests

BASE_URL = "https://fakestoreapi.com"

def get(endpoint):
    return requests.get(f"{BASE_URL}{endpoint}")

def post(endpoint, data):
    return requests.post(f"{BASE_URL}{endpoint}", json=data)

def delete(endpoint):
    return requests.delete(f"{BASE_URL}{endpoint}")