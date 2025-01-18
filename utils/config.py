# 📁 utils/config.py

# API BASE URL
BASE_URL = "https://fakestoreapi.com"
BASE_ENDPOINT = "/products"
URL = f"{BASE_URL}{BASE_ENDPOINT}"

# Large Data for Testing (Edge Cases)
LARGE_TITLE = "A" * 500000  # 500000 characters (reasonable for testing)
LARGE_PRICE = 10 ** 500  # Large number
LARGE_IMAGE_URL = "https://" + "a" * 500000 + ".com"  # ~500000-character URL