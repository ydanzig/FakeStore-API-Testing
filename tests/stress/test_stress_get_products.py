import threading
from utils.api_client import get

def test_get_products_stress():
    def make_request():
        response = get("/products")
        assert response.status_code == 200

    threads = []
    for _ in range(100):  # Simulate 100 concurrent requests
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
